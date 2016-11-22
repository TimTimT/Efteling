

import genetic_runner


class Visitor:
    def __init__(self,permutatie=None):
        self.locatie = 0
        self.permutatie = []
        self.permutatieStartuur = 0


    def calculate(self,locatie=0,lijstvanattracties=None,uur=0,dataclass=None,generations=200):
        g = genetic_runner.Genetic()
        self.permutatie = g.runGenetic(dataclass,generations,lijstvanattracties)
        return self.permutatie



