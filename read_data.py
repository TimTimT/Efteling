import csv
import pandas as pd
import datetime

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
        self.linelengthtable = self.calculateLines()
        self.showtimes = [[72,90,108],[66,90],[111],[66],[72,84,96],[24]]
        self.showdurations=[20,20,12,30,20,20]

        """
        Raveleijn	de Sprookjesboom	Aquanura	Pardoes en pardijn	The fire prince and snow princess	Efteling bewoners
72	66	111	66	72	24
90	90			84
108				96

20min	20min	12min	30min	0min	20min

        """

    def calculateLines(self):
        #Y = tijd
        #X = attractieindex
        # capacity = pers/uur
        # waiting times = uur (minuten)    ->   waitingtimes*capacity  vb   0.5 uur *  1700 pers/uur
        # So, from the change in waiting time, we can estimate how many people arrived
        # ex: 10/5minutes. -> 11/5minutes-> new waiting time

        linelengthtable = [[0.0 for x in range(len(self.averagewaitingtimes[0]))]for h in range(len(self.averagewaitingtimes))]
        for o in range(len(self.averagewaitingtimes)):
            for time in range(len(self.averagewaitingtimes[0])):
                linelengthtable[o][time] = (self.averagewaitingtimes[o][time]/60.0)*self.capacity[o]
        return linelengthtable

    def addAPerson(self,uur,attractie):
        # depending on the length of the line at [attractie][uur] and the capacity[attractie],
        # the lengths of lines at uur+x get longer as well.
        #capacity = self.capacity[attractie]/12    #capacity per 5 minutes.
        time = self.averagewaitingtimes[attractie][uur]
        # if time =30-> adjust length for 30/5 lines -> x,x+1 .... x+5
        columnstoadjust = int(round(time/5))
        for i in range(uur,uur+columnstoadjust):
            self.linelengthtable[attractie][i]+=1
            self.averagewaitingtimes[attractie][i] = self.linelengthtable[attractie][i]/(self.capacity[attractie]/60)

    def removeAPerson(self,uur,attractie):
        time = self.averagewaitingtimes[attractie][uur]
        columnstoadjust = int(round(time / 5))
        for i in range(uur,uur+columnstoadjust):
            self.linelengthtable[attractie][i]-=1
            self.averagewaitingtimes[attractie][i] = self.linelengthtable[attractie][i]/(self.capacity[attractie]/60)


    def getcurrentlocation(self,oldstartinglocation, oldstartinghour,oldpermutation,currenttime):
        vorige = oldstartinglocation
        totaletijd = oldstartinghour
        # parcours has been decided on, now adjust waiting times
        do = True
        if oldpermutation != None:
            for index in oldpermutation:
                totaletijd += self.distancetimes[vorige][index] / 5
                # here, totaleTijd equals the arrival time at the attraction

                if totaletijd > currenttime and do:
                    return vorige
                if totaletijd > 117:
                    totaletijd += 20
                else:
                    totaletijd += self.averagewaitingtimes[index][int(round(totaletijd))] / 5

                totaletijd += self.lengthofevents[index] / 300
                vorige = index
        return 0

    def adjustWaitingtimes(self,oldpermutation=None,newpermutation=None,oldstartinglocation=0,newstartinglocation=0,oldstartinghour=0,newstartinghour=0):
        vorige = oldstartinglocation
        totaletijd = oldstartinghour
        # parcours has been decided on, now adjust waiting times

        if oldpermutation !=None:
            for index in oldpermutation:
                totaletijd += self.distancetimes[vorige][index] / 5
            # here, totaleTijd equals the arrival time at the attraction
                self.removeAPerson(int(round(totaletijd)),index)

                if totaletijd > 117:
                    totaletijd += 20
                else:
                    totaletijd += self.averagewaitingtimes[index][int(round(totaletijd))] / 5

                totaletijd += self.lengthofevents[index] / 300
                vorige = index

        totaletijd = newstartinghour
        vorige = newstartinglocation
        for index in newpermutation:

            totaletijd += self.distancetimes[vorige][index] / 5

            # here, totaleTijd equals the arrival time at the attraction
            self.addAPerson(int(round(totaletijd)),index)

            if totaletijd > 117:
                totaletijd += 20
            else:
                totaletijd += self.averagewaitingtimes[index][int(round(totaletijd))] / 5

            totaletijd += self.lengthofevents[index] / 300

            vorige = index




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

        dir_wachttijd_data = '/Users/Timo/Dropbox/Project Management/Efteling Data/Merged/efteling_data_from_2016-11-02_to_2016-11-27_with_day_types.csv'
        wachttijd_df = pd.read_csv(dir_wachttijd_data, index_col=0)
        # Change variable name of 'hour'
        wachttijd_df = wachttijd_df.rename(columns={'hour': 'time'})
        # Create new variable, for grouping purposes
        wachttijd_df['hour'] = [i[:2] for i in wachttijd_df['time']]
        # Group the data , day_type , name and hour
        grouped_data = wachttijd_df.groupby(['day_type', 'name', 'time'], as_index=False).mean()



        #grouped_data.to_csv('vliegende_hollander_mystery.csv')


        print(datetime.date.today())
        day_type = self.get_day_type(datetime.date.today())
        table = [[0.0 for x in range(118)] for i in range(len(sortedindexes))]
        for l in range(len(sortedindexes)):
            if l == 0:
                continue
            for hour in range(118):
                minutes = (102 + hour)*5
                actualhour = minutes//60
                minutes = minutes%60
                if minutes < 10:
                    minutesstr = '0'+str(minutes)
                else:
                    minutesstr = str(minutes)
                hourstring = str(actualhour).zfill(2)

                stre = hourstring+':'+minutesstr+':00'
                #print(grouped_data.loc[(grouped_data['day_type'] == day_type) &
                        #(grouped_data['name'] == sortedindexes[l])].iloc[8888:])

                #print(stre, sortedindexes[l])
                #print(sortedindexes[l])
                try:
                    obs = grouped_data.loc[(grouped_data['day_type'] == day_type) &
                         (grouped_data['name'] == sortedindexes[l]) & (
                                grouped_data['time'] == stre)]['waiting_time'].values[0]
                    table[l][hour] = obs
                except IndexError:
                    table[l][hour] = obs


                last = obs
        return table



        """
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
        """

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

    def get_day_type(self,date):
        # Open feestdagen en check with the data
        dir_feestdagen = '/Users/Timo/Dropbox/Project Management/Feestdagen.csv'
        with open(dir_feestdagen, 'r') as f:
            reader = csv.reader(f)
            list_f = list(reader)[0]

        '''
        Assign day types
        1 = Feestdag
        2 = Weekend
        3 = Weekdag
        '''

        if date.strftime('%Y-%m-%d') in list_f:
            return 1
        elif date.isoweekday() > 5:
            return 2
        else:
            return 3


if __name__ == "__main__":
    run()
