# -*- coding: utf-8 -*-

from __future__ import division
import ImageOperation as ImOps
import numpy as np
            
ops = {'ShearX': ImOps.shearX,          'ShearY': ImOps.shearY, 
       'TranslateX': ImOps.translateX,  'TranslateY': ImOps.translateY, 
       'Rotate': ImOps.rotate,          'Solarize': ImOps.solarize, 
       'Posterize': ImOps.posterize,    'Contrast': ImOps.contrast,
       'Color': ImOps.color,            'Brightness': ImOps.brightness, 
       'Sharpness': ImOps.sharpness,    'Cutout': ImOps.cutout, 
       'AutoContrast': ImOps.autoContrast, 
       'Invert': ImOps.invert,          'Equalize': ImOps.equalize}
           
rangeMag = {'ShearX': [-0.3, 0.3],      'ShearY': [-0.3, 0.3], 
            'TranslateX': [-10, 10],  'TranslateY': [-10, 10], 
            'Rotate': [-30, 30],        'Solarize': [0, 256], 
            'Posterize': [4, 8],        'Contrast': [0.1, 1.9],
            'Color': [0.1, 1.9],        'Brightness': [0.1, 1.9], 
            'Sharpness': [0.1, 1.9],    'Cutout': [0, 20], 
            'AutoContrast': [0, 0],     'Invert': [0, 0],   'Equalize': [0, 0]}
            
intMag = { 'ShearX': False,         'ShearY': False, 
           'TranslateX': True,      'TranslateY': True, 
           'Rotate': False,         'Solarize': True, 
           'Posterize': True,       'Contrast': False,
           'Color': False,          'Brightness': False, 
           'Sharpness': False,      'Cutout': True, 
           'AutoContrast': False, 
           'Invert': False,         'Equalize': False}

exp0_0 = [[('Invert', 0.1, 7),          ('Contrast', 0.2, 6)],
          [('Rotate', 0.7, 2),          ('TranslateX', 0.3, 9)],
          [('Sharpness', 0.8, 1),       ('Sharpness', 0.9, 3)],
          [('ShearY', 0.5, 8),          ('TranslateY', 0.7, 9)],
          [('AutoContrast', 0.5, 8),    ('Equalize', 0.9, 2)]]
          
exp0_1 = [[('Solarize', 0.4, 5),        ('AutoContrast', 0.9, 3)],
          [('TranslateY', 0.9, 9),      ('TranslateY', 0.7, 9)],
          [('AutoContrast', 0.9, 2),    ('Solarize', 0.8, 3)],
          [('Equalize', 0.8, 8),        ('Invert', 0.1, 3)],
          [('TranslateY', 0.7, 9),      ('AutoContrast', 0.9, 1)]]
          
exp0_2 = [[('Solarize', 0.4, 5),        ('AutoContrast', 0.0, 2)],
          [('TranslateY', 0.7, 9),      ('TranslateY', 0.7, 9)],
          [('AutoContrast', 0.9, 0),    ('Solarize', 0.4, 3)],
          [('Equalize', 0.7, 5),        ('Invert', 0.1, 3)],
          [('TranslateY', 0.7, 9),      ('TranslateY', 0.7, 9)]]
          
exp0_3 = [[('Solarize', 0.4, 5),        ('AutoContrast', 0.9, 1)],
          [('TranslateY', 0.8, 9),      ('TranslateY', 0.9, 9)],
          [('AutoContrast', 0.8, 0),    ('TranslateY', 0.7, 9)],
          [('TranslateY', 0.2, 7),      ('Color', 0.9, 6)],
          [('Equalize', 0.7, 6),        ('Color', 0.4, 9)]]

exp1_0 = [[('ShearY', 0.2, 7),          ('Posterize', 0.3, 7)],
          [('Color', 0.4, 3),           ('Brightness', 0.6, 7)],
          [('Sharpness', 0.3, 9),       ('Brightness', 0.7, 9)],
          [('Equalize', 0.6, 5),        ('Equalize', 0.5, 1)],
          [('Contrast', 0.6, 7),        ('Sharpness', 0.6, 5)]]

