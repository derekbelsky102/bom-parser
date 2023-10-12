from bom_parser import Part_Number
from pprint import pprint
import time

bom_file = open('example_bom.txt', 'r')
lines = bom_file.readlines()

for line in lines:
    part_num = line.strip('\n')
    p = Part_Number(part_num)
    if p.error == '':
        print("{0} : {1}".format(part_num, p.operating_temp))
    else:
        print("{0} : {1}".format(part_num, p.error))
#pprint(vars(p))


