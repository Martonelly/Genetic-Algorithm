import numpy as np
import math
#fitness needs to be negative for rouletwheel reasons (bigger fitenss --> more accurate minimum, dont forget to change symbol)
def fitnessRosenbruck(chromosome):
    x,y = chromosome.x, chromosome.y
    funk_value = (x**2 + y**2 + 20 - 10*(math.cos(2*math.pi*x) + math.cos(2*math.pi*y)))
    chromosome.fitness = -funk_value
    return -funk_value

def simple(chromosome): 
    x,y = chromosome.x, chromosome.y 
    funk_value = x**2 + y**2
    chromosome.fitness = -funk_value

def myFunction(chromosome):
    x,y = chromosome.x, chromosome.y 
    funk_value = (x**2 + y**2 + x*y - math.sin(2*y**2) + 2*y)
    chromosome.fitness = -funk_value

