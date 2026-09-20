import copy
import random


def selectOne(population, variable):
    parents = random.choices(population, k=variable)
    parents = sorted(parents, key=lambda agent: agent.fitness, reverse=True)
    best = parents[0]
    return best

def select(population, number, variable, elitism):

    retPopulation = []
    # we need to add some sort of elitism --> like 10 precent of the best fitness
    tempLen = len(population) / 100 * elitism
    tempLen = round(tempLen) 
    # shold leave the best --> if possible switch this with a function 
    
    # for i in range(tempLen):
    #     retPopulation.append(population[i])


    # temp = abs(population[len(population)-1].fitness) + 1

    # popTemp = copy.deepcopy(population)
    # for i in range(len(population)):
    #     popTemp[i].fitness += temp
    # best should be of higher rank, so we just reverse the list
    if(number == 0):
        for i in range(tempLen-1, len(population)):
            retPopulation.append(selectOne(population, variable))
    else:
        for i in range(number):
            retPopulation.append(selectOne(population, variable))

    return retPopulation
