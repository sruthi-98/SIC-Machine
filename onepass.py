#Sruthi Suresh

#Python program to implement the first pass of a two pass assembler of a SIC machine

def to_hex(value):
	hex = 0
	k = 0
	value = list(value)
	for i in range(len(value)-1,0,-1):
		hex += int(value[k]) * (16**i)
		k += 1
	return hex

def search_sym(symbol):
	sym = open("symtab.txt","r")
	content = sym.read()
	if(symbol in content):
		return True
	else:
		return False
		
def search_opcode(opcode):
	op = open("optab.txt","r")
	for line in op:
		if(opcode in line):
			return True
	return False
	
def insert(label,locctr):
	sym = open("symtab.txt","a")
	sym.write(label+" "+hex(locctr).lstrip("0x")+"\n")
	
intermediate = "inter.txt"
input_file = raw_input("Enter the input file:");


##							PASS 1 								##
#Finding the starting address 

inp = open(input_file,"r")
firstline = inp.readline()
locctr = firstline.split()
if 'START' in locctr:
	if locctr[len(locctr)-1].isdigit():
		locctr =  locctr[len(locctr)-1]
	else:
		locctr = 0
else:
	locctr = 0
locctr = to_hex(locctr)
start = locctr 

inter = open(intermediate,"r+")
inter.write(hex(start).lstrip("0x")+" "+firstline)

	
symbol,opcode,operand = "","",""
counter = 0

for line in inp:	#Till the end of the program
	if("." not in line):	#If the current line is not a comment line
		if(len(line.split()) == 1): #Only opcode
			symbol,operand = "",""
			opcode = line
		elif(len(line.split()) == 2): #No label
			symbol = ""                                     
			opcode,operand = line.split()
		elif(len(line.split()) == 3):
			symbol,opcode,operand = line.split()

		if(counter):
			locctr += counter
		
		value = hex(locctr).lstrip("0x")+" "+opcode+" "+operand+"\n"
		print(value)
		inter.write(value)
			
		if(symbol != ""):
			found = search_sym(symbol)
			if(found):
				i = 0
				#print("Duplicate symbol found")
			else:
				insert(symbol,locctr)
		
		if(search_opcode(opcode)):
			counter = 3
		#print(counter)
		elif(opcode == "WORD"):
			counter = 3
		elif(opcode == "RESW"):
			counter = 3 * int(operand)
		elif(opcode == "RESB"):
			counter = int(operand)
		elif(opcode == "BYTE"):
			if("C" in operand):
				counter = len(operand)-3
			if("X" in operand):
				counter = (len(operand)-3)/2
		
prgm_len = hex(locctr - start).lstrip("0x")
