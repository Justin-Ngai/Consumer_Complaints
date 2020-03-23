'''
[Header]

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

# Code block to read the CSV input into a dictionary, for aggregating actions.

with open(sys.argv[1]) as file: # Opens input file
    reader = csv.reader(file)
    next(reader) # Skips header
    
    product_years = {} # Dictionary with product-year keys, & values being the companies with a number of complaints for these product-year's.
    for row in reader:

        if not row[0][:4].isnumeric(): # Graceful handling of date with wrong format
            raise TypeError('''
One or more rows has 'Date Received' that doesn't start with 4 digits for YYYY.
Please ensure that all rows have 'Date Received' starting with 4 digits for YYYY.
''')
        product_year = (row[1].lower(), row[0][:4])            # Each key is a product-year pair
        company = row[7]
        if product_year not in product_years:
            product_years[product_year] = {company.lower(): 1} # Each value is a dictionary of companies with this complaint, & how many complaints they got
        else:
            if company.lower() not in product_years[product_year]:
                product_years[product_year][company.lower()] = 1
            else:
                product_years[product_year][company.lower()] += 1

# Code block for aggregating actions

for product_year in product_years:                          # For this product-year:
    stats = [0, 0, 0]
    for company in product_years[product_year]:
        stats[0] += product_years[product_year][company]    # - Number of complaints
        stats[1] += 1                                       # - Number of companies complained at
        if stats[2] < product_years[product_year][company]: # - Highest number of complaints for one company
            stats[2] = product_years[product_year][company]

    # The below functions get the highest percentage of complaints (for this product-year) for one company.
    # The functions precisely round based on how precise a value Python can store.
    stats[2] = decimal.Decimal(stats[2]/stats[0] * 100).quantize(decimal.Decimal('1'),
                                                                 rounding=decimal.ROUND_HALF_UP)
    product_years[product_year] = stats

# Code block to sort, then write to an output file

prod_year_list = product_years.items()
prod_year_list = sorted(prod_year_list, key = lambda x: int(x[0][1])) # Sort by year
prod_year_list = sorted(prod_year_list, key = lambda x: x[0][0]) # Sort by product

with open(sys.argv[2], mode='w') as file: # Opens output file
    writer = csv.writer(file)
    for row in prod_year_list:       # For this row, the fields written are:
        writer.writerow([row[0][0],  # - Product
                         row[0][1],  # - Year
                         row[1][0],  # - Number of complaints
                         row[1][1],  # - Number of companies with complaint
                         row[1][2]]) # - Highest percentage of complaints for one company
