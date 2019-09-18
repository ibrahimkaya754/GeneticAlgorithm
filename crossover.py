# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 17:01:19 2017

@author: SADMcan
"""

import random
import math

def crossover_type(cross_over_probability,choice,encoded_list,number_of_genes,number_of_bits,indice1,indice2):
    offspring1 = []
    offspring2 = []
    if choice == 1:
        offspring1,offspring2 = onepoint_crossover(cross_over_probability,encoded_list,number_of_genes,number_of_bits,indice1,indice2)
    elif choice == 2:
        offspring1,offspring2 = twopoint_crossover(cross_over_probability,encoded_list,number_of_genes,number_of_bits,indice1,indice2)
    return offspring1,offspring2
        

def onepoint_crossover(cross_over_probability,encoded_list,number_of_genes,number_of_bits,indice1,indice2):
    cop = random.random()
    offspring1 = []
    offspring2 = []  
    for ii in range(number_of_genes * number_of_bits):
        offspring1[ii] = offspring1.append(0)
        offspring2[ii] = offspring2.append(0)
    if cop <= cross_over_probability:
        random_number = round(random.random() * number_of_genes * number_of_bits)
        if random_number == 0:
            random_number = random_number + 1
        elif random_number == number_of_genes * number_of_bits:
            random_number = random_number - 1
        
#        offspring1 = []
#        offspring2 = []
#        
#        # Offspring'ler initialize ediliyor
#        for ii in range(number_of_genes * number_of_bits):
#            offspring1[ii] = offspring1.append(0)
#            offspring2[ii] = offspring2.append(0)
        
        # New Offspring1 and Offspring2
        for ii in range(number_of_genes * number_of_bits):
            if ii <= random_number:
                offspring1[ii] = encoded_list[indice1][ii]
                offspring2[ii] = encoded_list[indice2][ii]
            else:
                offspring1[ii] = encoded_list[indice2][ii]
                offspring2[ii] = encoded_list[indice1][ii]
    else:
        for ii in range(number_of_genes * number_of_bits):
            offspring1[ii] = encoded_list[indice1][ii]
            offspring2[ii] = encoded_list[indice2][ii]
    
    return offspring1,offspring2

def twopoint_crossover(cross_over_probability,encoded_list,number_of_genes,number_of_bits,indice1,indice2):
    cop = random.random()
    offspring1 = []
    offspring2 = []  
    for ii in range(number_of_genes * number_of_bits):
        offspring1[ii] = offspring1.append(0)
        offspring2[ii] = offspring2.append(0)
    if cop <= cross_over_probability:
        random_number1 = round(random.random() * number_of_genes * number_of_bits)
        if random_number1 == 0:
            random_number1 = random_number1 + 1
        elif random_number1 >= (number_of_genes * number_of_bits / 2):
            random_number1 = math.floor(random_number1/2)
        
        random_number2 = round(random.random() * number_of_genes * number_of_bits)
        if random_number2 <= random_number1:
            random_number2 = 2 * random_number1
        elif random_number2 == (number_of_genes * number_of_bits):
            random_number2 = random_number2 - 1
        
        # Offspring'ler initialize ediliyor
#        offspring1 = []
#        offspring2 = []  
#        for ii in range(number_of_genes * number_of_bits):
#            offspring1[ii] = offspring1.append(0)
#            offspring2[ii] = offspring2.append(0)
            
        # New Offspring1 and Offspring2
        for ii in range(number_of_genes * number_of_bits):
            if ii <= random_number1:
                offspring1[ii] = encoded_list[indice1][ii]
                offspring2[ii] = encoded_list[indice2][ii]
            elif ii > random_number1 and ii < random_number2:
                offspring1[ii] = encoded_list[indice2][ii]
                offspring2[ii] = encoded_list[indice1][ii]
            elif ii >= random_number2:
                offspring1[ii] = encoded_list[indice1][ii]
                offspring2[ii] = encoded_list[indice2][ii]
    else:
        for ii in range(number_of_genes * number_of_bits):
            offspring1[ii] = encoded_list[indice1][ii]
            offspring2[ii] = encoded_list[indice2][ii]
    return offspring1,offspring2
            
    