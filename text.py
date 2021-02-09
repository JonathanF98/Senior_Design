import serial
import time
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=None)

def generate_CHKSUM(command):
	for x in range(len(command)):
		if (x == 0):
			result = command[x]^command[x+1]
		elif(x >= 2):
			result = result^command[x]
	return result

command = bytearray(b'\x01\x0A')
command.append(2)
command.extend(bytearray(b'\x00\x00'))
CHKSUM = generate_CHKSUM(command)
command.append(CHKSUM)
ser.write(command)
response = ser.read()
print(command)
print(response)


message = "Sui-chan best girl"
index = bytearray(b'\x00')

command = bytearray(b'\x02')
command.extend(index)
command.append(len(message))
command.extend(message.encode("ascii"))
command.append(generate_CHKSUM(command))
ser.write(command)
response = ser.read()
print(command)
print(response)
