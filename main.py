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
parent_range = range(10, 30, 10)
population_range = range(20, 80, 20)
generation_range = range(200, 800, 100)
tournament_range = range(4, 6, 1)
mutation_precentage = range(0, 15, 5)
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
        entity_fitness = functions.himmelBlau(temp)
        #functions.fitnessRosenbruck(temp)
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
        for selType in range(3):
            results = []
            for k in elitism_range:
                for t in tournament_range:    
                    for m in mutation_precentage:
                        for p in population_range:
                                for g in generation_range:
                                    avg_range = []
                                    for avg in range(3):
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
                                                population = tournamentSelection.select(population, 0, t, k)
                                            #crossoverTest --> at 50% and thats it after we just swap the new pop for the old one
                                            population = crossover.crossover(population)

                                            #Mutation 
                                            population = mutation.mutate(population, m)
                                        #final sort
                                        population.sort(key=sortFitness, reverse=True)
                                        #print(f"The x is: {population[0].x} the y is: {population[0].y} FITNESS: {population[0].fitness}")
                                        solution_time = time.time() - start_time
                                        best = population[0]
                                        avg_range.append([p, g, solution_time, best.x, best.y, best.fitness, k, m, t if selType==2 else None])
                                    #averages = [sum(x for x in column if x is not None) / sum(x is not None for x in column) for column in zip(*avg_range)]
                                    avg_time = 0
                                    avg_fitness = 0
                                    for temp in range(len(avg_range)):
                                        avg_time += avg_range[temp][2]
                                        avg_fitness += avg_range[temp][5]
                                    avg_time = avg_time/len(avg_range)
                                    avg_fitness = avg_fitness/len(avg_range)
                                    #results.append(averages[0], averages[1], averages[2],averages[3],averages[4],averages[5],averages[6],averages[7],[averages[8]])
                                    results.append([p, g, avg_time, best.x, best.y, avg_fitness, k, m, t if selType==2 else None])
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

            headers = ["Population", "Generation", "Time (s)", "X", "Y", "Fitness", "Elitism", "Mutation chance", "Tournament Count" if selType==2 else None]

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
                ws.title = "N Roulet Wheel"
                wb.save("GA_RouletWheelHB.xlsx")

            elif(selType==1):
                ws.title = "N Rank Selection"
                wb.save("GA_RankSelectionHB.xlsx")
            elif(selType==2):
                ws.title = "N Tournament Selection"
                wb.save("GA_TournamentSelectionHB.xlsx")

            print(f"LOADING {sel}/2")
                    
    #With steady state 
    elif (sel == 1):
        resRound = 0
        for selType in range(3):
            results = []
            for par in parent_range:
                for t in tournament_range:
                    for m in mutation_precentage:
                        for p in population_range:
                            for g in generation_range:
                                avg_range = []
                                for avg in range(3):
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
                                            offspring = rouletSelection.select(population,round(len(population)/100*par), 0)
                                        elif(selType==1):
                                            offspring = rankSelection.select(population, round(len(population)/100*par), 0)
                                        elif(selType==2):
                                            offspring = tournamentSelection.select(population, round(len(population)/100*par), t, 0)
                                        #offspring = rouletSelection.select(population,round(len(population)/10), 0)
                                        #offspring = rankSelection.select(population, round(len(population)/10), 0)
                                        #offspring = tournamentSelection.select(population, round(len(population)/10), 4, 0)
                                        offspring = crossover.crossover(offspring)
                                        #Mutation 
                                        offspring = mutation.mutate(offspring, m)
                                        for i in range(len(offspring)):
                                            if(population[len(population)-1-i].fitness < offspring[i].fitness):
                                                population[len(population)-1-i] = offspring[i]

                                        population.sort(key=sortFitness, reverse=True)

                                        #print(f"The x is: {population[0].x} the y is: {population[0].y} FITNESS: {population[0].fitness}")
                                    solution_time = time.time() - start_time                   
                                    best = population[0]
                                    avg_range.append([p, g, solution_time, best.x, best.y, best.fitness, par, m, t if selType==2 else None])
                                        #resRound += 1
                                        #print(f"Progress: {resRound}")
                            #averages = [sum(x for x in column if x is not None) / sum(x is not None for x in column) for column in zip(*avg_range)]
                            #results.append(averages[0], averages[1], averages[2],averages[3],averages[4],averages[5],averages[6],averages[7],[averages[8]])
                                    avg_time = 0
                                    avg_fitness = 0
                                    for temp in range(len(avg_range)):
                                        avg_time += avg_range[temp][2]
                                        avg_fitness += avg_range[temp][5]
                                    avg_time = avg_time/len(avg_range)
                                    avg_fitness = avg_fitness/len(avg_range)   
                                    results.append([p, g, avg_time, best.x, best.y, avg_fitness, par, m, t if selType==2 else None]) 
                        resRound += 1
                    print(f"Progress: {resRound}")
            results.sort(key=sortResult, reverse=True)
            #Extract it
            wb = Workbook()
            ws = wb.active
            #ws.title = "Steady State Test"
    
            headers = ["Population", "Generation", "Time (s)", "X", "Y", "Fitness", "Parent precentage","Mutation chance", "Tournament Count" if selType == 2 else None]
    
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
                ws.title = "SS Roulet Wheel"
                wb.save("GA_SS_RouletWheelHB.xlsx")

            elif(selType==1):
                ws.title = "SS Rank Selection"
                wb.save("GA_SS_RankSelectionHB.xlsx")
            elif(selType==2):
                ws.title = "SS Tournament Selection"
                wb.save("GA_SS_TournamentSelectionHB.xlsx")
            
        
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



