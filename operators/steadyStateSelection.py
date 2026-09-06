def select(population):
    bestSet = []
    for j in range(len(bestSet)):
                population[len(population)-1-j] = bestSet[j]
    return population
