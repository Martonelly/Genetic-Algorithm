

import random

from fitness import functions
from model import Chromosome
# at the crossover there should be
# strictly bellow the number
# strictly above the number
# strictly between the number (current)
def crossover(population):
    tempPopulation = []
    for j in range(len(population)):
        rand = random.randint(0, len(population)-1)
        # if (j == len(population)-1):
        #     newX = population[j].x*0.45 + population[rand].x*0.55
        #     newY = population[j].y*0.45 + population[rand].y*0.55
        # else:
            # newX = population[j].x*0.45 + population[j+1].x*0.55
            # newY = population[j].y*0.45 + population[j+1].y*0.55
        #add a twist so that 10% chance is that we just switch the x of one and the y of the other
        if (rand%10 == 0):
            if (rand%2==0):
                newX = population[j].x
                newY = population[rand].y
            else:
                newX = population[rand].x
                newY = population[j].y
        else:
            newX = population[j].x*random.uniform(0.0, 1.0) + population[rand].x*random.uniform(0.0, 1.0)
            newY = population[j].y*random.uniform(0.0, 1.0) + population[rand].y*random.uniform(0.0, 1.0)

        tempChromosome = Chromosome.C(newX, newY)
        #calculate the fitness
        functions.simple(tempChromosome)
        tempPopulation.append(tempChromosome)

    return tempPopulation