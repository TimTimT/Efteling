

import genetic_runner


class Visitor:
    def __init__(self,permutatie=None):
        self.locatie = 0
        self.hourofstart= 0
        self.permutatie = permutatie
        self.permutatieStartuur = 0


    def calculate(self,locatie=None,lijstvanattracties=None,uur=0,dataclass=None,generations=200):
        g = genetic_runner.Genetic()
        oldpermutation = self.permutatie
        self.permutatie = g.runGenetic(dataclass, generations, lijstvanattracties,locatie,uur)
        #currentlocation = 0
        #if oldpermutation != None:
        #    currentlocation = dataclass.getcurrentlocation(self.locatie, self.hourofstart,oldpermutation,uur)
        dataclass.adjustWaitingtimes(oldpermutation=oldpermutation,newpermutation=self.permutatie,
                                     oldstartinglocation=self.locatie,newstartinglocation=locatie,oldstartinghour=self.hourofstart,
                                     newstartinghour=uur)
        self.locatie = locatie
        self.hourofstart = uur
        return self.permutatie

