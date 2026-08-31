from model import Chromosome
from fitness import functions
from operators import rouletSelection, crossover, mutation
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
populationLen = 100
generationLen = 1000

population = []
best_scores = []
#initizalize
for i in range(populationLen):
    #initialize the chromosomes randomly
    temp = Chromosome.C(random.uniform(-100,100), random.uniform(-100,100))
    #this is the sphere function
    entity_fitness = functions.simple(temp)
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
    print("------------------BEST---------------")
    print(best_result)
    print("-------------------------------------")
    print(f"Population {i+1}: ")
    #print(population)
    if (flag):
        break
    #already sorted now there is only the selection and the opreators before the new loop
    #selection Roulet wheel selection 
    population = rouletSelection.select(population)
    
    #crossoverTest --> at 50% and thats it after we just swap the new pop for the old one
    population = crossover.crossover(population)

    #Mutation 
    population = mutation.mutate(population)

print(f"The x is: {population[0].x} the y is: {population[0].y}")
print("end")







# test1 =  Chromosome.C(2, 0)
# ##print(test1.fitness)
# entity_fitness = functions.fitnessRosenbruck(test1)
# #print(entity_fitness, " ", test1.fitness)



