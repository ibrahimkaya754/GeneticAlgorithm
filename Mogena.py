"""
@author: ikaya

First, Created on Thu Mar  9 13:17:58 2017
## MultiObjective Genetic Algorithm Code
## This code is converted to Class structure that can be imported from the environment for the upcoming projects 
Modification began on 22/01/2020

"""
# IMPORT MODULES
from .genes import *
from .input import *
from .selection import *
from .crossover import *
from .mutation import *
from .output import *
from .find_minmax import *
from .global_fitness_normalization import *
from .migration import *
from .test_functions import *

class MoGenA():
    def __init__(self,number_of_variables, lower_boundaries, upper_boundaries,
                 number_of_generation=100,number_of_bits=30,population_size=100,
                 mutation_probability=0.01,use_saved_data=False,
                 objective_number=1,migration_probability=0.03,selection_type="roulette-wheel",
                 cross_over_probability=0.85,crossover_type="two-point",read_input_file=False,
                 fitness_func = 'griewank'):

        ###### READ THE INPUTS FROM FILE AND APPEND THEM TO THE VARIABLES #####
        if read_input_file:
            inp = read_input()
        #######################################################################
        
        ##################### Dictionaries ####################################
        dict_selection              = {'roulette-wheel'            :1,
                                       'roulette-wheel-tournament' :2}
        dict_crossover              = {'one-point' : 1, 
                                       'two-point' : 2}
        self.decoding_matrix        = []
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
        self.fitting_function       = fitness_func
        #######################################################################
        
        #################### Functions ########################################
        self.encoding()
        self.create_population()
        self.iterate()
        self.best_individual()
        self.save()
        #######################################################################
        
        ################### Binary Encoding ###################################
    def encoding(self):
        decoding_array  = range(self.number_of_bits-1,-1,-1)
        for ff in range(self.number_of_bits):
            self.decoding_matrix.insert(ff,2**decoding_array[ff])
        #######################################################################
        
        ################### Fitness Function ##################################
    def fitness_function(self,params):
        if self.fitting_function == 'griewank':
