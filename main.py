import time
from openpyxl import Workbook
from model import Chromosome
from fitness import functions
from operators import rouletSelection, crossover, mutation, rankSelection, steadyStateSelection, tournamentSelection
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
elitism_range = range(0, 30, 10)
population_range = range(20, 60, 10)
generation_range = range(200, 800, 50)
resRound = 0
# populationLen = 20
# generationLen = 600
steadySS = False
somethingCNT = 0
population = []
best_scores = []
#initizalize
def init(populationLen):
    for i in range(populationLen):
        #initialize the chromosomes randomly
        temp = Chromosome.C(random.uniform(-10,10), random.uniform(-10,10))
        #this is the sphere function
        entity_fitness = functions.fitnessRosenbruck(temp)
        population.append(temp)


def sortFitness(val):
    return val.fitness

def sortResult(val):
    return val[5]
#check eta is 0.001 --> now between the last and the last minus 10 score
def checkNear():
    population.sort(key= sortFitness,reverse=True)
    if (len(best_scores)<=200):
        return False
    if ( abs(best_result-best_scores[len(best_scores)-10]) > 0.00001 and abs(best_result-best_scores[len(best_scores)-20]) > 0.00001 and abs(best_result-best_scores[len(best_scores)-30]) > 0.00001):
        return False
    else:
        return True

