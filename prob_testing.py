import random
import time
import math


if __name__ == '__main__':
    def run():
        T = TTT()
        amountofvisitors = 15000
        ghz = 3.0
        cores = 16


        clicktable = T.generateClickTable(amountofvisitors)
        T.scheduleCPUtime(clicktable,ghz,cores)
        print('amount of visitors:',amountofvisitors)

        # now what to do with the clicktable



        # We will randomly distribute the

class TTT:
    def generateClickTable(self,amountofvisitors):


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

        clicks = [[0 for i in range(3600)] for y in range(10)]

        count = 0
        for probofclick in list:

            for j in range(amountofvisitors):
                if probofclick > 1.0:
                    n = random.randint(0, 3599)
                    clicks[count][n] += 1
                    if random.uniform(0.0, 1.0) > probofclick - 1:
                        pass
                    else:
                        n = random.randint(0, 3599)
                        clicks[count][n] += 1
                else:
                    if random.uniform(0.0, 1.0) > probofclick:
                        # no click
                        pass
                    else:
                        clicks[count][random.randint(0, 3599)] += 1
            print(clicks[count])
            count += 1


        return clicks

    def scheduleCPUtime(self,clicktable, CPUCapacity, cores):
        # what do we want? we want data about the distribution of how long it takes for the server to respond.
        #

        # calculate the capacity that once core can handle per second, expressed in calls from the server.
        # the processing time for this mac is 2.65 seconds (20 attractie average)

        capacityofthismac = 2.7 # per core?

        processtime = 2.65 * capacityofthismac/CPUCapacity

        print(CPUCapacity, ' Ghz, ',cores,' cores')

        # Per core, requests can only be scheduled sequentially
        # Seperate requests can be assigned to different cores.

        # So the algortithm should add the request to the core with the least work.
        # However, we can never get the speed under 2.7/4.4*2.65 seconds

        # the business of the cores is measured in seconds that they will be busy



        # for all clicks, check when the response happens.

        distribution = [0 for i in range(100)] # use 50 as average


        corebusiness = [0.0 for i in range(cores)]
        totalclicks = 0
        totalresponsetime = 0
        for i in range(len(clicktable)):
            for j in range(3600):
                for k in range(clicktable[i][j]):
                    totalclicks+=1
                    indexofminimum = corebusiness.index(min(corebusiness))
                    corebusiness[indexofminimum]+= processtime

                    responsetime = corebusiness[indexofminimum]
                    totalresponsetime+=responsetime
                for k in range(cores):
                    if corebusiness[k]>1:
                        corebusiness[k]-=1.0
                    else:
                        corebusiness[k]=0.0

        averageresponsetime = totalresponsetime/totalclicks
        #print(averageresponsetime)

        totalresponsevar = 0

        corebusiness = [0.0 for i in range(cores)]
        totalclicks = 0
        totalresponsetime = 0
        for i in range(len(clicktable)):
            for j in range(3600):
                for k in range(clicktable[i][j]):
                    totalclicks += 1
                    indexofminimum = corebusiness.index(min(corebusiness))
                    corebusiness[indexofminimum] += processtime

                    responsetime = corebusiness[indexofminimum]
                    totalresponsevar+=pow(responsetime-averageresponsetime,2)
                    totalresponsetime += responsetime
                for k in range(cores):
                    if corebusiness[k] > 1:
                        corebusiness[k] -= 1.0
                    else:
                        corebusiness[k] = 0.0

        responsedeviation = math.sqrt(totalresponsevar/totalclicks)
        #print(averageresponsetime,responsedeviation)

        corebusiness = [0.0 for i in range(cores)]
        totalclicks = 0
        totalresponsetime = 0
        for i in range(len(clicktable)):
            for j in range(3600):
                for k in range(clicktable[i][j]):
                    totalclicks += 1
                    indexofminimum = corebusiness.index(min(corebusiness))
                    corebusiness[indexofminimum] += processtime

                    responsetime = corebusiness[indexofminimum]

                    if int(round((responsetime-averageresponsetime)*(10/responsedeviation)+50))>99:
                        pass#print(int(round((responsetime-averageresponsetime)*(10/responsedeviation)+50)))
                    else:
                        distribution[int(round((responsetime-averageresponsetime)*(10/responsedeviation)+50))]+=1
                    totalresponsetime += responsetime
                for k in range(cores):
                    if corebusiness[k] > 1:
                        corebusiness[k] -= 1.0
                    else:
                        corebusiness[k] = 0.0
        print('distribution: ', distribution)
        print('total clicks',totalclicks, 'average response time:', averageresponsetime,'seconds, std dev: ', responsedeviation)











if __name__ == "__main__":
    run()
