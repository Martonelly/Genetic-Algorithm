import numpy.random as npr
def selectOne(population):
    #just add the lowest fitness to all the values and that way there will be no negatives
    testSum = 0
    temp = abs(population[len(population)-1].fitness) + 1
    # for i in range(len(population)):
    #     testSum += population[i].fitness + temp
    fitnessSum = sum([c.fitness + temp for c in population])
    
    c =0
    selectProbs = [((c.fitness+ temp) / fitnessSum) for c in population]
    
    return population[npr.choice(len(population), p=selectProbs)]

def select(population):
    #print(population)
    retPopulation = []
    # we need to add some sort of elitism --> like 10 precent of the best fitness
    tempLen = len(population) / 30
    tempLen = round(tempLen) 
    # shold leave the best --> if possible switch this with a function 
    for i in range(tempLen):
        retPopulation.append(population[i])
    # now fill the remaining population with the "Random" selections

    for i in range(tempLen-1, len(population)):
       # print(f"The population number is: {i} \n")
        retPopulation.append(selectOne(population))
    # print("---------Newly Selected---------")
    # print(retPopulation)
    # print("--------------------------------")
    return retPopulation