#Sruthi Suresh

#Python program to implement the second pass of a two pass assembler of a SIC machine

from onepass import *

def ifrecordfull(current,inc):
	if(current <= 30 and current+inc > 30):
		return True
	return False

output = "output.txt"
input_file = raw_input("Enter the intermediate file:");

inp = open(input_file,"r")
out = open(output,"a")

firstline = inp.readline()
strt,prgm_name,opcode,operand = firstline.split()
out.write("H^"+prgm_name+"^"+strt+"^"+prgm_len+"\n")
out.write("T^")

max_len = 30	#maximum length of a text record in bytes
count = 0	#to maintain the length of a text record
code = ""   
line_ = ""

for line_ in inp.readlines():
	if("END" in line_.split()):						#END of file
		out.write(strt+"^"+hex(count).lstrip("0x")+"^"+code+"\n")
		line = line_.split()
		start = line[len(line)-1]
		symtab = open("symtab.txt","r")
		out = open(output,"a")
		for line1 in symtab:						#writing END record
			if(start in line1):
				addr = line1.strip(start).strip()
				length = len(addr)
				if(length < 6):
					length = 6-length
					value = "0" * length
					addr = value + addr
				out.write("E^"+addr)
		out.close()

	opcode_not_found = 1
	operand_not_found = 1

	optab = open("optab.txt","r")
	symtab = open("symtab.txt","r")

	if("." not in line_):	#not a comment line
		length = len(line_.split())
		if(length == 3):
			addr,opcode,operand = line_.split()
		if(length == 2):
			addr,opcode = line_.split()
			
		for line1 in optab.readlines():
			if(opcode in line1.split()):
				opcode_not_found = 0
				if(code == "" and count == 0):
					strt = addr
				if(ifrecordfull(count,3)):
					out.write(strt+"^"+hex(count).lstrip("0x")+"^"+code+"\n"+"T^")
					count = 0
					code = ""
					strt = addr
				code += line1.strip(opcode).strip()
				count += 1	#adding 1 byte for opcode
				
		for line2 in symtab.readlines():
			if(operand in line2.split() and opcode != "RSUB"):
				operand_not_found = 0
				code += line2.strip(operand).strip()
				count += 2
				code += "^"
			if(",X" in line_ and operand.strip(",X") in line2.split()):	#indexed addressing
				operand_not_found = 0
				operand = operand.strip(",X")
				value = hex(32768 + int(line2.strip(operand).strip(),16)).lstrip("0x") + "^"
				code += value
				count += 2
				
		if(opcode_not_found):
			operand_not_found = 0
			if(opcode == "RESW" or opcode == "RESB"):
				if(count != 0):
					out.write(strt+"^"+hex(count).lstrip("0x")+"^"+code+"\n"+"T^")
				count = 0
				code = ""
				strt = addr
			if(opcode == "BYTE"):
				if("X" in operand):
					operand = operand.strip("X").strip("'")
					if(ifrecordfull(count,len(operand)/2)):
						out.write(strt + "^"+hex(count).lstrip("0x")+"^"+code+"\n"+"T^")
						count = 0
						code = ""
						strt = addr
					code += operand
					count += len(operand)/2
				if("C" in operand):
					operand = operand.strip("C").strip("'")
					if(ifrecordfull(count,len(operand))):
						out.write(strt + "^"+hex(count).lstrip("0x")+"^"+code+"\n"+"T^")
						count = 0
						code = ""							
						strt = addr
					count += len(operand)
					for letter in operand:
						code += hex(ord(letter)).lstrip("0x")
				code += "^"
			if(opcode == "WORD"):
				if(ifrecordfull(count,3)):
					out.write(strt + "^"+hex(count).lstrip("0x")+"^"+code+"\n"+"T^")
					count = 0
					code = ""
					strt = addr
				value = hex(int(operand)).lstrip("0x")
				length = len(value)
				if(length < 6):
					length = 6 - length
					constant = "0" * length 
					code += constant
				code += value
				count += 3
				code += "^"

		if(operand_not_found):
			code += "0000^"
			count += 2
		
