from bom_parser import Part_Number
from pprint import pprint

bom_file = open('example_bom.txt', 'r')
lines = bom_file.readlines()
for line in lines:
    p = Part_Number(line.strip('\n'))
    pprint(vars(p))


