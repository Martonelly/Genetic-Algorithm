import time

from model import Chromosome
from fitness import functions
from operators import rouletSelection, crossover, mutation, rankSelection, steadyStateSelection
import random

#we need the statrting genreations and the main algorithm
#1. Population initialization

#2. Fitness evaluation --> checking restrictions
#3. Evolution operators --> selection --> crossover and mutation 

#4. Replace population --> step 2

#Define
#Population
#Iteration
#Eta
populationLen = 20
generationLen = 600
steadySS = True
population = []
best_scores = []
#initizalize
start_time = time.time()
for i in range(populationLen):
    #initialize the chromosomes randomly
    temp = Chromosome.C(random.uniform(-10,10), random.uniform(-10,10))
    #this is the sphere function
    entity_fitness = functions.myFunction(temp)
    population.append(temp)

#algorithm
best_result = float('inf')
def sortFitness(val):
    return val.fitness
#check eta is 0.001 --> now between the last and the last minus 10 score
def checkNear():
    population.sort(key= sortFitness,reverse=True)
    if (len(best_scores)<=100):
        return False
    if ( abs(best_result-best_scores[len(best_scores)-10]) > 0.00001 and abs(best_result-best_scores[len(best_scores)-20]) > 0.00001 and abs(best_result-best_scores[len(best_scores)-30]) > 0.00001):
        return False
    else:
        return True

i = 0
for i in range(generationLen):
    #flag and the best values
    flag = checkNear()
    best_result = population[0].fitness
    best_scores.append(best_result)
    # print("------------------BEST---------------")
    # print(best_result)
    # print("-------------------------------------")
    # print(f"Population {i+1}: ")
    #print(population)
    if (flag):
        break
    #already sorted now there is only the selection and the opreators before the new loop
    #selection Roulet wheel selection 
    #Here we replace the worst of the chromosomes with the best from the previous generation
    if (steadySS):
        offspring = []
        #should be changed to selections
        # for i in range(round(len(population)/10)):
        #     offspring.append(population[i])
        #SELECTION
        #offspring = rouletSelection.select(population,round(len(population)/10))
        offspring = rankSelection.select(population, round(len(population)/10))
        offspring = crossover.crossover(offspring)
        #Mutation 
        offspring = mutation.mutate(offspring)
        for i in range(len(offspring)):
             if(population[len(population)-1-i].fitness < offspring[i].fitness):
                population[len(population)-1-i] = offspring[i]
    else:   
        #SELECTIONS
        #population = rouletSelection.select(population, 0)
        population = rankSelection.select(population)
        #crossoverTest --> at 50% and thats it after we just swap the new pop for the old one
        population = crossover.crossover(population)

        #Mutation 
        population = mutation.mutate(population)

print(f"The x is: {population[0].x} the y is: {population[0].y} FITNESS: {population[0].fitness}")
solution_time = time.time() - start_time
print(f"Time needed is: {solution_time}")
print("end")







# test1 =  Chromosome.C(2, 0)
# ##print(test1.fitness)
# entity_fitness = functions.fitnessRosenbruck(test1)
# #print(entity_fitness, " ", test1.fitness)



