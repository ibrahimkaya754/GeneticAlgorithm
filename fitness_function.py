# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 13:16:08 2017

@author: SADMcan
"""
import test_functions
#import kerasTF_v1
#from keras import backend as K
#import tensorflow as tf
import numpy as np

def fitness_function(params):
    out = test_functions.egg(params)
    return out
    