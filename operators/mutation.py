import math
import random

from fitness import functions

def mutateSingle(rand, individual, precentage):
    if (precentage==0):
        return individual
    if (rand%precentage==0):
        step = random.uniform(0, 2.35)
        if (round(random.random()*100)%2==0):
            individual.x -= step
            individual.y -= step
        else:
            individual.x += step
            individual.y += step
        
    return individual

def mutate(population, precentage):
    for i in range(len(population)):
        rand = random.random() * 100
        rand = round(rand)
        individual =  mutateSingle(rand, population[i], precentage)
        functions.fitnessRosenbruck(individual)
        population[i] = individual
    
    return population