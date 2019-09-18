# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 16:08:48 2017

@author: SADMcan
"""
import random

def selectiontype(migration_existence,selection_choice,number_of_genes,number_of_bits,cumulative_probability,individual_probability,population_size):
    if migration_existence == 1:
        [index1,index2] = random_selection(population_size)
    else:
        if selection_choice == 1:
             [index1,index2] = roulette_wheel(cumulative_probability)
        elif selection_choice == 2:
             [index1,index2] = roulette_wheel_tournament_selection(cumulative_probability,individual_probability)
    return index1,index2

def roulette_wheel(cumulative_probability):    
    length = len(cumulative_probability)
    indice1 = 0
    indice2 = 0
    while indice1 == indice2:
        roulette_random_number = random.random()
        for ii in range(length):
            if cumulative_probability[ii] >= roulette_random_number :
                indice1 = ii
                break
        roulette_random_number = random.random() 
        for ii in range(length):
            if cumulative_probability[ii] >= roulette_random_number :
                indice2 = ii
                break
    return indice1,indice2

def roulette_wheel_tournament_selection(cumulative_probability,individual_probability):
    length = len(cumulative_probability)    
    indeks  = []
    for ii in range(2):
        indeks.append(0)    
    indice1 = 0
    indice2 = 0
    while indeks[0] == indeks[1]:
        for kk in range(2):
            random_number1 = random.random()
            for jj in range(length):
                if cumulative_probability[jj] >= random_number1:
                    indice1 = jj
                    indice2 = jj
                    break
            while indice1 == indice2:
                random_number2 = random.random()
                for jj in range(length):
                    if cumulative_probability[jj] >= random_number2:
                        indice2 = jj
                        break
            if individual_probability[indice1] > individual_probability[indice2]:
                indeks[kk] = indice1
            else:
                indeks[kk] = indice2
    
    return indice1,indice2            

def random_selection(population_size):
    random_number1 = 0
    random_number2 = 0
    while random_number1==random_number2:
        random_number1 = round(random.random() * population_size - 1)
        random_number2 = round(random.random() * population_size - 1)
    return random_number1,random_number2
            