#            print('global test function "egg" will run')
            out = ackley(params)
        else:
            out = self.fitting_function(params)
        return out
        #######################################################################
        
        ################## Creating Population ################################ 
    def create_population(self):
        self.individual                          = [] # individual listesi ilklendiriliyor
        self.list_individual_encoded             = [] # individual listesinin encoded hali ilklendiriliyor
        self.list_individual_decoded             = [] # individual listesinin decoded hali ilklendiriliyor
        self.list_individual_decoded_normalized  = [] # individual listesinin, her bir variable'ın alt üst sınırlarına göre normalize edildiği liste ilklendiriliyor
        self.list_fitness_values                 = [] # listedeki her individualin fitness değeri
        self.list_fitness_values_normalized      = [] # Fitness değerleri 0-1 aralığına normalize ediliyor
        self.list_global_fitness_values          = [] # Normalize edilmiş fitness değerleri, global fitness fonksiyouna sokuluyor
        self.list_individual_probability         = [] # Her individualin fitness değerine göre seçilme olasılığı // Her individualin fitness değeri. cumulative fitness değerine bölünür 
        self.list_cumulative_probability         = [] # Her individualin, cumulative probability'ye olan etkisi
        self.list_offspring                      = [] # Yeni oluşturulacak olan individualler
        self.list_selection_index                = [] # Selection operasyonuyla seçilen individuallerin indisi // Kontrol amaçlı tutuluyor.
        self.list_min_val                        = [] # Her bir objective için minimum değer ataması // Global fitness fonksiyonunda kullanılacak
        self.list_max_val                        = [] # Her bir objective için maksimum deer atamas1 // Global fitness fonksiyonunda kullan1lacak
        self.best_individual_decoded_ever        = [] # Best individual ever - decoded
        self.best_individual_encoded_ever        = [] # Best individual ever - encoded
        
        for jj in range(self.population_size): 
            self.individual[jj]                          = self.individual.append(None)
            self.list_individual_encoded[jj]             = self.list_individual_encoded.append(None)
            self.list_individual_decoded[jj]             = self.list_individual_decoded.append(None)
            self.list_individual_decoded_normalized[jj]  = self.list_individual_decoded_normalized.append(None)
            self.list_fitness_values[jj]                 = self.list_fitness_values.append(None)
            self.list_fitness_values_normalized[jj]      = self.list_fitness_values_normalized.append(None)
            self.list_global_fitness_values[jj]          = self.list_global_fitness_values.append(None)
            self.list_individual_probability[jj]         = self.list_individual_probability.append(None)
            self.list_cumulative_probability[jj]         = self.list_cumulative_probability.append(0)
            self.list_offspring[jj]                      = self.list_offspring.append(0)

        for j in range(int(self.population_size/2)):
            self.list_selection_index[j]            = self.list_selection_index.append(0)    
        #######################################################################

        ########### Every Individual is defined as Genes Class Object #########
        if self.saved_data == False:
            for jj in range(self.population_size): 
                self.individual[jj]              = individual(self.number_of_bits,self.number_of_genes,self.decoding_matrix,self.lower_boundaries,self.upper_boundaries)
                self.list_individual_encoded[jj] = self.individual[jj].binary_encoding()
            for obj in range(self.objective_number):
                self.list_min_val.append(float(10000000000))
                self.list_max_val.append(float(-10000000000))
            for bb in range(self.number_of_genes):
                self.best_individual_decoded_ever.append(0)
            self.best_individual_encoded_ever = self.list_individual_encoded[0]
        elif self.saved_data == True:
            [list_individual_encoded_saved,self.list_min_val,self.list_max_val,self.best_individual_decoded_ever,self.best_individual_encoded_ever] = read_saved_data(self.population_size,self.objective_number)
            for jj in range(len(self.list_individual_decoded)):
                self.individual[jj]              = individual(self.number_of_bits,self.number_of_genes,self.decoding_matrix,self.lower_boundaries,self.upper_boundaries)
                self.individual[jj].individual_update(list_individual_encoded_saved[jj])
                self.list_individual_encoded[jj] = self.individual[jj].binary_encoding()
            for jj in range(len(self.list_individual_decoded),self.population_size): 
                self.individual[jj]              = individual(self.number_of_bits,self.number_of_genes,self.decoding_matrix,self.lower_boundaries,self.upper_boundaries)
                self.list_individual_encoded[jj] = self.individual[jj].binary_encoding() 
        #######################################################################

        ##################### Iterations ######################################
    def iterate(self):
        generation    = 0
        while generation < self.iteration:
            total_fitness                  = 0
            cumulative_probability         = 0
            remainder                      = generation % 100
            # Decoding & Fitness function evalution
            for jj in range(self.population_size): 
                self.list_individual_decoded[jj]                                                             = self.individual[jj].decoding_oper()
                self.list_individual_decoded_normalized[jj]                                                  = self.individual[jj].normalization()
                self.list_fitness_values[jj]                                                                 = self.fitness_function(self.list_individual_decoded_normalized[jj])
                [self.list_min_val,self.list_max_val,self.best_individual_encoded_ever,self.best_individual_decoded_ever]   = min_max_upgrade(self.list_fitness_values[jj],self.list_min_val,self.list_max_val,jj,self.list_individual_encoded,self.list_individual_decoded_normalized,self.best_individual_encoded_ever,self.best_individual_decoded_ever)  
            # Normalized fitness - Global fitness - Total fitness Calculation
            for jj in range(self.population_size):
                self.list_fitness_values_normalized[jj]  = fitness_value_normalization(self.list_fitness_values[jj],self.list_min_val,self.list_max_val)
                self.list_global_fitness_values[jj]      = fitness_value(self.list_fitness_values_normalized[jj])
                total_fitness                       = total_fitness + self.list_global_fitness_values[jj]
            # Individual & Cumulative Probability Calculation
            for jj in range(self.population_size):
                self.list_individual_probability[jj]     = self.list_global_fitness_values[jj]/total_fitness
                cumulative_probability              = cumulative_probability + self.list_individual_probability[jj]
                self.list_cumulative_probability[jj]     = cumulative_probability
            # Migration #   
            [self.individual,self.list_individual_encoded,mig_exist]    = migration(self.individual,self.list_individual_encoded,self.list_fitness_values_normalized,self.migration_probability,self.objective_number,self.number_of_bits,self.number_of_genes,remainder,self.best_individual_encoded_ever)
            # Selection - Crossover - Mutation #
            for j in range(int(self.population_size/2)):
                [index1,index2]                     = selectiontype(mig_exist,self.selection_type,self.number_of_genes,self.number_of_bits,self.list_cumulative_probability,self.list_individual_probability,self.population_size)
                self.list_selection_index[j]             = [index1,index2]
                [offspring1,offspring2]             = crossover_type(self.cross_over_probability,self.crossover_type,self.list_individual_encoded,self.number_of_genes,self.number_of_bits,index1,index2)
                [offspring1,offspring2]             = mutation([offspring1,offspring2],self.mutation_probability)
                self.list_offspring[2*j]                 = offspring1
                self.list_offspring[2*j+1]               = offspring2
            # Generation Update #
            for jj in range(self.population_size): 
                self.individual[jj].individual_update(self.list_offspring[jj])
                self.list_individual_encoded[jj]              = self.individual[jj].binary_encoding()
            print('generation = ', generation+1)    
            generation = generation + 1
            #Saving Data
            output(self.list_individual_encoded)
            min_max_saved(self.list_min_val,self.list_max_val,self.best_individual_decoded_ever,self.best_individual_encoded_ever)
        #######################################################################
        
        ################# Finding the Bests ###################################
    def best_individual(self):
        self.best_fitness                        = min_of_array(self.list_fitness_values)
        self.worst_fitness                       = max_of_array(self.list_fitness_values)
        self.best_fitness_index                  = [i for i, j in enumerate(self.list_fitness_values) if j==self.best_fitness]
        self.best_individual_decoded             = self.list_individual_decoded_normalized[self.best_fitness_index[0]]
        self.best_fitness_ever                   = self.list_min_val[0]
        #######################################################################
    
        #################### Saving Data ######################################
    def save(self):
        output(self.list_individual_encoded)
        min_max_saved(self.list_min_val,self.list_max_val,self.best_individual_decoded_ever,self.best_individual_encoded_ever)
        #######################################################################
