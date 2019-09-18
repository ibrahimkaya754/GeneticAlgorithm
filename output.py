# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 15:20:02 2017

@author: SADMcan
"""

def output(list_birey_encoded):
    file = open("saved_data.txt","w")
    row = len(list_birey_encoded)
    col = len(list_birey_encoded[0])
    for ii in range(row):
        for jj in range(col):
            file.write("%d" % list_birey_encoded[ii][jj])
            file.write("  ")
        file.write('\n')
    file.close

def min_max_saved(list_min,list_max,best_individual_decoded_ever,best_individual_encoded_ever):
    file = open("saved_min_max_data.txt","w")
    row = len(list_min)    
    for ii in range(row):
        file.write("%.15f   %.15f" % (list_min[ii],list_max[ii]))
        file.write('\n')
    for jj in range(len(best_individual_decoded_ever)):
        file.write("%.15f" % (best_individual_decoded_ever[jj]))
        file.write("   ")
    file.write('\n')
    for kk in range(len(best_individual_encoded_ever)):
        file.write("%d" % best_individual_encoded_ever[kk])
        file.write("  ")
    file.write('\n')
    file.close