from bom_parser import Part_Number
from pprint import pprint
import time
import pandas as pd
import csv
import openpyxl

def export_csv(input_file, output_file):

    bom_file = open(input_file, 'r')
    lines = bom_file.readlines()  
        
    # field names 
    top_fields = ['General Part Attributes', '', '', '', '', '', '', '', \
    'Passives Specific', '', 'Resistor Specific', 'Capacitor Specific', '']
    desc_fields = ['Part Name Requested', 'Part Number Returned', 'Error', 'Part Type', \
    'Description', 'Manufacturer', 'Operating Temp', 'Package', 'Value', 'Tolerance', 'Power', 'Voltage Rating', 'Dieletric'] 

    # writing to csv file  
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:  
        # creating a csv writer object  
        csvwriter = csv.writer(csvfile)  
            
        # writing the fields  
        csvwriter.writerow(top_fields)
        csvwriter.writerow(desc_fields)

        for line in lines:
            part_num = line.strip('\n')
            p = Part_Number(part_num)
            print("Processing ", part_num)
            list = [part_num, p.part_number, p.error, p.part_type, \
            p.description, p.manufacturer, p.operating_temp, p.package, p.value, p.tolerance, \
            p.power, p.voltage_rate, p.dieletric]
            csvwriter.writerow(list)
            
input_file = 'example_bom.txt'
output_file = 'example_output.csv'
output_excel_file = 'output_bom.xlsx'
export_csv(input_file, output_file)

# Convert to xlsx for conditional formatting
df = pd.read_csv(output_file, encoding='utf-8')
df.to_excel(output_excel_file, index=None, header=True)


