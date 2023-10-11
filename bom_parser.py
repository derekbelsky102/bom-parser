import json
import os
from pathlib import Path
import re
import platform

import digikey
from digikey.v3.productinformation import KeywordSearchRequest
from digikey.v3.batchproductdetails import BatchProductDetailsRequest

# Call Digikey PN and get json string result. 
def digikey_manuf_search(x):
    CACHE_DIR = ''

    if platform.system() == "Windows":
        os.system("mkdir path\\to\\cache\\dir")
        CACHE_DIR = "path/to/cache/dir"
    if platform.system() == "Linux":
        os.system("mkdir -p path/to/cache/dir")
        CACHE_DIR = "path/to/cache/dir"

    os.environ['DIGIKEY_CLIENT_ID'] = 'zoMDIPlwJAJ2BDzAP8AfNrYtxzGutIAz'
    os.environ['DIGIKEY_CLIENT_SECRET'] = 'VSNvHwtEA2vUlQPE'
    os.environ['DIGIKEY_CLIENT_SANDBOX'] = 'False'
    os.environ['DIGIKEY_STORAGE_PATH'] = CACHE_DIR


    # Search for parts
    search_request = KeywordSearchRequest(keywords=x, record_count=1)
    result = digikey.keyword_search(body=search_request)
    return str(result)

# Json File needs some parsing before it is ready to parse through
def format_json_file(string):
    formatted_result = string.replace('"', '\\"')
    formatted_result = formatted_result.replace('\'', '"')
    formatted_result = formatted_result.replace('None', '"None"')
    formatted_result = formatted_result.replace('False', '"False"')

    space_form_result =  []
    combined_line = ''
    for line in formatted_result.splitlines():
        if(line[-1] == ','):
            if(combined_line != ''):
                combined_line = combined_line + line.strip().replace('"', '').replace(',', '') + '",' 
                space_form_result.append(combined_line+"\n")
                #print(combined_line)
                combined_line = ''
            else:
                space_form_result.append(line+"\n")
        else:
            if(combined_line == ''):
                combined_line = line[:-1] #need to remove last quote
            else:
                combined_line = combined_line + line.strip().replace('"', '')
    space_form_result.append(line+"\n")
            
    return ''.join(space_form_result)
          

class Part_Number:
    def __init__(self, part_number):
        pre_format_json = digikey_manuf_search(part_number)
        formatted_json = format_json_file(pre_format_json)
        #print(formatted_json)

        try:
            part_num_info = json.loads(formatted_json)

            self.part_number = part_number
            self.description = part_num_info["exact_manufacturer_products"][0]["product_description"]
            self.manufacturer = part_num_info["exact_manufacturer_products"][0]["manufacturer"]['value']
            self.part_type = part_num_info["exact_manufacturer_products"][0]["category"]["value"]

            self.value = ""
            self.tolerance = ""
            self.power = ""
            self.package = ""
            self.voltage_rate = ""
            self.dieletric = ""
            self.error = ""
            self.operating_temp = ""

            parameters =  part_num_info["exact_manufacturer_products"][0]["parameters"]
            # Grab general parameters
            for line in parameters:
                if line["parameter"] == "Operating Temperature":
                    self.operating_temp = line["value"]
                if line["parameter"] == "Package / Case":
                    self.package = line["value"]
            # Specific Parameters
            if self.part_type == 'Resistors':
                for line in parameters:
                    if line["parameter"] == "Resistance":
                        self.value = line["value"]
                    if line["parameter"] == "Tolerance":
                        self.tolerance = line["value"]
                    if line["parameter"] == "Power (Watts)":
                        self.power = line["value"]
            if self.part_type == 'Capacitors':
                parameters =  part_num_info["exact_manufacturer_products"][0]["parameters"]
                for line in parameters:
                    if line["parameter"] == "Capacitance":
                        self.value = line["value"]
                    if line["parameter"] == "Tolerance":
                        self.tolerance = line["value"]
                    if line["parameter"] == "Temperature Coefficient":
                        self.dieletric = line["value"]
                    if line["parameter"] == "Voltage - Rated":
                        self.voltage_rate = line["value"]
        except:
            self.error = "No Parameters Extracted"
        
    




