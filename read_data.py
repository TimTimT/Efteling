import csv

if __name__ == '__main__':
    def run():
        d = DataClass()
        print(d.averagewaitingtimes)


class DataClass:
    def __init__(self):
        self.indextable = self.makeIndexTable()
        self.averagewaitingtimes = self.getAverageWaitingTimes(self.indextable)
        self.distancetimes = self.getDistanceTimes(self.indextable)
        self.lengthofevents = self.getLengthOfEvent(self.indextable)
        self.capacity = self.getCapacity(self.indextable)
        self.linelengthtable = self.calculateLines(self.averagewaitingtimes,self.capacity)

    def calculateLines(self,averagewaitingtimes,capacity):
        #Y = tijd
        #X = attractieindex
        # capacity = pers/uur
        # waiting times = uur (minuten)    ->   waitingtimes*capacity  vb   0.5 uur *  1700 pers/uur
        linelengthtable = [[0.0 for x in range(len(averagewaitingtimes[0]))]for h in range(len(averagewaitingtimes))]

        for o in range(len(averagewaitingtimes)):
            for time in range(len(averagewaitingtimes[0])):
                linelengthtable[o][time] = (averagewaitingtimes[o][time]/60.0)*capacity[o]

        return linelengthtable

    def adjustWaitingtimes(self,oldpermutation=None,newpermutation=None,startinghour=0):
        totaletijd = startinghour
        vorige = None
        # parcours has been decided on, now adjust waiting times

        for index in newpermutation:
            if vorige != None:
                totaletijd += self.afstandtijdtable[vorige][index] / 5
            else:
                totaletijd += self.afstandtijdtable[0][index] / 5

            # here, totaleTijd equals the arrival time at the attraction
            # These are derivatives: Length of line is x in units of time, capacity is speed, line change is acceleration.
            # so what's the effect of adding to x on the line?
            # speed = 1700 pers/uur
            # line is x uur
            #
            # suppose: +1 person -> length of line = x+1/1700u
            #
            # if inflow is higher than capacity-> acceleration
            # if inflow is lower than capacity-> deceleration
            # definitely need table with all line lengths.


            if totaletijd > 117:
                totaletijd += 20
            else:
                totaletijd += self.wachttijdentable[index][int(round(totaletijd))] / 5

            totaletijd += self.duurtijdtable[index] / 300






            vorige = index
        totaletijd = totaletijd - startinghour
        print('totale tijd:', str(totaletijd / 30) + str('hrs'))





    def makeIndexTable(self):
        g = open('Wandeltijden.csv', 'r')
        reader = csv.reader(g, delimiter=';')
        count = 0
        names = []
        for row in reader:
            if row[0] != '':
                print(row[0])
                names.append(row[0])

            count += 1
        print('length of attractionlist:', len(names))
        return names

    def getAverageWaitingTimes(self, sortedindexes):
        table = [[0.0 for x in range(118)] for i in range(len(sortedindexes))]
        g = open('formatted_example_average_waiting_time_data.csv', 'r')
        reader = csv.reader(g)
        count = 0
        print('getting average waiting times...')
        for row in reader:
            if count > 0:
                for i in range(len(row)):
                    try:
                        f = heads[count - 1]
                        table[sortedindexes.index(heads[count - 1])][i] = float(row[i])
                    except ValueError:
                        print('\tskipped this one:', f)
                        break
            else:
                heads = row
                # for p in heads:
                #    print(p)

            count += 1
        print(table)
        return table

    def getDistanceTimes(self, sortedindices):
        table = [['' for y in range(len(sortedindices))] for x in range(len(sortedindices))]

        f = open('Wandeltijden.csv')
        reader = csv.reader(f, delimiter=';')
        count = 0
        heads = []
        print('sorted', sortedindices)
        for row in reader:
            if count > 0:

                indexofhead = sortedindices.index(row[0])
                for o in range(1, len(row)):
                    indexofcurrent = sortedindices.index(heads[o])
                    table[indexofhead][indexofcurrent] = float(row[o].replace(',', '.'))


            else:
                heads = row
                for p in heads:
                    print(p)

            count = 1
        print(table)
        return table


    def getLengthOfEvent(self, indextable):
        table = [0 for o in range(len(indextable))]
        f = open('duurtijd en capaciteit per attractie.csv')
        reader = csv.reader(f, delimiter=';')
        count = 0
        print(indextable)
        for row in reader:
            if count > 1:
                index = indextable.index(row[0])
                table[index] = int(row[1])
                print(row[0])

            count += 1
        return table


    def getCapacity(self, indextable):
        table = [0 for o in range(len(indextable))]
        f = open('duurtijd en capaciteit per attractie.csv')
        reader = csv.reader(f, delimiter=';')
        count = 0
        print(indextable)
        index = indextable.index('Ingang')
        table[index] = 0
        for row in reader:
            if count > 1:
                index = indextable.index(row[0])
                table[index] = int(row[3])
                print(row[0])

            count += 1
        return table


if __name__ == "__main__":
    run()
