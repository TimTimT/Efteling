
import math



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
    def evaluate(afstandtijdtable,wachttijdentable,duurtijdtable,permutatie,translationtable):
        starttijd = 0 # units -> 5 minuten
        totaletijd = 0
        vorige = None
        print(len(permutatie))
        for i in permutatie:
            index = translationtable[i]
            if vorige != None:
                totaletijd+= afstandtijdtable[vorige][index]/5
            else:
                totaletijd+= afstandtijdtable[0][index]/5

            if totaletijd>117:
                totaletijd+=20
            else:
                totaletijd += wachttijdentable[index][int(round(totaletijd))]/5

            totaletijd += duurtijdtable[index]/300
            vorige = index
        print('totale tijd:',str(totaletijd/30)+str('hrs'))
        return totaletijd/30








