class Capacitor:
	def __init__(self, size, voltage_rate, dielectric, capacitance_code, tolerance_code):
		self.size = size;  # Ex: 0201, 0402
		self.voltage_rate = voltage_rate; # Ex: 4V 6.3V
		self.dielectric = dielectric; # Ex: X7R, C0G
		self.capacitance_code = capacitance_code; # Ex: 226 (22uF)
		self.tolerance_code = tolerance_code; # 1% 

def avx_parser(CAP_NAME):
	size = CAP_NAME[0:4]
	voltage_code = CAP_NAME[4]
	dielectric_code = CAP_NAME[5]
	capacitance_code = CAP_NAME[6:9]
	tolerance_code = CAP_NAME[9]

	voltage_value_dict = {
	'4': "4V",
	'6': "6.3V",
	'Z': "10V",
	'Y': "16V",
	'3': "25V",
	'5': "50V",
	'1': "100V",
	'2': "200V",
	'7': "500V",
	}

	dielectric_value_dict = {
	"C": "X7R",
	"D": "X5R"
	}
	
	dielectric = dielectric_value_dict[dielectric_code]
	voltage_rate = voltage_value_dict[voltage_code]
	return Capacitor(size, voltage_rate, dielectric, capacitance_code, tolerance_code)
	
def kemet_parser(CAP_NAME):
	size = CAP_NAME[1:5]
	capacitance_code = CAP_NAME[6:9]
	tolerance_code = CAP_NAME[9]
	voltage_code = CAP_NAME[10]
	dielectric_code = CAP_NAME[11]

	dielectric_value_dict = {
	"R": "X7R",
	"P": "X5R",
	"G": "C0G"
	}
	
	dielectric = dielectric_value_dict[dielectric_code]
	
	if dielectric == "X7R":
		voltage_value_dict = {
		'9': "6.3V",
		'8': "10V",
		'4': "16V",
		'3': "25V",
		'6': "35V",
		'5': "50V",
		'1': "100V",
		'2': "200V",
		'A': "250V"
		}
	elif dielectric == "X5R":
		voltage_value_dict = {
		'7': "4V",
		'9': "6.3V",
		'8': "10V",
		'4': "16V",
		'3': "25V",
		'6': "35V",
		'5': "50V" 
		}
	elif dielectric == "C0G":
		voltage_value_dict = {
		'8': "10V", 
		'4': "16V",
		'3': "25V",
		'5': "50V",
		'1': "100V",
		'2': "200V",
		'A': "250V",
		}
		
	voltage_rate = voltage_value_dict[voltage_code]
	
	return Capacitor(size, voltage_rate, dielectric, capacitance_code, tolerance_code)
	
def tdk_parser(CAP_NAME):
	size_code = CAP_NAME[3]
	thickness = CAP_NAME[4] #maybe add later
	dielectric_code = CAP_NAME[6:9]
	voltage_code = CAP_NAME[9:11]
	capacitance_code = CAP_NAME[11:14]
	tolerance_code = CAP_NAME[14]

	size_code_dict = {
		'1' : "0201",
		'2' : "0402",
		'3' : "0603",
		'4' : "0805",
		'5' : "1206",
		'6' : "1210",
		'8' : "1812",
		'9' : "2220"
	}
	
	voltage_value_dict = {
		'0E' : '2.5V',
		'0G' : '4V',
		'0J' : '6.3V',
		'1A' : '10V',
		'1C' : '16V',
		'1E' : '25V',
		'1V' : '35V',
		'1H' : '50V',
		'1N' : '75V'
	}
	
	size = size_code_dict[size_code]
	dielectric = dielectric_code
	voltage_rate = voltage_value_dict[voltage_code]
	
	return Capacitor(size, voltage_rate, dielectric, capacitance_code, tolerance_code)
	
def samsung_parser(CAP_NAME):
	size_code = CAP_NAME[2:4]
	dielectric_code = CAP_NAME[4]
	capacitance_code = CAP_NAME[5:8]
	tolerance_code = CAP_NAME[8]
	voltage_code = CAP_NAME[9]
	thickness = CAP_NAME[10]
	
	size_code_dict = {
		'R1' : "008004",
		'02' : "01005",
		'03' : "0201",
		'05' : "0402",
		'10' : "0603",
		'21' : "0805",
		'31' : "1206",
		'32' : "1210",
		'42' : "1808",
		'43' : "1812",
		'55' : "2220",
		'L5' : "0204",
		'L6' : "0304",
		'01' : "0306",
		'19' : "0503"
	}
	
	dielectric_value_dict = {
		"A" : "X5R",
		"X" : "X6S",
		"W" : "X6T",
		"B" : "X7R",
		"K" : "X7R(S)",
		"Y" : "X7S",
		"Z" : "X7T",
		"F" : "Y5V",
		"M" : "X8M",
		"E" : "X8L",
		"J" : "JIS-B"
	}
	
	voltage_value_dict = {
		'S' : '2.5V',
		'R' : '4.0V',
		'Q' : '6.3V',
		'P' : '10V',
		'O' : '16V',
		'A' : '25V',
		'L' : '35V',
		'B' : '50V',
		'C' : '100V',
		'D' : '200V',
		'E' : '250V',
		'F' : '350V',
		'G' : '500V',
		'H' : '630V',
		'I' : '1kV',
		'J' : '2kV',
		'K' : '3kV'
	}
	
	size = size_code_dict[size_code]
	dielectric = dielectric_value_dict[dielectric_code]
	voltage_rate = voltage_value_dict[voltage_code]
	
	p1 = Capacitor(size, voltage_rate, dielectric, capacitance_code, tolerance_code)
	print(p1.size)
	return p1
# Capacitor name parser
MANUF=""

print("Enter a capacitor manufacturing P/N")
CAP_NAME=input()

if len(CAP_NAME) < 12:
	print("This isn't a valid Capacitor P/N")
	exit()
else:
	if CAP_NAME[0:2] == "CL":
		MANUF = "SAMSUNG"
	elif CAP_NAME[0:3] == "CGA":
		MANUF = "TDK"
	elif CAP_NAME[0] == 'C' and CAP_NAME[5] == 'C':
		MANUF = "KEMET"
	elif CAP_NAME[10:12] == "AT":
		MANUF = "AVX"

if MANUF == "AVX":
	cap = avx_parser(CAP_NAME)
	
elif MANUF == "KEMET":
	cap = kemet_parser(CAP_NAME)
		
elif MANUF == "TDK":
	cap = tdk_parser(CAP_NAME)
		
elif MANUF == "SAMSUNG":
	cap = samsung_parser(CAP_NAME)
	

# if + or - isn't there assume it is +/-
# TODO: this is broken for Samsung values < 10pF : F should be +/-1pF
tolerance_value_dict = {
'N': "0.03pF",
'A': "0.05pF",
'B': "0.10pF",
'C': "0.25pF",
'H': "+0.25pF",
'L': "-0.25pF",
'D': "0.5pF",
'F': "1%",
'G': "2%",
'J': "5%",
'U': "+5%",
'V': "-5%",
'K': "10%",
'M': "20%",
'Z': "-20,+80%"
}

tolerance = tolerance_value_dict[cap.tolerance_code]
capacitance_value=int(cap.capacitance_code[0:2])*(10**int(cap.capacitance_code[2]))*1e-12

# Size is given in inches
print("Manufacturer  "+MANUF)
print("Size:         "+cap.size)
print("Voltage Code: "+cap.voltage_rate)
print("Dielectric:   "+cap.dielectric)
print("Capacitance:  "+str(capacitance_value))
print("Tolerance:    "+tolerance)



