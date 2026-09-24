import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


# from model import Chromosome
# from fitness import functions
#from operators import rouletSelection, crossover, mutation, rankSelection, steadyStateSelection, tournamentSelection
import random
import time

files = [
    "GA_RouletWheelHB.xlsx",
    "GA_RankSelectionHB.xlsx",
    "GA_TournamentSelectionHB.xlsx",
    "GA_SS_RouletWheelHB.xlsx",
    "GA_SS_RankSelectionHB.xlsx",
    "GA_SS_TournamentSelectionHB.xlsx"
]
labels = [
    "N Roulette",
    "N Rank",
    "N Tournament",
    "St.S Roulette",
    "St.S Rank",
    "St.S Tournament"
]

all_data = []

for file, label in zip(files, labels):
    df = pd.read_excel(file)
    df["Selection"] = label

    all_data.append(df)

# Combine all six Excel files
combined = pd.concat(all_data, ignore_index=True)

combined = combined.sort_values(
    by=["Fitness", "Time (s)"],
    ascending=[False, True]
).reset_index(drop=True)

top20 = combined.head(20)

print(top20)

top20.to_excel(
    "Top20_HimmelBlau.xlsx",
    index=False
) 
#initizalize

# population = []
# best_scores = []
# best_result = 0
# def init(populationLen):
#     for i in range(populationLen):
#         #initialize the chromosomes randomly
#         temp = Chromosome.C(random.uniform(-10,10), random.uniform(-10,10))
#         #this is the sphere function
#         entity_fitness = functions.fitnessRosenbruck(temp)
#         #functions.fitnessRosenbruck(temp)
#         population.append(temp)


# def sortFitness(val):
#     return val.fitness

# def sortResult(val):
#     return val[5]

# #check eta is 0.001 --> now between the last and the last minus 10 score
# def checkNear():
#     population.sort(key= sortFitness,reverse=True)
#     if (len(best_scores)<=200):
#         return False
#     if ( abs(best_result-best_scores[len(best_scores)-10]) > 0.00001 and abs(best_result-best_scores[len(best_scores)-20]) > 0.00001 and abs(best_result-best_scores[len(best_scores)-30]) > 0.00001):
#         return False
#     else:
#         return True 

# all_averages = []

# for i in range(len(top20)):
#     avg_range = []
#     for avg in range(20):
#         results = []
#         population = []
#         best_scores = []
#         offspring = []
#         init(top20["Population"][i])
#         best_result = float('inf')
#         start_time = time.time()
#         for g in range(len(top20["Generation"][i])):
#             population.sort(key=sortFitness, reverse=True)
#             #flag and the best values
#             flag = checkNear()
#             best_result = population[0].fitness
#             best_scores.append(best_result)
            
#             if (flag):
#                 break

#             if (top20["Selection"][i]=="N Roulette"):
#                 population = rouletSelection.select(population, 0, top20["Elitism"][i])
#                 population = crossover.crossover(population)
#                 #Mutation 
#                 population = mutation.mutate(population, top20["Mutation chance"][i])

#             elif(top20["Selection"][i]=="N Rank"):
#                 population = rankSelection.select(population, 0, top20["Elitism"][i])
#                 population = crossover.crossover(population)
#                 #Mutation 
#                 population = mutation.mutate(population, top20["Mutation chance"][i])

#             elif(top20["Selection"][i]=="N Tournament"):
#                 population = tournamentSelection.select(population, 0, top20["Tournament Count"][i], top20["Elitism"][i])
#                 population = crossover.crossover(population)
#                 #Mutation 
#                 population = mutation.mutate(population, top20["Mutation chance"][i])

#             elif(top20["Selection"][i]=="St.S Roulette"):
#                 offspring = rouletSelection.select(population,round(len(population)/100*top20["Parent precentage"][i]), 0)
#                 offspring = crossover.crossover(offspring)
#                                                         #Mutation 
#                 offspring = mutation.mutate(offspring, top20["Mutation chance"][i])
#                 for j in range(len(offspring)):
#                     if(population[len(population)-1-j].fitness < offspring[j].fitness):
#                         population[len(population)-1-j] = offspring[j]

#             elif(top20["Selection"][i]=="St.S Rank"):
#                 offspring = rankSelection.select(population, round(len(population)/100*top20["Parent precentage"][i]), 0)
#                 offspring = mutation.mutate(offspring, top20["Mutation chance"][i])
#                 for j in range(len(offspring)):
#                     if(population[len(population)-1-j].fitness < offspring[j].fitness):
#                         population[len(population)-1-j] = offspring[j]

#             elif(top20["Selection"][i]=="St.S Tournament"):
#                 offspring = tournamentSelection.select(population, round(len(population)/100*top20["Parent precentage"][i]), t, 0)
#                 offspring = mutation.mutate(offspring, top20["Mutation chance"][i])
#                 for j in range(len(offspring)):
#                     if(population[len(population)-1-j].fitness < offspring[j].fitness):
#                         population[len(population)-1-j] = offspring[j]
#         solution_time = time.time() - start_time                   
#         best = population[0]
#         avg_range.append([
#             best.fitness,
#             solution_time,
#             best.x,
#             best.y
#         ])        
#     avg_range = np.array(avg_range)

#     average_fitness = np.mean(avg_range[:, 0])
#     average_time = np.mean(avg_range[:, 1])
#     average_x = np.mean(avg_range[:, 2])
#     average_y = np.mean(avg_range[:, 3])

#     std_fitness = np.std(avg_range[:, 0])
#     std_time = np.std(avg_range[:, 1])

#     all_averages.append([
#         selection,
#         population_len,
#         generation_len,
#         elitism,
#         parent_percentage,
#         tournament_count,
#         mutation_chance,
#         average_fitness,
#         std_fitness,
#         average_time,
#         std_time,
#         average_x,
#         average_y
#     ])      

# average_df = pd.DataFrame(
# all_averages,
# columns=[
#     "Selection",
#     "Population",
#     "Generation",
#     "Elitism",
#     "Parent percentage",
#     "Tournament count",
#     "Mutation chance",
#     "Average fitness",
#     "Fitness std",
#     "Average time",
#     "Time std",
#     "Average X",
#     "Average Y"
# ]
# )

# print("\nFINAL AVERAGES:")
# print(average_df)

# average_df.to_excel(
#     "Top20_Validation_Averages.xlsx",
#     index=False
# )     

