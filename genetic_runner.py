import evaluator
from deap import algorithms, base, creator, tools
import random, operator
import numpy
import read_data
import matplotlib.pyplot as plt




if __name__ == '__main__':
    def run():
        d = read_data.DataClass()
        g = Genetic()
        attracties = [5,8,10,22,26,1,0,4]
        g.runGenetic(d,50,attracties)


class Genetic:
    def runGenetic(self,dataclass,generations,lijstattracties):

        translationtable = []
        for i in lijstattracties:
            translationtable.append(i)

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

        toolbox.register("evaluate", evaluation,wachttijdentable=dataclass.averagewaitingtimes,afstandtijdtable=dataclass.distancetimes,duurtijdtable=dataclass.lengthofevents,translationtable=translationtable)
        toolbox.register("select", tools.selTournament, tournsize=3)

        pop = toolbox.population(n=100)

        fit_stats = tools.Statistics(key=operator.attrgetter("fitness.values"))
        fit_stats.register('mean', numpy.mean)
        fit_stats.register('min', numpy.min)
        hof = tools.HallOfFame(1)
        result, log = algorithms.eaSimple(pop, toolbox,
                                          cxpb=0.8, mutpb=0.2,
                                          ngen=generations,halloffame=hof,verbose=False,stats=fit_stats)
        plt.figure(1, figsize=(11, 4), dpi=500)
        plots = plt.plot(log.select('min'), 'c-', log.select('mean'), 'b-', antialiased=True)
        plt.legend(plots, ('Minimum fitness', 'Mean fitness'))
        plt.ylabel('hrs')
        plt.xlabel('Generations')
        plt.savefig("Evolution of schedule")
        print(evaluation(hof[0],wachttijdentable=dataclass.averagewaitingtimes,afstandtijdtable=dataclass.distancetimes,duurtijdtable=dataclass.lengthofevents,translationtable=translationtable))
        print('result',hof[0])


        #translateback
        perm = []
        for i in hof[0]:
            perm.append(lijstattracties[i])
        return perm

def evaluation(individual,wachttijdentable=None,afstandtijdtable=None,duurtijdtable=None,translationtable=None):
    return (evaluator.Evaluation.evaluate(afstandtijdtable,wachttijdentable,duurtijdtable,individual,translationtable),)

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
