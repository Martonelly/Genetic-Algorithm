#Chromosome needs x and y coordinate and it also needs a fittnes counter
import sys


class C:
    
    def __init__(self, x=0, y=0, fitness = float('inf')):
        self.x = x
        self.y = y
        self.fitness = fitness

    def __str__(self):
        return self.x," ", self.y, " ", self.fitness

    def __repr__(self):
        return f"X: {self.x};  Y: {self.y};  Fitness: {self.fitness}"