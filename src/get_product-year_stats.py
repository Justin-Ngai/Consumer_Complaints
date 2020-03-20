'''
This file takes a CSV of complaints,
gets some statistics on these complaints,
then writes these statistics to an output CSV file.
'''

import sys, csv

# Code block to read CSV into a dictionary for aggregate functions

with open(sys.argv[1]) as file: # Opens input file
    reader = csv.reader(file)
    next(reader) # Skips header
    
    d = {}
    for row in reader:
        key = (row[1].lower(), row[0][:4]) # Each key is product-year pair
        company = row[7]
        if key not in d:
            d[key] = {company.lower(): 1} # Each value is companies with this complaint & how many complaints for each of these companies
        else:
            if company.lower() not in d[key]:
                d[key][company.lower()] = 1
            else:
                d[key][company.lower()] += 1

# Code block for aggregate functions

for key in d:
    stats = [0, 0, 0]
    for company in d[key]:
        stats[0] += d[key][company] # Recurrence of this complaint
        stats[1] += 1 # Number of companies with this complaint
        if stats[2] < d[key][company]: # Highest number of complaints for one company
            stats[2] = d[key][company]
    stats[2] = round(stats[2]/stats[0] * 100) # Writing as percentage of total compaints
    d[key] = stats

# Code block to sort, then write to output file

l = d.items()
l = sorted(l, key = lambda x: int(x[0][1])) # Sort by year
l = sorted(l, key = lambda x: x[0][0]) # Sort by product

with open(sys.argv[2], mode='w') as file: # Open output file
    writer = csv.writer(file)
    for row in l:
        writer.writerow([row[0][0], # Product
                         row[0][1], # Year
                         row[1][0], # Number of complaints
                         row[1][1], # Number of companies with complaint
                         row[1][2]]) # Highest percentage of complaints for one company
