# -*- coding: utf-8 -*-

from __future__ import division, print_function
import tensorflow as tf
import numpy as np
import os, sys, time, re
from multiprocessing import Pool
import util

os.environ['CUDA_DEVICES_ORDER'] = 'PCI_BUS_ID'
os.environ['CUDA_VISIBLE_DEVICES'] = '0, 1'    # the GPU(s) can be used

# If you don't config the GPUs, TensorFlow would occupy all free memory of the visible GPUs.
# Set the `per_process_gpu_memory_fraction` to restrict the usable memory.
# Set the `allow_growth` the let it self-adaptively fetch the memory, however some memory
# would be wasted as the program would apply for more memory than it actually need.
# Since the first GPU is used to store some shared variables, it need more memory than the rest.
config = tf.ConfigProto()
#config.gpu_options.per_process_gpu_memory_fraction = 0.3
config.gpu_options.allow_growth = True

if __name__ == '__main__':
    
    data_path = '/home/hzm/cifar_data'  # data path
    ckpt_meta = 'ckpt/model-final.meta' # meta checkpoint the resotre the graph
    ckpt = 'ckpt/model-final'           # checkpoint to resotre the variables
    classes = 10                        # total classes of the label
    epochs = 200                        # epochs to train
    init_lr = 0.1                       # initial learning rate
    # You can define the learning rate foe every epoch or even every batch, 
    # by feeding the `lr` in the feed_dict (see the Training Stage codes).
    # By default we use the cosine decay rate without restart for every batch, 
    # you can set the offset of the cosine function to restart the training with the proper lr.
    # Below is the learining rate used in origingal papers for ResNet.
    # learning_rate = lambda e: init_lr if e < 100 else (init_lr / 10) if e < 150 else (init_lr / 100)
    
    use_val = False                     # whether apply the validation with part of training set
    val_ratio = 0.1                     # take a part of the traing set to apply validation
    train_batch_size = 128              # batch size of the training set
    val_batch_size = 100                # batch size of the validating set
    
    # Below are some augment methods, read the corresponding papers for details. 
    # Set `mixip_alpha` zero to disable the mixup augmentation, 
    # and a non-zero float number represents the alpha (here equal to beta) of the BETA distribution.
    # Set `autoAugment` TRUE to enable the auto-Augmentation.
    # Set mixup_alpha = 0 and autoAugment = False to use the baseline augment methods.
    # Generally, autoAugmentation is better than mixup, and even better with both two.
    mixup_alpha = 1.0
    autoAugment = True
    
    """
    ---------------------------------------------------------------------------
    Gather the dataset.
    ---------------------------------------------------------------------------
    """
    fs = os.listdir(os.path.join(data_path, 'train'))
    xs_train = np.array([os.path.join(data_path, 'train', f) for f in fs])
    ys_train = np.array([int(re.split('[_.]', f)[1]) for f in fs])
    
    fs = os.listdir(os.path.join(data_path, 'test'))
    xs_test = np.array([os.path.join(data_path, 'test', f) for f in fs])
    ys_test = np.array([int(re.split('[_.]', f)[1]) for f in fs])
    
    if use_val == True:
        # Take a part of the traing set as the validation set.
        val_size = int(ys_train.shape[0] * val_ratio)
        val_batches = val_size // val_batch_size
        val_size = val_batches * val_batch_size
        
        rnd = np.random.permutation(range(ys_train.shape[0]))
        xs_val, xs_train = xs_train[rnd[:val_size]], xs_train[rnd[val_size:]]
        ys_val, ys_train = ys_train[rnd[:val_size]], ys_train[rnd[val_size:]]
    else:
        xs_val, ys_val = np.copy(xs_test), np.copy(ys_test)
        val_size = xs_val.shape[0]
        val_batches = val_size // val_batch_size
        
    train_batches = xs_train.shape[0] // train_batch_size
    
    ###########################################################################
    # Preprocess the validating images with multiprocessing.
    procs = 5
    splits = [(xs_val.shape[0] // procs) * i for i in range(procs)[1:]]
    xs_val = np.split(xs_val, splits)
    ys_val = np.split(ys_val, splits)
    
    pool = Pool(procs)
    results = []
    for i in range(procs):
        results.append(pool.apply_async(util.batch_parse, (xs_val[i], ys_val[i], False, mixup_alpha, autoAugment, classes)))
        
    pool.close()
    pool.join()
    
    xs_val, ys_val = [], []
    for result in results:
        a, b = result.get()
        xs_val.extend(a)
        ys_val.extend(b)
    xs_val, ys_val = np.stack(xs_val), np.stack(ys_val)
    del (results, result, a, b)
    ###########################################################################
    
    """
    ---------------------------------------------------------------------------
    Restore the network and start training.
    ---------------------------------------------------------------------------
    """
    with tf.Session(config=config) as sess:
        
        saver = tf.train.import_meta_graph(ckpt_meta)
        saver.restore(sess, ckpt)
        
        graph = tf.get_default_graph()
        xs = graph.get_operation_by_name('Data_loader/xs').outputs[0]
        ys = graph.get_operation_by_name('Data_loader/ys').outputs[0]
        batch_size = graph.get_operation_by_name('Data_loader/batch_size').outputs[0]
        train_flag = graph.get_operation_by_name('training_flag').outputs[0]
        lr = graph.get_operation_by_name('lr').outputs[0]
        
        tower_error = tf.get_collection('error')[0]
        tower_loss = tf.get_collection('loss')[0]
        train_op = tf.get_collection('train_op')[0]
        data_loader_initializer = tf.get_collection('data_loader_initializer')[0]
        
        # gather the variables to save
        params = 0
        for var in tf.trainable_variables():
            params += np.prod(var.get_shape().as_list())
            
        saver = tf.train.Saver(max_to_keep=5)
        
        #######################################################################
        # Augment the training data with multiprocess.
        print('Data preparing ...')
        procs = 5
        splits = [(xs_train.shape[0] // procs) * i for i in range(procs)[1:]]
        xs_train1 = np.split(xs_train, splits)
        ys_train1 = np.split(ys_train, splits)
        
        pool = Pool(procs)
        results = []
        for i in range(procs):
            results.append(pool.apply_async(util.batch_parse, (xs_train1[i], ys_train1[i], True, mixup_alpha, autoAugment, classes)))
        pool.close()
        pool.join()
        
        xs_train1, ys_train1 = [], []
        for result in results:
            a, b = result.get()
            xs_train1.extend(a)
            ys_train1.extend(b)
        xs_train1, ys_train1 = np.stack(xs_train1), np.stack(ys_train1)
        del (pool, results, result, a, b)
        #######################################################################
        
        print('Training ...')
        print('Trainable parameters: {}'.format(params))
        begin = time.time()
        
        rnd_samples = np.arange(ys_train.shape[0])
        train_losses, train_err = np.zeros([2, epochs])
        val_losses, val_err = np.zeros([2, epochs])
        best_val = 100.0
        
        for e in range(epochs):
            """
            -------------------------------------------------------------------
            Training stage.
            -------------------------------------------------------------------
            """
            sess.run(data_loader_initializer, feed_dict={xs: xs_train1, ys: ys_train1, batch_size: train_batch_size})
            ###################################################################
            # Augment the training data every epoch, 
            # and do it with another process to save time.
            np.random.shuffle(rnd_samples)
            xs_train, ys_train = xs_train[rnd_samples], ys_train[rnd_samples]
            
            pool = Pool(1)
            result = pool.apply_async(util.batch_parse, (xs_train, ys_train, True, mixup_alpha, autoAugment, classes))
            pool.close()
            
            for i in range(train_batches):
                # cosine learning rate decay without restart
                # If the training epoch doesn't start from 0, you can set the offset of the cosine function.
                lr_batch = 0.5 * init_lr * (1 + np.cos(np.pi * (e * train_batches + i) / (epochs * train_batches)))
                batch_time = time.time()
                _, loss_i, err_i = sess.run([train_op, tower_loss, tower_error], feed_dict={train_flag: True, lr: lr_batch, batch_size: train_batch_size})
                train_losses[e] += loss_i
                train_err[e] += err_i
                
                sys.stdout.write('Epoch {}: {} / {} batches.  Error: {:.2f}  Loss: {:.3f}  {:.2f}s   '.format(
                                    e+1, i+1, train_batches, err_i, loss_i, time.time()-batch_time) + '\r')
                sys.stdout.flush()
                
            train_losses[e] /= train_batches
            train_err[e] /= train_batches
            print('')
            print('Epoch {}: Train_loss = {:.3f}, Train_err = {:.2f}'.format(e+1, train_losses[e], train_err[e]))
            
            pool.join()
            a, b = result.get()
            xs_train1, ys_train1 = np.stack(a), np.stack(b)
            del (pool, result, a, b)
            
            """
            -------------------------------------------------------------------
            Validation stage.
            -------------------------------------------------------------------
            """
            val_time = time.time()
            sess.run(data_loader_initializer, feed_dict={xs: xs_val, ys: ys_val, batch_size: val_batch_size})
            for i in range(val_batches):
                loss_val_i, err_val_i = sess.run([tower_loss, tower_error], feed_dict={train_flag: False, batch_size: val_batch_size})
                val_err[e] += err_val_i
                val_losses[e] += loss_val_i
            val_losses[e] /= val_batches
            val_err[e] /= val_batches
            
            cur_time = time.time()
            h, m, s = util.parse_time(cur_time - begin)
            print('Epoch {}:   Val_loss = {:.3f},   Val_err = {:.2f}  ({} samples)  {:.2f}s   '.format(
                                        e+1, val_losses[e], val_err[e], val_size, cur_time-val_time))
            print('Global time has passed {:.0f}:{:.0f}:{:.0f}'.format(h, m, s))
            print('')
            
            # Make a checkpoint.
            util.save_epoch_result('new_train_result', e, train_losses[e], train_err[e], val_losses[e], val_err[e])
            if val_err[e] < best_val:
                best_val = val_err[e]
                saver.save(sess, 'new_ckpt/model', global_step=e+1, write_meta_graph=True)
        
        # Make a final checkpoint.
        saver.save(sess, 'new_ckpt/model-final', write_meta_graph=True)
        print('Training time: {:.2f}'.format(time.time() - begin))
        util.plot_training_result('new_train_result', train_losses, train_err, val_losses, val_err)
        
    del(xs_train1, xs_val, xs_train)
    test_loss, test_err = util.test('new_ckpt/model-final.meta', 'new_ckpt/model-final', xs_test, ys_test, val_batch_size, classes)
    f = open('new_train_result.txt', 'a')
    print('Test_loss = {:.3f},  Test_err = {:.2f}'.format(test_loss, test_err), file=f)
    f.close()




