import time
import serial
ser = serial.Serial('/dev/ttyUSB0', 115200)

def generate_CHKSUM(command):
	#print(*command)
	#print(len(command))
	for x in range(len(command)):
		if (x == 0):
			result = command[x]^command[x+1]
			#print(result)
		elif(x >= 2):
			result = result^command[x]
			#print(result)
	return result

for x in range(8):
	command = bytearray(b'\x01\x0A')
	if(x == 1):
		command.append(1)
	elif(x == 2):
		command.append(2)
	elif(x == 3):
		command.append(3)
	elif(x == 4):
		command.append(4)
	elif(x == 5):
		command.append(5)
	elif(x == 6):
		command.append(6)
	elif(x == 7):
		command.append(7)
	command.extend([0,0])
	CHKSUM = generate_CHKSUM(command)
	command.append(CHKSUM)
	
	if(x != 0):
		print(command)
		ser.write(command)
		response = ser.read()
		print(response)
	time.sleep(3)
	

command = bytearray(b'\x01\x0A\x01\x00\x00\x00')
ser.write(command)
