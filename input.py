# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 16:49:47 2017

@author: SADMcan
"""

def read_input():
    inputfile = open('GA_input.txt')
    inp = inputfile.read()
    inputs = inp.split("\n")
    girdi = []
    counter = 0;
    for line in inputs:
        c1 = line
        c2 = c1.split()
        for ii in range(c2.index("=")+1,c2.index("%"),1):
            girdi.insert(counter,c2[ii])
            counter = counter + 1    
    inputfile.close
    return girdi
    
def read_saved_data(population_no,objective_no):
    # Kaydedilmiş bireyler okunuyor    
    inputfile  = open("saved_data.txt","r")
    inp        = inputfile.read()
    inputs     = inp.split("\n")    
    list_birey = []
    counter    = 0
    for line in inputs:
        girdi = []        
        c1    = line
        c2    = c1.split()
        col   = len(c2)        
        for ii in range(col):
            girdi.insert(ii,int(c2[ii]))
        if counter<population_no:
            list_birey.insert(counter,girdi)
        counter = counter + 1
    inputfile.close
    # Kaydedilmiş minmax değerleri okunuyor
    inputfile  = open("saved_min_max_data.txt","r")
    inp        = inputfile.read()
    inputs     = inp.split("\n") 
    minimum    = []
    maximum    = []
    best_decoded_ever = []
    best_encoded_ever = []
    counter    = 0
    for line in inputs:
        c1      = line
        c2      = c1.split()
        col     = len(c2)
        if counter < objective_no:
            minimum.insert(counter,float(c2[0]))
            maximum.insert(counter,float(c2[1]))
        elif counter == objective_no:
            for kk in range(col):
                best_decoded_ever.insert(kk,float(c2[kk]))
        else:
            for tt in range(col):
                best_encoded_ever.insert(tt,int(c2[tt]))
        counter = counter + 1
            
    return list_birey,minimum,maximum,best_decoded_ever,best_encoded_ever

