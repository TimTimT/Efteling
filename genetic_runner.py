import evaluator
from deap import algorithms, base, creator, tools
import random, operator
import numpy
import read_data
import matplotlib.pyplot as plt
import timeit
import time
import psutil


if __name__ == '__main__':
    def run():
        g = Genetic()


        d = read_data.DataClass()

        attracties = [2,5,23,13,9,16,24,8]
        #attracties =[0 + i for i in range(20)]
        # 1-- [2,5,23,13,9,16,24,8,3,12]
        # 2-- [17,7,11,21,10,19,15,14,20,18]
        # 3-- [22,6,1,4,2,5,23,13,9]
        # 4-- [18,20,21,17,7,11,19,15,14]
        # 5-- [6,22,20,18,23,5,13,9,16]

        # 1-- [2,5,23,13,9,16,24,8]
        # 2-- [17,7,11,21,10,19,15,14]
        # 3-- [22,6,1,4,2,5,23,13]
        # 4-- [18,20,21,17,7,11,19,15]
        # 5-- [6,22,20,18,23,5,13,9]


        print(psutil.cpu_percent())

        for i in range(1):
            g.runGenetic(d,200,attracties,0,25)
        #g.justGiveMeTheSchedule(d,attracties,,50)


class Genetic:
    def justGiveMeTheSchedule(self,dataclass,lijstattracties,locatie,startuur):
        translationtable = []
        r = []
        count = 0
        for i in lijstattracties:
            translationtable.append(i)
            r.append(count)
            count+=1

        # print('result',hof[0])
        evaluation2(r, wachttijdentable=dataclass.averagewaitingtimes, afstandtijdtable=dataclass.distancetimes,
                    duurtijdtable=dataclass.lengthofevents, translationtable=translationtable, location=locatie,
                    startuur=startuur, showtijdtable=dataclass.showtimes, showduration=dataclass.showdurations,
                    indextable=dataclass.indextable)

        # translateback
        perm = []
        # print('hof',hof[0])
        print(translationtable)
        for i in r:
            perm.append(dataclass.indextable[lijstattracties[i]])
        print('results', perm)

        return perm

    def runGenetic(self,dataclass,generations,lijstattracties,locatie,startuur):

        translationtable = []
        for i in lijstattracties:
            translationtable.append(i)
        print('trans',translationtable)

        toolbox = base.Toolbox()
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

        toolbox.register("indices", numpy.random.permutation, len(lijstattracties))
        toolbox.register("individual", tools.initIterate, creator.Individual,
                         toolbox.indices)
        toolbox.register("population", tools.initRepeat, list,
                         toolbox.individual)

        toolbox.register("mate", tools.cxOrdered)
        toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)

        toolbox.register("evaluate", evaluation,wachttijdentable=dataclass.averagewaitingtimes,afstandtijdtable=dataclass.distancetimes,duurtijdtable=dataclass.lengthofevents,translationtable=translationtable,location=locatie,startuur=startuur,showtijdtable=dataclass.showtimes,showduration=dataclass.showdurations)
        toolbox.register("select", tools.selTournament, tournsize=3)

        pop = toolbox.population(n=100)

        fit_stats = tools.Statistics(key=operator.attrgetter("fitness.values"))
        fit_stats.register('mean', numpy.mean)
        fit_stats.register('min', numpy.min)
        hof = tools.HallOfFame(1)
        time1 = time.time()
        result, log = algorithms.eaSimple(pop, toolbox,
                                          cxpb=0.8, mutpb=0.2,
                                          ngen=generations,halloffame=hof,verbose=False,stats=fit_stats)
        time2 = time.time()
        #print('duration', time2 - time1)
        plt.figure(1, figsize=(11, 4), dpi=500)
        plots = plt.plot(log.select('min'), 'c-', log.select('mean'), 'b-', antialiased=True)
        plt.legend(plots, ('Minimum fitness', 'Mean fitness'))
        plt.ylabel('hrs')
        plt.xlabel('Generations')
        plt.savefig("Evolution of schedule")
        #print('here',hof[0])
        print('best',evaluation(hof[0],wachttijdentable=dataclass.averagewaitingtimes,afstandtijdtable=dataclass.distancetimes,duurtijdtable=dataclass.lengthofevents,translationtable=translationtable,location=locatie,startuur=startuur,showtijdtable=dataclass.showtimes,showduration=dataclass.showdurations)[0])
        #print('result',hof[0])
        evaluation2(hof[0],wachttijdentable=dataclass.averagewaitingtimes,afstandtijdtable=dataclass.distancetimes,duurtijdtable=dataclass.lengthofevents,translationtable=translationtable,location=locatie,startuur=startuur,showtijdtable=dataclass.showtimes,showduration=dataclass.showdurations,indextable=dataclass.indextable)


        #translateback
        perm = []
        #print('hof',hof[0])
        #print(translationtable)
        for i in hof[0]:
            perm.append(translationtable[i])

        print('results',perm)


        return perm

def evaluation(individual,wachttijdentable=None,afstandtijdtable=None,duurtijdtable=None,translationtable=None,location=None,startuur=None,showtijdtable=None,showduration=None):

    return (evaluator.Evaluation.evaluate(afstandtijdtable,wachttijdentable,duurtijdtable,individual,translationtable,location,startuur,showtijdtable,showduration),)
def evaluation2(individual,wachttijdentable=None,afstandtijdtable=None,duurtijdtable=None,translationtable=None,location=None,startuur=None,showtijdtable=None,showduration=None,indextable=None):

    return (evaluator.Evaluation.evaluate2(afstandtijdtable,wachttijdentable,duurtijdtable,individual,translationtable,location,startuur,showtijdtable,showduration,indextable),)
def randomShuffle(lijstattracties):
    numpy.random.shuffle(lijstattracties)
    return lijstattracties

def mate(ind1,ind2):
    for i in range(0,len(ind1),2):
        ind1[i]= ind2[i]
        ind2[i+1]=ind1[i+1]

    return tuple([ind1,ind2])


if __name__ == "__main__":
    run()
