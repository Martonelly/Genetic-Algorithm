import math
import random

def mutateSingle(rand, individual):
    if (rand%5==0):
        if (round(random.random()*100)%2==0):
            individual.x -= 2.35
            individual.y -= 2.25
        else:
            individual.x += 2.35
            individual.y += 2.25
        
    return individual

def mutate(population):
    for i in range(len(population)):
        rand = random.random() * 100
        rand = round(rand)
        individual =  mutateSingle(rand, population[i])
        population[i] = individual
    return population