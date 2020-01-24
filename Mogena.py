# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 13:17:58 2017

@author: SADMcan
"""

## MultiObjective Genetic Algorithm Code
## This code is converted to Class structure that can be imported from the environment for the upcoming projects

# CLEAR ALL
# get_ipython().magic('reset -sf')

# IMPORT MODULES
import genes
import input
import fitness_function
import selection
import crossover
import mutation
import output
import find_minmax
import global_fitness_normalization
import migration

class MoGenA():
    def __init__(self,number_of_variables, lower_boundaries, upper_boundaries,
                 number_of_generation=100,number_of_bits=30,population_size=100,
                 mutation_probability=0.01,use_saved_data=False,
                 objective_number=1,migration_probability=0.03,selection_type="roulette-wheel",
                 cross_over_probability=0.85,crossover_type="two-point",read_input_file=False):

        ###### READ THE INPUTS FROM FILE AND APPEND THEM TO THE VARIABLES #####
        if read_input_file:
            inp = input.read_input()
        #######################################################################
        
        ##################### Dictionaries ####################################
        dict_selection              = {'roulette-wheel'            :1,
                                       'roulette-wheel-tournament' :2}
        dict_crossover              = {'one-point' : 1, 
                                       'two-point' : 2}
        #######################################################################
        
        ################### Inputs ############################################
        self.iteration              = number_of_generation
        self.number_of_bits         = number_of_bits
        self.population_size        = population_size
        self.number_of_genes        = number_of_variables
        self.mutation_probability   = mutation_probability
        self.saved_data             = use_saved_data
        self.objective_number       = objective_number
        self.migration_probability  = migration_probability
        self.selection_type         = dict_selection[selection_type]
        self.cross_over_probability = cross_over_probability
        self.crossover_type         = dict_crossover[crossover_type]   
        self.lower_boundaries       = lower_boundaries
        self.upper_boundaries       = upper_boundaries
        #######################################################################
            
        ################### Binary Encoding ###################################
        decoding_array  = range(self.number_of_bits-1,-1,-1)
        decoding_matrix = []
        for ff in range(self.number_of_bits):
            decoding_matrix.insert(ff,2**decoding_array[ff])
        #######################################################################
            
        ################## Creating Population ################################ 
        individual                          = [] # individual listesi ilklendiriliyor
        list_individual_encoded             = [] # individual listesinin encoded hali ilklendiriliyor
        list_individual_decoded             = [] # individual listesinin decoded hali ilklendiriliyor
        list_individual_decoded_normalized  = [] # individual listesinin, her bir variable'ın alt üst sınırlarına göre normalize edildiği liste ilklendiriliyor
        list_fitness_values                 = [] # listedeki her individualin fitness değeri
        list_fitness_values_normalized      = [] # Fitness değerleri 0-1 aralığına normalize ediliyor
        list_global_fitness_values          = [] # Normalize edilmiş fitness değerleri, global fitness fonksiyouna sokuluyor
        list_individual_probability         = [] # Her individualin fitness değerine göre seçilme olasılığı // Her individualin fitness değeri. cumulative fitness değerine bölünür 
        list_cumulative_probability         = [] # Her individualin, cumulative probability'ye olan etkisi
        list_offspring                      = [] # Yeni oluşturulacak olan individualler
        list_selection_index                = [] # Selection operasyonuyla seçilen individuallerin indisi // Kontrol amaçlı tutuluyor.
        list_min_val                        = [] # Her bir objective için minimum değer ataması // Global fitness fonksiyonunda kullanılacak
        list_max_val                        = [] # Her bir objective için maksimum deer atamas1 // Global fitness fonksiyonunda kullan1lacak
        best_individual_decoded_ever        = [] # Best individual ever - decoded
        best_individual_encoded_ever        = [] # Best individual ever - encoded
        
        for jj in range(self.population_size): 
            individual[jj]                          = individual.append(None)
            list_individual_encoded[jj]             = list_individual_encoded.append(None)
            list_individual_decoded[jj]             = list_individual_decoded.append(None)
            list_individual_decoded_normalized[jj]  = list_individual_decoded_normalized.append(None)
            list_fitness_values[jj]                 = list_fitness_values.append(None)
            list_fitness_values_normalized[jj]      = list_fitness_values_normalized.append(None)
            list_global_fitness_values[jj]          = list_global_fitness_values.append(None)
            list_individual_probability[jj]         = list_individual_probability.append(None)
            list_cumulative_probability[jj]         = list_cumulative_probability.append(0)
            list_offspring[jj]                      = list_offspring.append(0)

        for j in range(int(self.population_size/2)):
            list_selection_index[j]            = list_selection_index.append(0)    
        #######################################################################

        ########### Every Individual is defined as Genes Class Object #########
        if self.saved_data == False:
            for jj in range(self.population_size): 
                individual[jj]              = genes.individual(number_of_bits,self.number_of_genes,decoding_matrix,self.lower_boundaries,self.upper_boundaries)
                list_individual_encoded[jj] = individual[jj].binary_encoding()
            for obj in range(self.objective_number):
                list_min_val.append(float(10000000000))
                list_max_val.append(float(-10000000000))
            for bb in range(self.number_of_genes):
                best_individual_decoded_ever.append(0)
            best_individual_encoded_ever = list_individual_encoded[0]
        elif self.saved_data == True:
            [list_individual_encoded_saved,list_min_val,list_max_val,best_individual_decoded_ever,best_individual_encoded_ever] = input.read_saved_data(self.population_size,objective_number)
            for jj in range(len(list_individual_decoded)):
                individual[jj]              = genes.individual(number_of_bits,self.number_of_genes,decoding_matrix,self.lower_boudaries,self.upper_boundaries)
                individual[jj].individual_update(list_individual_encoded_saved[jj])
                list_individual_encoded[jj] = individual[jj].binary_encoding()
            for jj in range(len(list_individual_decoded),self.population_size): 
                individual[jj]              = genes.individual(number_of_bits,self.number_of_genes,decoding_matrix,self.lower_boudaries,self.upper_boundaries)
                list_individual_encoded[jj] = individual[jj].binary_encoding() 
        #######################################################################

        ##################### Iterations ######################################
        generation    = 0
        while generation < self.iteration:
            total_fitness                  = 0
            cumulative_probability         = 0
            remainder                      = generation % 100
            # Decoding & Fitness function evalution
            for jj in range(self.population_size): 
                list_individual_decoded[jj]                                                                  = individual[jj].decoding_oper()
                list_individual_decoded_normalized[jj]                                                       = individual[jj].normalization()
                list_fitness_values[jj]                                                                 = fitness_function.fitness_function(list_individual_decoded_normalized[jj])
                [list_min_val,list_max_val,best_individual_encoded_ever,best_individual_decoded_ever]   = find_minmax.min_max_upgrade(list_fitness_values[jj],list_min_val,list_max_val,jj,list_individual_encoded,list_individual_decoded_normalized,best_individual_encoded_ever,best_individual_decoded_ever)  
            # Normalized fitness - Global fitness - Total fitness Calculation
            for jj in range(self.population_size):
                list_fitness_values_normalized[jj]  = global_fitness_normalization.fitness_value_normalization(list_fitness_values[jj],list_min_val,list_max_val)
                list_global_fitness_values[jj]      = global_fitness_normalization.fitness_value(list_fitness_values_normalized[jj])
                total_fitness                       = total_fitness + list_global_fitness_values[jj]
            # Individual & Cumulative Probability Calculation
            for jj in range(self.population_size):
                list_individual_probability[jj]     = list_global_fitness_values[jj]/total_fitness
                cumulative_probability              = cumulative_probability + list_individual_probability[jj]
                list_cumulative_probability[jj]     = cumulative_probability
            # Migration #   
            [individual,list_individual_encoded,mig_exist]    = migration.migration(individual,list_individual_encoded,list_fitness_values_normalized,self.migration_probability,self.objective_number,number_of_bits,self.number_of_genes,remainder,best_individual_encoded_ever)
            # Selection - Crossover - Mutation #
            for j in range(int(self.population_size/2)):
                [index1,index2]                     = selection.selectiontype(mig_exist,self.selection_type,self.number_of_genes,number_of_bits,list_cumulative_probability,list_individual_probability,population_size)
                list_selection_index[j]             = [index1,index2]
                [offspring1,offspring2]             = crossover.crossover_type(cross_over_probability,self.crossover_type,list_individual_encoded,self.number_of_genes,number_of_bits,index1,index2)
                [offspring1,offspring2]             = mutation.mutation([offspring1,offspring2],self.mutation_probability)
                list_offspring[2*j]                 = offspring1
                list_offspring[2*j+1]               = offspring2
            # Generation Update #
            for jj in range(self.population_size): 
                individual[jj].individual_update(list_offspring[jj])
                list_individual_encoded[jj]              = individual[jj].binary_encoding()
            print('generation = ', generation+1)    
            generation = generation + 1
            #Saving Data
            output.output(list_individual_encoded)
            output.min_max_saved(list_min_val,list_max_val,best_individual_decoded_ever,best_individual_encoded_ever)
        #######################################################################
        
        ################# Finding the Bests ###################################
        best_fitness                        = find_minmax.min_of_array(list_fitness_values)
        worst_fitness                       = find_minmax.max_of_array(list_fitness_values)
        best_fitness_index                  = [i for i, j in enumerate(list_fitness_values) if j==best_fitness]
        best_individual_decoded             = list_individual_decoded_normalized[best_fitness_index[0]]
        best_fitness_ever                   = list_min_val[0]
        #######################################################################
        
        #################### Saving Data ######################################
        output.output(list_individual_encoded)
        output.min_max_saved(list_min_val,list_max_val,best_individual_decoded_ever,best_individual_encoded_ever)
        #######################################################################        
            
            

            
