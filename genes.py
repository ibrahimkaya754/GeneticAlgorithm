# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 16:13:01 2017

@author: SADMcan
"""
import random
class birey:
    def __init__(self,bitno,gene_no,decoding_matrix,lower_boundary,upper_boundary):
        bitt = []
        for ii in range(bitno*gene_no):
            bitt.insert(ii,random.random())
            if bitt[ii]<0.5:
                bitt[ii] = 0
            else:
                bitt[ii] = 1
        self.bit = bitt
        self.bitno = bitno
        self.gene_no = gene_no
        self.decoding_matrix = decoding_matrix
        self.lower_boundary = lower_boundary
        self.upper_boundary = upper_boundary
        self.total_decoded_value = []
        self.normalized_decoded_value = []        
        for jj in range(gene_no):
            self.total_decoded_value[jj] = self.total_decoded_value.append(None)
            self.normalized_decoded_value[jj] = self.normalized_decoded_value.append(None)

    def binary_encoding(self):
        return self.bit
        
    def decoding_oper(self): 
        decoded_array = []
        for jj in range(self.gene_no):
            toplam = 0
            for kk in range(self.bitno):
                gen_no = jj
                bit_no = kk
                decoded_value = self.bit[bit_no+gen_no*self.bitno] * self.decoding_matrix[bit_no]
                decoded_array.insert(bit_no+gen_no*self.bitno,decoded_value)
                toplam = toplam + decoded_value
            self.total_decoded_value[jj] = toplam                
        return self.total_decoded_value
    
    def normalization(self):            
        for jj in range(self.gene_no):  
            normalized_value = self.lower_boundary[jj] + self.total_decoded_value[jj] * (self.upper_boundary[jj]-self.lower_boundary[jj]) / (2**self.bitno-1)
            self.normalized_decoded_value[jj] = normalized_value
        return self.normalized_decoded_value
    
    def birey_update(self,list_birey_encoded_yeni):
        col  = len(list_birey_encoded_yeni)
        bitt = []
        for ii in range(col):
            bitt.insert(ii,list_birey_encoded_yeni[ii])
        self.bit = bitt
        self.total_decoded_value = []
        self.normalized_decoded_value = []        
        for jj in range(self.gene_no):
            self.total_decoded_value[jj] = self.total_decoded_value.append(None)
            self.normalized_decoded_value[jj] = self.normalized_decoded_value.append(None)
#        return self.bit
            
        
        
        

#for jj in range(population_size):
#     decoded = []
#     for ss in range(number_of_genes):        
#         for ff in range(number_of_bits):
#             gen_no = ss
#             decoded_value = x_encoded[jj][ff + gen_no*number_of_bits] * decoding_matrix[ff]
#             decoded.insert(ff+gen_no*number_of_bits,decoded_value)  
#             toplam = toplam + decoded_value
#         total.insert(ss,toplam)
#         toplam = 0    
#     decoded_array.insert(jj,decoded)
#     x_decoded.insert(jj,total)  
#     #normalized_value = lower_boundaries[ss] + x_decoded[jj][ss] * (upper_boundaries[ss]-lower_boundaries[ss]) / (2**number_of_bits-1)
#     #x_decoded_normalized.insert(jj,normalized_value)
#     total = []
#     