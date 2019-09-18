# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 13:18:52 2017

@author: SADMcan
"""
import random
import math
import genes

def migration(birey,list_birey_encoded,fitness_values,migration_probability,objective_number,bitno,gene_no,remainder,best_encoded_ever):
    if remainder == 1:
        migration_probability = migration_probability * 10
        
    random_number    = random.random()
    if random_number <= migration_probability:
        sorted_fitness      = sorted(fitness_values,reverse=True)
        population_size     = len(fitness_values)
        migration_number    = 2 * math.ceil(migration_probability*population_size + objective_number)
        worst_indices       = []
        bitt                = [] 
        migration_existence = 1
        for jj in range(migration_number-1):        
            worst_indeks = [i for i, j in enumerate(fitness_values) if j==sorted_fitness[jj]]
            worst_indices.append(worst_indeks)
            for ii in range(bitno*gene_no):
                bitt.insert(ii,random.random())
                if bitt[ii]<0.5:
                    bitt[ii] = 0
                else:
                    bitt[ii] = 1        
            birey[worst_indeks[0]].birey_update(bitt)
            list_birey_encoded[worst_indeks[0]] = birey[worst_indeks[0]].binary_encoding()
        for jj in range(migration_number-1,migration_number):        
            worst_indeks = [i for i, j in enumerate(fitness_values) if j==sorted_fitness[jj]]
            worst_indices.append(worst_indeks)
            birey[worst_indeks[0]].birey_update(best_encoded_ever)
            list_birey_encoded[worst_indeks[0]] = birey[worst_indeks[0]].binary_encoding()
    else:
        migration_existence = 0
    return birey,list_birey_encoded,migration_existence
    
    