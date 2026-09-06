import copy

import numpy.random as npr

def selectOneRanked(rankedList):
    rankedSum = sum(rankedList)
    selectProbs = []
    for i in range(len(rankedList)):
        selectProbs.append(rankedList[i]/rankedSum)
    index = npr.choice(len(rankedList), p=selectProbs)
    return index

def select(population, number):
   
    retPopulation = []
    # we need to add some sort of elitism --> like 10 precent of the best fitness
    tempLen = len(population) / 30
    tempLen = round(tempLen) 
    # shold leave the best --> if possible switch this with a function 
    
    for i in range(tempLen):
        retPopulation.append(population[i])
    # now fill the remaining population with the "Random" selections but we need to rank them
    # add the temp so the smallest will become the biggest fitness
    temp = abs(population[len(population)-1].fitness) + 1
        
    popTemp = copy.deepcopy(population)
    for i in range(len(population)):
        popTemp[i].fitness += temp
    # best should be of higher rank, so we just reverse the list
    popTemp.reverse()
    population.reverse()

    #We need the formula:
    #individual value: minFitness + (maxFitness-minFitness)*(((individualRank)-1)/maxFitness-1)
    #we do this here --> after that RankList is complete we just use the RW selection 

    rankedList=[]

    for i in range(len(popTemp)):
        RankNum = popTemp[0].fitness + (popTemp[len(popTemp)-1].fitness-popTemp[0].fitness)*(((i+1)-1)/(len(popTemp)-1))
        rankedList.append(RankNum)
    #now the list is filled with values --> use the RW formula for these new values
    
    #print(rankedList)
    if (number == 0):
        for i in range(tempLen-1, len(population)):
            index = selectOneRanked(rankedList)
            retPopulation.append(population[index])
    #for steady state
    else:
        for i in range(number):
            index = selectOneRanked(rankedList)
            retPopulation.append(population[index])
    population.reverse()
    return retPopulation
    
