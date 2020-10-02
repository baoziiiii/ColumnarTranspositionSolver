from random import randint
from random import shuffle
from random import sample
from collections import defaultdict
import re
import datetime
import sys
from log import fprint
from blist import sortedlist


gram_score = {
    'EEE':-5,
    'E_': 2,
    '_T':1,
    'HE':1,
    'TH':1,
    '_A':1,
    '___':-10,
    'ING':5,
    'S_':1,
    '__':-6,
    '_TH':5,
    'THE':5,
    'HE_':5,
    'AND':5
}

class Individual:
    def __init__(self, crypt, key_length,  key = None):
        self.fitness = 0
        self.crypt = crypt
        self.key_length = key_length
        if key:
            self.key = key
        else:
            self.key = list(range(self.key_length))
            shuffle(self.key)
        self.calcFitness()


    def decrypt(self):
        crypt = list(self.crypt)
        plain = ['']*len(crypt)
        for i in range(len(crypt)//self.key_length):
            b = i * self.key_length 
            for j in range(self.key_length):
                plain[b+self.key[j]] = crypt[b + j]
        return "".join(plain)

    def calcFitness(self):
        self.fitness = 0
        plain = self.decrypt()
        length = len(plain)
        for i in range(length-1):
            bigram = plain[i]+plain[i+1]
            if bigram in gram_score:
                self.fitness += gram_score[bigram]
            if i < length - 2:
                tigram = bigram + plain[i+2]
                if tigram in gram_score:
                    self.fitness += gram_score[tigram]
        return self.fitness


class Population:
    def __init__(self, size, crypt, key_length):
        self.crypt = crypt
        self.key_length = key_length
        self.individuals = sortedlist([Individual(crypt, key_length) for i in range(size)],key = lambda x: x.fitness)
        self.individuals_dict = defaultdict(int)
        for individual in self.individuals:
            self.individuals_dict[tuple(individual.key)] += 1
        self.pop_size = size
        self.fittest = 0

    def get_fittest(self):
        return self.individuals[-1]

    def get_fittest_rand(self):
        r = -1*randint(0,2)
        max_fit = self.individuals[r]
        self.fittest = max_fit.fitness
        return max_fit

    def get_second_fittest_rand(self):
        r = -1*randint(3,5)
        return self.individuals[r]
    
    def get_least_fittest_index(self):
        return 0
    
    # def calculate_fitness(self):
    #     for individual in self.individuals:
    #         individual.calcFitness()
    #     self.individuals.sort(key=(lambda x:x.fitness))

    def replace(self, replace_index, replace, revive_threshold):
        rk = tuple(replace.key)
        if rk in self.individuals_dict:
            self.individuals_dict[rk] += 1
            self.revive(rk, revive_threshold)
            return
        del self.individuals_dict[tuple(self.individuals[replace_index].key)]
        del self.individuals[replace_index] 
        self.individuals.add(replace)
        self.individuals_dict[rk] += 1
    
    def revive(self, key, revive_threshold):
        if self.individuals_dict[key] > revive_threshold:
            for i, individual in enumerate(self.individuals):
                if tuple(individual.key) == key:
                    fprint("revive...")
                    new_key = list(range(self.key_length))
                    shuffle(new_key)
                    nc = Individual(self.crypt, self.key_length ,key = new_key)
                    nc.calcFitness()
                    self.replace(i, nc, revive_threshold)
                    return

class TranspositionGA:
    def __init__(self, crypt, key_length):
        self.crypt = crypt
        self.generationCount = 0
        self.key_length = key_length
        self.population = Population(1000, crypt, key_length)
        for i in range(self.population.pop_size):
            fprint(self.population.individuals[i].key)
        self.fittest = self.population.get_fittest_rand()
        self.secondFittest = self.population.get_second_fittest_rand()
        fprint("Generation: {} Fittest: {}".format(self.generationCount,self.population.fittest))

    def selection(self):
        self.fittest = self.population.get_fittest_rand()
        self.secondFittest = self.population.get_second_fittest_rand()


    def crossover(self, revive_threshold):
        P = self.key_length
        c1 = [0]*P 
        c2 = [0]*P
        p1 = self.fittest.key
        p2 = self.secondFittest.key
        tmp_set = set()

        r = randint(0,P-1)
        for i in range(r):
            c1[i] = p1[i]
            tmp_set.add(p1[i])
        i = 0
        k = 0
        while i < P - r and k < P:
            if p2[k] not in tmp_set:
                c1[i + r] = p2[k]
                tmp_set.add(p2[k])
                i += 1
            else:
                k += 1
        
        tmp_set.clear()
        
        r = randint(0,P-1)
        for i in range(P-1,r-1,-1):
            c2[i] = p1[i]
            tmp_set.add(p1[i])
        i = 1
        k = P-1
        while i <= r and k >= 0:
            if p2[k] not in tmp_set:
                c2[r - i] = p2[k]
                tmp_set.add(p2[k])
                i += 1
            else:
                k -= 1

        fprint("r:{}|p1:{}|p2:{}|c1:{}|c2:{}".format(r,p1,p2,c1,c2))

        r = randint(0,2)

        for i in range(r):
   # mutation
            swap =  sample(list(range(P)),2)
            c1[swap[0]],c1[swap[1]] = c1[swap[1]],c1[swap[0]]
            swap = sample(list(range(P)),2)
            c2[swap[0]],c2[swap[1]] = c2[swap[1]],c2[swap[0]]

        c_i1 = Individual(self.crypt, self.key_length , key = c1)
        c_i1.calcFitness()
        c_i2 = Individual(self.crypt, self.key_length , key = c2)
        c_i2.calcFitness()
    # get_fittest_offspring(self)
        c_i_max= max(c_i1, c_i2, key=(lambda x:x.fitness))

    #add_fittest_offspring(self)
        self.population.replace(self.population.get_least_fittest_index(),c_i_max, revive_threshold)

    def run(self, fitness_threshold, generation_limit):
        result = []
        while self.generationCount < generation_limit :
            self.generationCount += 1
            self.selection()
            self.crossover(generation_limit//500)
            fittest = self.population.get_fittest()
            if fittest.fitness >= fitness_threshold:
                if result and tuple(fittest.key) == tuple(result[-1][2]):
                    continue
                r = (fittest.decrypt(),fittest.fitness,fittest.key)
                result.append(r)
                fprint("Solution Found:\n{}\nFitness:{} Key:{}".format(r[0],r[1],r[2]))
                if input("\nIs this solution bingo? Enter b to break the program. Otherwise press Enter to continue searching...") == 'b':
                    return

            fprint("Generation: {} Fittest: {}".format(self.generationCount,self.population.fittest))
        
        if not result :
            fprint("Can't find solution")
        else:
            fprint("\n\nSolutions Found:{}")
            for i,r in enumerate(result):
                fprint("{}.\n{}\nFitness:{} Key:{}".format(i,r[0],r[1],r[2]))

