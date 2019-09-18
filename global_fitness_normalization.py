# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 16:47:39 2017

@author: SADMcan
"""
import math
def fitness_value_normalization(fitness_val,min_val,max_val):
    objective_number = len(min_val)    
    for ii in range(objective_number):
        minima = min_val[ii]
        maxima = max_val[ii]
    normalized_fitness = (fitness_val - minima) / (maxima - minima)
    return normalized_fitness

def fitness_value(normalized_fitness):
    return math.pow((1/100000),normalized_fitness)