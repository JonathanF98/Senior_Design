command = bytearray(b'\x0A\x01\x05\x09')
exclusive = command
print(*command)
print(len(command))
for x in range(len(exclusive)):
	if (x == 0):
		result = exclusive[x]^exclusive[x+1]
		print(result)
	elif(x >= 2):
		result = result^exclusive[x]
		print(result)
		
print(result)
command.append(result)
print(command)

for x in range(len(command)):
	if (x == 0):
		result2 = exclusive[x]^exclusive[x+1]
		print(result2)
	elif(x >= 2):
		result2 = result2^exclusive[x]
		print(result2)
print(result2)
