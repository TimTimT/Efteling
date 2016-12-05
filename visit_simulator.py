


import read_data
from visitor import Visitor
import random

if __name__ == '__main__':
    def run():
        simulator = Simulator()
        d = read_data.DataClass()
        simulator.simulateVisits(2000,0.2,d)




class Simulator:
    def simulateVisits(self,totalvisitors,proportionthatuseapp,dataclass):

        #let's assume for a second that everyone arrives at 8u30 but is active at 8

        listofvisitors = [Visitor() for j in range(int(proportionthatuseapp*totalvisitors))]
        for i in listofvisitors:
            print(i.__class__)
        amountofusers = proportionthatuseapp*totalvisitors



        list = [0 for i in range(10)]
        list[0] = 1.3
        list[1] = 0.6
        list[2] = 0.6
        list[3] = 0.5
        list[4] = 0.5
        list[5] = 0.6
        list[6] = 0.4
        list[7] = 0.4
        list[8] = 0.1
        list[9] = 0.1

        timeline = [0 for x in range(10000)]
        for i in range(10):
            clicks = int(list[i]*amountofusers)
            # add clicks in random places
            for k in range(clicks):
                timeline[random.randint(i*1000,i*1000+999)]+=1



        for j in range(10000):
            currenttime = j/10000 * 118

            for i in range(timeline[j]):
                # take random visitor and make him click ;)
                vis = listofvisitors[random.randint(0,amountofusers)]
                amountofattractions = random.normalvariate(15,2)
                listofattractions = []
                for kl in range(int(amountofattractions)):
                    r = random.randint(0,27)
                    if r not in listofattractions:
                        listofattractions.append(r)
                #oldstartinglocation, oldstartinghour, oldpermutation, newstartinghour
                currentlocation = dataclass.getcurrentlocation(vis.locatie, vis.hourofstart,vis.permutatie,currenttime)
                vis.calculate(locatie=currentlocation,lijstvanattracties=listofattractions,uur=currenttime,dataclass=dataclass,generations=200)

        return

    def tryout(self,d):
        examplevisitor = Visitor()
        attracties = [5, 8, 10, 22, 26, 1, 0, 4]
        permutatie = examplevisitor.calculate(lijstvanattracties=attracties,dataclass=d,generations=100)
        print(permutatie)
        # since it knows the old permutation, it can reverse the effects on the waiting tables.













if __name__ == "__main__":
    run()

