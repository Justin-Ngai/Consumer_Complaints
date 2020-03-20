import sys, csv

#Code block to read CSV file & prepare a dictionary for aggregation functions

i = sys.argv[1] #input file
with open(i) as file: #opens input file
    reader = csv.reader(file)
    reader.next() #skips header
    d = {}
    for row in reader:
        index = (row[1], row[0][:4])
        if index not in d:
            d[index] = {row[7]: 1}
        else:
            if row[7] not in d[index]:
                d[index][row[7]] = 1
            else:
                d[index][row[7]] += 1

#Code block for aggregation functions

for k in d:
    l = [0, 0, 0]
    for c in d[k]:
        l[0] += d[k][c] #num complaints
        l[1] += 1 #num companies
        if l[2] < d[k][c]: # highest count
            l[2] = d[k][c]
    l[2] = round(float(l[2])/float(l[0]) * 100) #CAREFUL, THIS ROUNDS DOWN FOR .5
    d[k] = l

#Code block to order the data & prepare for writing to output file
l = d.items()
l = sorted(l, key = lambda x: int(x[0][1])) #Sort by year
l = sorted(l, key = lambda x: x[0][0]) #Sort by product


o = sys.argv[2] #output
with open(o, mode='w') as file:
    writer = csv.writer(file)
    for r in l:
        writer.writerow([r[0][0],
                         r[0][1],
                         str(r[1][0]),
                         str(r[1][1]),
                         str(r[1][2])])
