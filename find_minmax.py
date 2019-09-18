# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 14:14:18 2017

@author: SADMcan
"""

def min_func(x1,x2):
    if x1<=x2:
        min = x1
    else:
        min = x2
    return min

def max_func(x1,x2):
    if x1>=x2:
        max = x1
    else:
        max = x2
    return max

def min_max_upgrade(list_fitness_values,list_minimum,list_maximum,indice_of_element,list_encoded,list_decoded,best_individual_encoded,best_individual_decoded):
    objective_number = len(list_minimum)
    x1 = list_fitness_values
    for ii in range(objective_number):
        x2 = list_minimum[ii]
        x3 = list_maximum[ii]
        minimum = min_func(x1,x2)
        maximum = max_func(x1,x3)
        if minimum == x1:
            index                                             = indice_of_element
            [best_individual_encoded,best_individual_decoded] = best_individual(list_encoded,list_decoded,index)            
        list_minimum[ii] = minimum
        list_maximum[ii] = maximum
    return list_minimum,list_maximum,best_individual_encoded,best_individual_decoded
         
def min_of_array(liste):
    minima = 10000000000
    row = len(liste)
    for ii in range(row):
        minima = min_func(liste[ii],minima)
    return minima

def max_of_array(liste):
    maxima = -10000000000
    row = len(liste)
    for ii in range(row):
        maxima = max_func(liste[ii],maxima)
    return maxima

def best_individual(list_encoded,list_decoded,index):
    best_individual_encoded = list_encoded[index]
    best_individual_decoded = list_decoded[index]
    return best_individual_encoded,best_individual_decoded