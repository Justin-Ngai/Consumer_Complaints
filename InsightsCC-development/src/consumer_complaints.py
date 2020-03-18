import sys
input = sys.argv[1]
print(input)

with open(input) as file:
    for line in file:
        print(line)

output = sys.argv[2]
with open(output, mode='w') as file:
    file.write('line 1\n')
    file.write('line 2\n')
