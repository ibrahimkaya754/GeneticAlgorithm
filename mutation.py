# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 09:10:58 2017

@author: SADMcan
"""

import random

def mutation(offspring,mutation_probability):
    row = len(offspring)
    col = len(offspring[0])
    for ii in range(row):
        for jj in range(col):
            probability = random.random()
            if probability<= mutation_probability:
                if offspring[ii][jj] == 0:
                    offspring[ii][jj] = 1
                else:
                    offspring[ii][jj] = 0
    return offspring
            