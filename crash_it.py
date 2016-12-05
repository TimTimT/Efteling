# this class gets a permutation and a time limit, it attempts to crash optimally.

import random
import read_data
import time


if __name__ == '__main__':
    def run():
        dataclass = read_data.DataClass()
        attracties = [9, 16, 23, 18, 20, 22, 6, 13]
        pso = PSO_attempt()
        time1 = time.time()
        pso.crashPermutation(attracties,100,100,0.729,2.025,2.025,dataclass.averagewaitingtimes,dataclass.lengthofevents,dataclass.distancetimes,35,0,0)
        print(time.time()-time1)



class PSO_attempt:
    def crashPermutation(self,permutation,swarmsize,generations,omega,phip,phig,wachttijdentable,duurtijdtable,afstandtable,deadline,startingtime,startingposition):
        # enkel length of permutation is hier eigelijk belangrijk.


        swarm = []
        permlen = len(permutation)
        for fly in range(swarmsize):
            choices = []
            for i in range(len(permutation)):
                choices.append(random.uniform(0.0,4.0))
            swarm.append(choices)

        bestknownposition = []
        bestknownscores = []
        bestscoreever = 100000

        for i in swarm:
            bestknownposition.append(i)
            bestknownscores.append(self.evaluate(i,wachttijdentable,duurtijdtable,afstandtable,permutation,deadline,startingtime,startingposition))
        bestknownpos = swarm[0]

        v= []
        for i in range(len(swarm)):
            speed = []
            for j in range(len(permutation)):
                speed.append(random.uniform(-4.0/100,4.0/100))
            v.append(speed)

        for i in range(generations):
            for particle in range(swarmsize):
                for d in range(permlen):
                    rp = random.uniform(0,1)
                    rg = random.uniform(0,1)
                    #update velocity

                    v[particle][d] = omega*v[particle][d] + phip * rp \
                                                            * (bestknownposition[particle][d]-swarm[particle][d])+ phig * rg* (bestknownpos[d]-swarm[particle][d])
                    # update position
                    newpos = swarm[particle][d]+v[particle][d]
                    if newpos >= 0.0:
                        swarm[particle][d] = newpos
                        if newpos <= 4.0:
                            swarm[particle][d] = newpos
                        else:
                            swarm[particle][d] = 4.0
                    else:
                        swarm[particle][d] = 0.0
                score = self.evaluate(swarm[particle],wachttijdentable,duurtijdtable,afstandtable,permutation,deadline,startingtime,startingposition)

                if score<bestknownscores[particle]:
                    bestknownscores[particle] = score
                    bestknownposition[particle] = swarm[particle]
                    #print(score)
                if score < bestscoreever:
                    bestscoreever = score
                    bestknownpos = swarm[particle]
                    #print(score)
            #print(bestknownscores)
        print(bestscoreever,'runner ups',bestknownscores)




    def evaluate(self, particle,wachttijdentable,duurtijdtable,afstandtable,permutatie,deadline,startingtime,startingposition):# returns cost! not in time -> big penalty
        print('evaluate')
        decisions = []
        for sc in particle:
            decisions.append(int(round(sc)))
        leng = len(permutatie)
        time = startingtime
        totalcost = 0
        vorige = startingposition
        for i in range(leng):
            time += afstandtable[vorige][i] / 5
            percAndCost = self.getPercentageAndFixedCost(decisions[i])
            if percAndCost[0] == 1.0:
                # no waiting time
                totalcost += percAndCost[1]
                pass
            else:

                waitingtime = wachttijdentable[permutatie[i]][int(round(time))]/5
                time+= waitingtime * (1-percAndCost[0])
                if percAndCost[0]>0.0:
                    totalcost+= percAndCost[1] + 0.06 * waitingtime * (1-percAndCost[0])
            ######
            if percAndCost[0]==0.0:
                print('Do not crash')
            elif percAndCost[0]==0.3:
                print('Bronze')
            elif percAndCost[0] == 0.5:
                print('Silver')
            elif percAndCost[0]== 0.9:
                print('Gold')
            elif percAndCost[0]== 1.0:
                print('single shot')

            ######
            time+= duurtijdtable[permutatie[i]]/300

            vorige = permutatie[i]
        if time> deadline:
            totalcost+=(time-deadline)*50

        return totalcost



    def getPercentageAndFixedCost(self, decision):
        if decision == 0:
            return [0.0,1]
        if decision == 1:
            return[0.3,0.5]
        if decision == 2:
            return [0.5,1.25]
        if decision == 3:
            return [0.9,2.0]
        if decision == 4:
            return [1.0,5]



class crash:
    def crashPermutation(self,permutation,startuur,deadline):
        # crash price =  fixed(type) + f(wachtrij)

        # what this method does, is go look at the waiting times, see what methods can win enough time to catch
        # the deadline, and takes the cheapest one. Does it check all options?


        benefitbronze = 0.3
        benefitsilver = 0.5
        benefitgold = 0.9

        fixedbronze = 0.5
        fixedsilver = 1.25
        fixedgold = 2.0
        fixedsingleshot = 5.0

        priceperminute = 0.06

        # price = fixed + priceperminute * benefit * waitingtime

        # how many options ? pow(4,len(perm))     = 1 000 000 for 10 attr.
        # check all? Is there a better heuristic? Well, cost increases are not entirely linear
        # Try cheapest option every time, and if it's not sufficient.
        #
        # why not try particle swarm optimization?



        """
        n walibi werken ze met een systeem met verschillende gradaties van voorsteken. vb:
        brons -> 30% minder wachten.
        zilver 50% wachten.
        Gold -> 90% minder wachten.
        single shot -> geen wachtrij

        """


if __name__ == "__main__":
    run()

