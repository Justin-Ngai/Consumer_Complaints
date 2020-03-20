'''
This file takes a CSV of complaints,
gets some statistics on these complaints,
then writes these statistics to an output CSV file.
'''

import sys, csv

# Code block to read CSV & prepare dictionary for aggregate functions

with open(sys.argv[1]) as file: # Opens input file
    reader = csv.reader(file)
    reader.next() # Skips header
    
    d = {}
    for row in reader:
        key = (row[1], row[0][:4]) # Each key is product-year pair
        if key not in d:
            d[key] = {row[7]: 1} # Each value is companies with this complaint
        else:                    # & how many complaints for each of these companies
            if row[7] not in d[key]:
                d[key][row[7]] = 1
            else:
                d[key][row[7]] += 1

# Code block for aggregate functions

for key in d:
    stats = [0, 0, 0]
    for c in d[key]:
        stats[0] += d[key][c] # Recurrence of this complaint
        stats[1] += 1 # Number of companies with this complaint
        if stats[2] < d[key][c]: # The number of complaints for the company with the most complaints
            stats[2] = d[key][c]
    stats[2] = round(float(stats[2])/float(stats[0]) * 100) # CAREFUL! THIS ROUNDS DOWN FOR .5!
    d[key] = stats

# Code block to sort, then write to output file

l = d.items()
l = sorted(l, key = lambda x: int(x[0][1])) # Sort by year
l = sorted(l, key = lambda x: x[0][0]) # Sort by product

with open(sys.argv[2], mode='w') as file: # Open output file
    writer = csv.writer(file)
    for r in l:
        writer.writerow([r[0][0], # Product
                         r[0][1], # Year
                         str(r[1][0]), # Number of complaints
                         str(r[1][1]), # Number of companies with complaint
                         str(r[1][2])]) # Highest percentage of complaints for one company