exp1_1 = [[('Brightness', 0.3, 7),      ('AutoContrast', 0.5, 8)],
          [('AutoContrast', 0.9, 4),    ('AutoContrast', 0.5, 6)],
          [('Solarize', 0.3, 5),        ('Equalize', 0.6, 5)],
          [('TranslateY', 0.2, 4),      ('Sharpness', 0.3, 3)],
          [('Brightness', 0.0, 8),      ('Color', 0.8, 8)]]

exp1_2 = [[('Solarize', 0.2, 6),        ('Color', 0.8, 6)],
          [('Solarize', 0.2, 6),        ('AutoContrast', 0.8, 1)],
          [('Solarize', 0.4, 1),        ('Equalize', 0.6, 5)],
          [('Brightness', 0.0, 0),      ('Solarize', 0.5, 2)],
          [('AutoContrast', 0.9, 5),    ('Brightness', 0.5, 3)]]

exp1_3 = [[('Contrast', 0.7, 5),        ('Brightness', 0.0, 2)],
          [('Solarize', 0.2, 8),        ('Solarize', 0.1, 5)],
          [('Contrast', 0.5, 1),        ('TranslateY', 0.2, 9)],
          [('AutoContrast', 0.6, 5),    ('TranslateY', 0.0, 9)],
          [('AutoContrast', 0.9, 4),    ('Equalize', 0.8, 4)]]

exp1_4 = [[('Brightness', 0.0, 7),      ('Equalize', 0.4, 7)],
          [('Solarize', 0.2, 5),        ('Equalize', 0.7, 5)],
          [('Equalize', 0.6, 8),        ('Color', 0.6, 2)],
          [('Color', 0.3, 7),           ('Color', 0.2, 4)],
          [('AutoContrast', 0.5, 2),    ('Solarize', 0.7, 2)]]

exp1_5 = [[('AutoContrast', 0.2, 0),    ('Equalize', 0.1, 0)],
          [('ShearY', 0.6, 5),          ('Equalize', 0.6, 5)],
          [('Brightness', 0.9, 3),      ('AutoContrast', 0.4, 1)],
          [('Equalize', 0.8, 8),        ('Equalize', 0.7, 7)],
          [('Equalize', 0.7, 7),        ('Solarize', 0.5, 0)]]

exp1_6 = [[('Equalize', 0.8, 4),        ('TranslateY', 0.8, 9)],
          [('TranslateY', 0.8, 9),      ('TranslateY', 0.6, 9)],
          [('TranslateY', 0.9, 0),      ('TranslateY', 0.5, 9)],
          [('AutoContrast', 0.5, 3),    ('Solarize', 0.3, 4)],
          [('Solarize', 0.5, 3),        ('Equalize', 0.4, 4)]]

exp2_0 = [[('Color', 0.7, 7),           ('TranslateX', 0.5, 8)],
          [('Equalize', 0.3, 7),        ('AutoContrast', 0.4, 8)],
          [('TranslateY', 0.4, 3),      ('Sharpness', 0.2, 6)],
          [('Brightness', 0.9, 6),      ('Color', 0.2, 8)],
          [('Solarize', 0.5, 2),        ('Invert', 0.0, 3)]]

exp2_1 = [[('AutoContrast', 0.1, 5),    ('Brightness', 0.0, 0)],
          [('Cutout', 0.2, 4),          ('Equalize', 0.1, 1)],
          [('Equalize', 0.7, 7),        ('AutoContrast', 0.6, 4)],
          [('Color', 0.1, 8),           ('ShearY', 0.2, 3)],
          [('ShearY', 0.4, 2),          ('Rotate', 0.7, 0)]]

exp2_2 = [[('ShearY', 0.1, 3),          ('AutoContrast', 0.9, 5)],
          [('TranslateY', 0.3, 6),      ('Cutout', 0.3, 3)],
          [('Equalize', 0.5, 0),        ('Solarize', 0.6, 6)],
          [('AutoContrast', 0.3, 5),    ('Rotate', 0.2, 7)],
          [('Equalize', 0.8, 2),        ('Invert', 0.4, 0)]]

