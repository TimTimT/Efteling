
import math

if __name__ == '__main__':
    def run():
        return


class Evaluation:
    # what about shows?
    # allow them in regular list.
    # Pick them out because their numbers are known ?
    # They probably have a few viewings. All of them, but only them, should be considered.
    # practically
    #   - Show times are prompted.
    #   - Do we push in the shows?
    #   -

    # what about maintenance/defects? Leave out of list but prompt?


    @staticmethod
    def evaluate(afstandtijdtable,wachttijdentable,duurtijdtable,permutatie,translationtable,location,startuur,showtijdtable,showduration):
        # 1-- [2,5,23,13,9,16,24,8,3,12]
        # 2-- [17,7,11,21,10,19,15,14,20,18]
        # 3-- [22,6,1,4,2,5,23,13,9]
        # 4-- [18,20,21,17,7,11,19,15,14]
        # 5-- [6,22,20,18,23,5,13,9,16]


        totaletijd = startuur
        vorige = location

        pausetime =0
        showsseen = 0
        extrapenalty=0
        for i in permutatie:
            index = translationtable[i]
            totaletijd += afstandtijdtable[vorige][index] / 5

            if showsseen>0:
                extrapenalty+=showsseen*(afstandtijdtable[vorige][index] / 5)
            if index >26:# this is a show!
                shownumber = index%27
                for startingtime in showtijdtable[shownumber]:
                    if totaletijd<startingtime:
                        # take this one.
                        # you could take the total time and leverage the time after any show
                        # why might that not work ?
                        # Because then no objective evaluation would be made when deciding whether to do an
                        # attraction after of before a show..
                        # What else can you do?
                        # take total time as evaluator, penalize for the time spent on attractions after show.
                        # This way, they are preferably done before a show. Penalize heavily?

                        # So. Put show in first following showtime.
                        pausetime+=startingtime - totaletijd
                        totaletijd = startingtime+showduration[shownumber]
                        showsseen+=1

                        break


            if totaletijd>117:
                totaletijd+=20
            else:

                totaletijd += wachttijdentable[index][int(round(totaletijd))]/5

                if showsseen > 0:
                    extrapenalty += showsseen * (wachttijdentable[index][int(round(totaletijd))]/5)

            totaletijd += duurtijdtable[index]/300
            vorige = index

        print((totaletijd-startuur-pausetime+extrapenalty)/12)

        return (totaletijd-startuur-pausetime+extrapenalty)/12

    @staticmethod
    def evaluate2(afstandtijdtable, wachttijdentable, duurtijdtable, permutatie, translationtable, location, startuur,
                 showtijdtable, showduration,indextable):
        # 1-- [2,5,23,13,9,16,24,8,3,12]
        # 2-- [17,7,11,21,10,19,15,14,20,18]
        # 3-- [22,6,1,4,2,5,23,13,9]
        # 4-- [18,20,21,17,7,11,19,15,14]
        # 5-- [6,22,20,18,23,5,13,9,16]


        totaletijd = startuur
        vorige = location

        schedule = []
        pausetime = 0
        showsseen = 0
        extrapenalty = 0
        for i in permutatie:
            index = translationtable[i]
            schedule.append(makeline(getTime(totaletijd),[': wandel ', str(round(afstandtijdtable[vorige][index],2)), ' minuten']))
            #print(makeline(getTime(totaletijd),[': wandel ', str(round(afstandtijdtable[vorige][index])), ' minuten']))
            totaletijd += afstandtijdtable[vorige][index] / 5

            if showsseen > 0:
                extrapenalty += showsseen * (afstandtijdtable[vorige][index] / 5)
            if index > 26:  # this is a show!
                shownumber = index % 27
                for startingtime in showtijdtable[shownumber]:
                    if totaletijd < startingtime:
                        # take this one.
                        # you could take the total time and leverage the time after any show
                        # why might that not work ?
                        # Because then no objective evaluation would be made when deciding whether to do an
                        # attraction after of before a show..
                        # What else can you do?
                        # take total time as evaluator, penalize for the time spent on attractions after show.
                        # This way, they are preferably done before a show. Penalize heavily?

                        # So. Put show in first following showtime.
                        pausetime += startingtime - totaletijd
                        totaletijd = startingtime + showduration[shownumber]
                        showsseen += 1

                        break

            if totaletijd > 117:
                totaletijd += 20
            else:
                schedule.append(
                    makeline(getTime(totaletijd),[': wacht ', str(round(wachttijdentable[index][int(round(totaletijd))],2)), ' minuten']))
                totaletijd += wachttijdentable[index][int(round(totaletijd))] / 5

                if showsseen > 0:
                    extrapenalty += showsseen * (wachttijdentable[index][int(round(totaletijd))] / 5)
            schedule.append(
                makeline(getTime(totaletijd),
                    [': Joepi! ', str(round(duurtijdtable[index] / 60,2)), ' minuten op de ', str(indextable[index])]))
            totaletijd += duurtijdtable[index] / 300
            vorige = index
        for l in schedule:
            print(''.join(l))

        print((totaletijd-startuur-pausetime)/12,permutatie)
        return (totaletijd - startuur - pausetime + extrapenalty) / 12
def makeline(a,b):
    for i in b:
        a.append(i)
    return a
def getTime(uur):
    achtdertig = 102 *5
    minutentijd = uur*5
    totalhourinminutes = achtdertig+minutentijd
    hour = totalhourinminutes//60
    minutes = totalhourinminutes%60
    if len(str(int(minutes))) == 1:
        minutes = '0'+str(int(minutes))
    else:
        minutes = str(int(minutes))
    return [str(int(hour)),'h',minutes]


if __name__ == "__main__":
    run()





