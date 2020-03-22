'''
[Title]

Get Product-Year-Aggregates for Customer Complaints

[Description]

This file:
1. Takes a CSV of customer complaints
2. Groups them by product-year
3. Calculates aggregates for these product-year
4. Orders by product-year & writes this to an output CSV file

[Structuring]

Each code block performs a specific step that was outlined above.
Within each code block are comments to help the reader understand techniques used.
'''

import sys, csv, decimal

# Code block to read the CSV input into a dictionary for aggregating actions

with open(sys.argv[1]) as file: # Opens input file
    reader = csv.reader(file)
    next(reader) # Skips header
    
    d = {}
    for row in reader:
        key = (row[1].lower(), row[0][:4]) # Each key is product-year pair
        company = row[7]
        if key not in d:
            d[key] = {company.lower(): 1} # Each value is a dictionary of companies with this complaint, & how many complaints they got
        else:
            if company.lower() not in d[key]:
                d[key][company.lower()] = 1
            else:
                d[key][company.lower()] += 1

# Code block for aggregate actions

for key in d:                          # For this product-year:
    stats = [0, 0, 0]
    for company in d[key]:
        stats[0] += d[key][company]    # - Number of complaints
        stats[1] += 1                  # - Number of companies complained at
        if stats[2] < d[key][company]: # - Highest number of complaints for one company
            stats[2] = d[key][company]

    # This is to get the highest percentage of complaints for one company.
    # It's using functions to precisely round based on the values Python is able to hold.
    stats[2] = decimal.Decimal(stats[2]/stats[0] * 100).quantize(decimal.Decimal('1'),
                                                                 rounding=decimal.ROUND_HALF_UP)
    d[key] = stats

# Code block to sort, then write to an output file

l = d.items()
l = sorted(l, key = lambda x: int(x[0][1])) # Sort by year
l = sorted(l, key = lambda x: x[0][0]) # Sort by product

with open(sys.argv[2], mode='w') as file: # Opens output file
    writer = csv.writer(file)
    for row in l:                    # For this row, these fields are the:
        writer.writerow([row[0][0],  # - Product
                         row[0][1],  # - Year
                         row[1][0],  # - Number of complaints
                         row[1][1],  # - Number of companies with complaint
                         row[1][2]]) # - Highest percentage of complaints for one company