i = 0
for sel in range(2):
    if (sel == 0):
        results = []
        for selType in range(3):
            for k in elitism_range:
                
                for p in population_range:
                        for g in generation_range:
                            population = []
                            best_scores = []
                            init(p)
                            best_result = float('inf')
                            start_time = time.time()    
                            for i in range(g):
                                population.sort(key=sortFitness, reverse=True)
                                #flag and the best values
                                flag = checkNear()
                                best_result = population[0].fitness
                                best_scores.append(best_result)
                                
                                if (flag):
                                    break
                                #already sorted now there is only the selection and the opreators before the new loop
                                #selection Roulet wheel selection 
                                #SELECTIONS
                                if (selType==0):
                                    population = rouletSelection.select(population, 0, k)
                                elif(selType==1):
                                    population = rankSelection.select(population, 0, k)
                                elif(selType==2):
                                    population = tournamentSelection.select(population, 0, 4, k)
                                #crossoverTest --> at 50% and thats it after we just swap the new pop for the old one
                                population = crossover.crossover(population)

                                #Mutation 
                                population = mutation.mutate(population)
                            #final sort
                            population.sort(key=sortFitness, reverse=True)
                            #print(f"The x is: {population[0].x} the y is: {population[0].y} FITNESS: {population[0].fitness}")
                            solution_time = time.time() - start_time
                            best = population[0]
                            results.append([p, g, solution_time, best.x, best.y, best.fitness, k])
                            somethingCNT += 1
                            print(f"Something {somethingCNT}")
                somethingCNT = 0
                resRound += 1
                print(f"Progress NOT STEADY: {resRound}")
            results.sort(key=sortResult, reverse=True)
            #Extract it
            wb = Workbook()
            ws = wb.active
            
            #ws.title = "Steady State Test"

            headers = ["Population", "Generation", "Time (s)", "X", "Y", "Fitness", "Elitism"]

            ws.append(headers)

            for result in results:
                ws.append(result)

            for column in ws.columns:
                max_length = 0

                for cell in column:
                    if (cell.value is not None):
                        max_length = max(max_length, len(str(cell.value)))

                ws.column_dimensions[column[0].column_letter].width = max_length+2

            

            if (selType==0):
                ws.title = "Steady State Test Roulet Wheel"
                wb.save("GA_Normal_RouletWheel.xlsx")

            elif(selType==1):
                ws.title = "Steady State Test Rank Selection"
                wb.save("GA_Normal_RankSelection.xlsx")
            elif(selType==2):
                ws.title = "Steady State Test Tournament Selection"
                wb.save("GA_Normal_TournamentSelection.xlsx")

            print(f"LOADING {sel}/2")
                    
    #With steady state 
    elif (sel == 1):
        resRound = 0
        for selType in range(3):
            results = []
            for p in population_range:
                for g in generation_range:
                    population = []
                    best_scores = []
                    start_time = time.time()
                    init(p)
                    #algorithm
                    best_result = float('inf')
                    for i in range(g):
                        #flag and the best values
                        population.sort(key=sortFitness, reverse=True)
                        best_result = population[0].fitness
                        best_scores.append(best_result)

                        flag = checkNear()
                        if (flag):
                            break
                        #already sorted now there is only the selection and the opreators before the new loop
                        #selection Roulet wheel selection 
                        #Here we replace the worst of the chromosomes with the best from the previous generation
                        #if (steadySS):
                        #its like a built in elitism but reverse --> so you just select some to change keep the rest
                        offspring = []
                        #should be changed to selections
                        #SELECTION
                        if (selType==0):
                            offspring = rouletSelection.select(population,round(len(population)/10), 0)
                        elif(selType==1):
                            offspring = rankSelection.select(population, round(len(population)/10), 0)
                        elif(selType==2):
                            offspring = tournamentSelection.select(population, round(len(population)/10), 4, 0)
                        #offspring = rouletSelection.select(population,round(len(population)/10), 0)
                        #offspring = rankSelection.select(population, round(len(population)/10), 0)
                        #offspring = tournamentSelection.select(population, round(len(population)/10), 4, 0)
                        offspring = crossover.crossover(offspring)
                        #Mutation 
                        offspring = mutation.mutate(offspring)
                        for i in range(len(offspring)):
                            if(population[len(population)-1-i].fitness < offspring[i].fitness):
                                population[len(population)-1-i] = offspring[i]

                        population.sort(key=sortFitness, reverse=True)

                        #print(f"The x is: {population[0].x} the y is: {population[0].y} FITNESS: {population[0].fitness}")
                    solution_time = time.time() - start_time                   
                    best = population[0]
                    results.append([p, g, solution_time, best.x, best.y, best.fitness, -1])
                        #resRound += 1
                        #print(f"Progress: {resRound}")
                resRound += 1
                print(f"Progress: {resRound}")
            results.sort(key=sortResult, reverse=True)
            #Extract it
            wb = Workbook()
            ws = wb.active
            #ws.title = "Steady State Test"
    
            headers = ["Population", "Generation", "Time (s)", "X", "Y", "Fitness", "Elitism"]
    
            ws.append(headers)
    
            for result in results:
                ws.append(result)
    
            for column in ws.columns:
                max_length = 0
    
                for cell in column:
                    if (cell.value is not None):
                        max_length = max(max_length, len(str(cell.value)))
    
                ws.column_dimensions[column[0].column_letter].width = max_length+2
            if (selType==0):
                ws.title = "Steady State Test Roulet Wheel"
                wb.save("GA_STEADYS_RouletWheel.xlsx")

            elif(selType==1):
                ws.title = "Steady State Test Rank Selection"
                wb.save("GA_STEADYS_RankSelection.xlsx")
            elif(selType==2):
                ws.title = "Steady State Test Tournament Selection"
                wb.save("GA_STEADYS_TournamentSelection.xlsx")
            
        
        print(f"LOADING 2/{sel}")
            
            #print("END1")

# results.sort(key=sortResult, reverse=True)
# #Extract it
# wb = Workbook()
# ws = wb.active
# ws.title = "Steady State Test"

# headers = ["Population", "Generation", "Time (s)", "X", "Y", "Fitness", "Elitism"]

# ws.append(headers)

# for result in results:
#     ws.append(result)

# for column in ws.columns:
#     max_length = 0

#     for cell in column:
#         if (cell.value is not None):
#             max_length = max(max_length, len(str(cell.value)))

#     ws.column_dimensions[column[0].column_letter].width = max_length+2

# wb.save("GA_STEADYS_FIRST.xlsx")

# print("END")






# test1 =  Chromosome.C(2, 0)
# ##print(test1.fitness)
# entity_fitness = functions.fitnessRosenbruck(test1)
# #print(entity_fitness, " ", test1.fitness)



