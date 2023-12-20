import json
import os
from pathlib import Path
import re
import platform
import ast

import digikey
from digikey.v3.productinformation import KeywordSearchRequest
from digikey.v3.batchproductdetails import BatchProductDetailsRequest

# Call Digikey PN and get json string result. 
def digikey_manuf_search(x):
    CACHE_DIR = 'path/to/cache/dir'

    os.environ['DIGIKEY_CLIENT_ID'] = 'zoMDIPlwJAJ2BDzAP8AfNrYtxzGutIAz'
    os.environ['DIGIKEY_CLIENT_SECRET'] = 'VSNvHwtEA2vUlQPE'
    os.environ['DIGIKEY_CLIENT_SANDBOX'] = 'False'
    os.environ['DIGIKEY_STORAGE_PATH'] = CACHE_DIR


    # Search for parts
    search_request = KeywordSearchRequest(keywords=x, record_count=1)
    result = digikey.keyword_search(body=search_request)
    return str(result)

class Part_Number:
    def __init__(self, part_number):
        pre_format_json = digikey_manuf_search(part_number)
        
        self.part_number = ""
        self.part_type = ""
        self.description = ""
        self.manufacturer = ""
        self.value = ""
        self.tolerance = ""
        self.power = ""
        self.package = ""
        self.voltage_rate = ""
        self.dieletric = ""
        self.error = ""
        self.operating_temp = ""
        
        try:
            part_num_info = ast.literal_eval(pre_format_json)
            try:
                #  Digikey routes to alternatives sometimes. Check for alternatives
                if part_num_info["exact_manufacturer_products"]:
                    part_num_product_type = part_num_info["exact_manufacturer_products"][0]
                else:
                    part_num_product_type = part_num_info["products"][0]
                
                self.part_number = part_num_product_type["manufacturer_part_number"]
                self.description = part_num_product_type["product_description"]
                self.manufacturer = part_num_product_type["manufacturer"]['value']
                self.part_type = part_num_product_type["category"]["value"]
                
                parameters =  part_num_product_type["parameters"]
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
                self.error = "No Parameters Returned"
        except:
            self.error = "Formatting Issue in Digikey Data"