exp2_3 = [[('Equalize', 0.9, 5),        ('Color', 0.7, 0)],
          [('Equalize', 0.1, 1),        ('ShearY', 0.1, 3)],
          [('AutoContrast', 0.7, 3),    ('Equalize', 0.7, 0)], 
          [('Brightness', 0.5, 1),      ('Contrast', 0.1, 7)],
          [('Contrast', 0.1, 4),        ('Solarize', 0.6, 5)]]

exp2_4 = [[('Solarize', 0.2, 3),        ('ShearX', 0.0, 0)],
          [('TranslateX', 0.3, 0),      ('TranslateX', 0.6, 0)],
          [('Equalize', 0.5, 9),        ('TranslateY', 0.6, 7)],
          [('ShearX', 0.1, 0),          ('Sharpness', 0.5, 1)],
          [('Equalize', 0.8, 6),        ('Invert', 0.3, 6)]]

exp2_5 = [[('AutoContrast', 0.3, 9),    ('Cutout', 0.5, 3)],
          [('ShearX', 0.4, 4),          ('AutoContrast', 0.9, 2)],
          [('ShearX', 0.0, 3),          ('Posterize', 0.0, 3)],
          [('Solarize', 0.4, 3),        ('Color', 0.2, 4)],
          [('Equalize', 0.1, 4),        ('Equalize', 0.7, 6)]]

exp2_6 = [[('Equalize', 0.3, 8),        ('AutoContrast', 0.4, 3)],
          [('Solarize', 0.6, 4),        ('AutoContrast', 0.7, 6)],
          [('AutoContrast', 0.2, 9),    ('Brightness', 0.4, 8)],
          [('Equalize', 0.1, 0),        ('Equalize', 0.0, 6)],
          [('Equalize', 0.8, 4),        ('Equalize', 0.0, 4)]]

exp2_7 = [[('Equalize', 0.5, 5),        ('AutoContrast', 0.1, 2)],
          [('Solarize', 0.5, 5),        ('AutoContrast', 0.9, 5)],
          [('AutoContrast', 0.6, 1),    ('AutoContrast', 0.7, 8)],
          [('Equalize', 0.2, 0),        ('AutoContrast', 0.1, 2)],
          [('Equalize', 0.6, 9),        ('Equalize', 0.4, 4)]]
          
exp3_0 = [[('Equalize', 0.2, 0),        ('AutoContrast', 0.6, 0)],
          [('Equalize', 0.2, 8),        ('Equalize', 0.6, 4)],
          [('Color', 0.9, 9),           ('Equalize', 0.6, 6)],
          [('AutoContrast', 0.8, 4),    ('Solarize', 0.2, 8)],
          [('Brightness', 0.1, 3),      ('Color', 0.7, 0)]]

'''
# presented in google's open-source code
exp0s = exp0_0 + exp0_1 + exp0_2 + exp0_3
exp1s = exp1_0 + exp1_1 + exp1_2 + exp1_3 + exp1_4 + exp1_5 + exp1_6
exp2s = exp2_0 + exp2_1 + exp2_2 + exp2_3 + exp2_4 + exp2_5 + exp2_6 + exp2_7
policys = exp0s + exp1s + exp2s
'''
# policys in the paper
policys = exp0_0 + exp0_1 + exp1_0 + exp2_0 + exp3_0

def D2A(rangeA, digit, toInt=False):
    analog = digit * (rangeA[1] - rangeA[0]) / 10.0 + rangeA[0]
    if toInt == True:
        analog = int(analog)
    return analog

def ImOperation(img, (ImOp, prob, mag)):
    mag = D2A(rangeMag[ImOp], mag, intMag[ImOp])
    rnd = np.random.uniform()
    if rnd <= prob and prob > 0.0:
        img = ops[ImOp](img, mag)
    return img
    
def policy(img):
    policy_id = np.random.choice(len(policys))
    img = ImOperation(img, policys[policy_id][0])
    img = ImOperation(img, policys[policy_id][1])
    return img
    
    
    
    
    
    
