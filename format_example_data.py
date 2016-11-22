import csv




if __name__ == '__main__':
    def run():

        f = open('input_example_to_format(tem4012).csv','r')
        tabletowrite = []
        reader = csv.reader(f,delimiter=';')
        count = 0
        last = ''
        rowintable = 0
        columnintable = -1
        listofnames = []
        for row in reader:
            print(row)
            rowintable+=1
            if count>0:
                if row[3] == last:
                    tabletowrite[columnintable].append(row[6])
                else:
                    listofnames.append(row[3])
                    rowintable = 0
                    columnintable += 1
                    tabletowrite.append([0])
                    tabletowrite[columnintable][0]= row[6]



            last = row[3]
            count+=1
            if count == 4013:
                break
        print(tabletowrite)


        # print diene table in e nieuw, je mag weer kommatjes omzettn.
        g = open('formatted_example_average_waiting_time_data.csv', 'w')
        writer = csv.writer(g)
        writer.writerow(listofnames)
        for r in tabletowrite:
            actuallisttowrite= []
            for k in r:
                actuallisttowrite.append(k.replace(',','.'))
            #print(actuallisttowrite)
            writer.writerow(actuallisttowrite)
            print(len(actuallisttowrite))



if __name__ == "__main__":
    run()

