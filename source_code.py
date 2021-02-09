# Possible shebang would go here

############################# IMPORTS & GLOBALS ################################
import subprocess as sp
import serial			          # imports pySerial for comm with LCD
import RPi.GPIO as GPIO		# imports RPi.GPIO_NP to talk with GPIO pins
import time
ser = serial.Serial('/dev/ttyS1', 115200)
currentForm = 0					    # global variable that should follow the current LCD screen form
													# Make sure to keep track of this value as it will change
													# between functions
# FORM 0 INDEX
FORM_0_INDEX			= bytearray(b'\x00')
# FORM 1 INDEXES
FORM_1_INDEX			= bytearray(b'\x01')			# replace "index with hex code such as 00,01,1B, ETC."
NETWORK_DETECT_LED		= bytearray(b'\x00')
RF_DETECT_LED 			= bytearray(b'\x01')
FORM1_EXIT_LED 		  	= bytearray(b'\x02')
# FORM 2 INDEXES
FORM_2_INDEX			= bytearray(b'\x02')
NETWORK_STRING_0		= bytearray(b'\x00')
NETWORK_STRING_1	  	= bytearray(b'\x01')
NETWORK_STRING_2		= bytearray(b'\x02')
NETWORK_STRING_3		= bytearray(b'\x03')
NETWORK_STRING_4		= bytearray(b'\x04')
NETWORK_LED_0			= bytearray(b'\x03')
NETWORK_LED_1			= bytearray(b'\x04')
NETWORK_LED_2			= bytearray(b'\x05')
NETWORK_LED_3			= bytearray(b'\x06')
NETWORK_LED_4			= bytearray(b'\x07')
# FORM 3 INDEXES
FORM_3_INDEX			= bytearray(b'\x03')
ENTER_KEY_LED			= bytearray(b'\x14')
KEYPAD_LED_0			= bytearray(b'\x08')
KEYPAD_LED_1			= bytearray(b'\x09')
KEYPAD_LED_2			= bytearray(b'\x0A')
KEYPAD_LED_3			= bytearray(b'\x0B')
KEYPAD_LED_4			= bytearray(b'\x0C')
KEYPAD_LED_5			= bytearray(b'\x0D')
KEYPAD_LED_6			= bytearray(b'\x0E')
KEYPAD_LED_7			= bytearray(b'\x0F')
KEYPAD_LED_8			= bytearray(b'\x10')
KEYPAD_LED_9			= bytearray(b'\x11')
KEYPAD_LED_10			= bytearray(b'\x12')
KEYPAD_LED_11			= bytearray(b'\x13')
PASSWORD_STRING			= bytearray(b'\x05')
# FORM 4 INDEXES
FORM_4_INDEX			= bytearray(b'\x04')
MAC_ADDRESS_STRING_0	= bytearray(b'\x06')
DEVICE_STRING_0			= bytearray(b'\x07')
MAC_ADDRESS_STRING_1	= bytearray(b'\x08')
DEVICE_STRING_1			= bytearray(b'\x09')
MAC_ADDRESS_STRING_2	= bytearray(b'\x0A')
DEVICE_STRING_2			= bytearray(b'\x0B')
NEXT_FORM_LED_0			= bytearray(b'\x15')

# FORM 5 INDEXES
FORM_5_INDEX			= bytearray(b'\x05')
MAC_ADDRESS_STRING_3	= bytearray(b'\x0C')
DEVICE_STRING_3			= bytearray(b'\x0D')
MAC_ADDRESS_STRING_4	= bytearray(b'\x0E')
DEVICE_STRING_4			= bytearray(b'\x0F')
MAC_ADDRESS_STRING_5	= bytearray(b'\x10')
DEVICE_STRING_5			= bytearray(b'\x11')
NEXT_FORM_LED_1 		= bytearray(b'\x16')

# FORM 6 INDEXES
FORM_6_INDEX			= bytearray(b'\x06')
MAC_ADDRESS_STRING_6	= bytearray(b'\x12')
DEVICE_STRING_6			= bytearray(b'\x13')
MAC_ADDRESS_STRING_7	= bytearray(b'\x14')
DEVICE_STRING_7			= bytearray(b'\x15')
MAC_ADDRESS_STRING_8	= bytearray(b'\x16')
DEVICE_STRING_8			= bytearray(b'\x17')
NEXT_FORM_LED_2			= bytearray(b'\x17')

# FORM 7 INDEXES
FORM_7_INDEX			= bytearray(b'\x07')
PROXIMITY_LED_0			= bytearray(b'\x18')
PROXIMITY_LED_1			= bytearray(b'\x19')
PROXIMITY_LED_2			= bytearray(b'\x1A')
PROXIMITY_LED_3			= bytearray(b'\x1B')
LED_DIGITS_0			= bytearray(b'\x00')
ELIPSES_STRING			= bytearray(b'\x18')

############################# FUNCTION - DEFINITIONS ################################

#############################
# Helper Functions For Modes
#############################


def ok_button_pressed():
	if GPIO.input(4):
		time.sleep(0.3)
		return 1
	else:
		return 0


def up_button_pressed():
	if GPIO.input(10):
		time.sleep(0.3)
		return 1
	else:
		return 0


def down_button_pressed():
	if GPIO.input(18):
		time.sleep(0.3)
		return 1
	else:
		return 0


def left_button_pressed():
	if GPIO.input(11):
		time.sleep(0.3)
		return 1
	else:
		return 0


def right_button_pressed():
	if GPIO.input(14):
		time.sleep(0.3)
		return 1
	else:
		return 0


def generate_CHKSUM(command):
	for x in range(len(command)):
		if (x == 0):
			result = command[x]^command[x+1]
		elif(x >= 2):
			result = result^command[x]
	return result


def led_on(LED):
	command = bytearray(b'\x01\x13')
	command.extend(LED)
	command.extend(b'\x00\x01')
	CHKSUM = generate_CHKSUM(command)
	command.append(CHKSUM)
	ser.write(command)
	response = ser.read()
	print(response)


def led_off(LED):
	command = bytearray(b'\x01\x13')
	command.extend(LED)
	command.extend(b'\x00\x00')
	CHKSUM = generate_CHKSUM(command)
	command.append(CHKSUM)
	ser.write(command)
	response = ser.read()
	print(response)


def default_keypad_state():
	led_off(KEYPAD_LED_0)
	led_off(KEYPAD_LED_1)
	led_off(KEYPAD_LED_2)
	led_off(KEYPAD_LED_3)
	led_off(KEYPAD_LED_4)
	led_off(KEYPAD_LED_5)
	led_off(KEYPAD_LED_6)
	led_off(KEYPAD_LED_7)
	led_off(KEYPAD_LED_8)
	led_off(KEYPAD_LED_9)
	led_off(KEYPAD_LED_10)
	led_off(KEYPAD_LED_11)


def default_mode_state():
	led_off(NETWORK_DETECT_LED)
	led_off(RF_DETECT_LED)
	led_off(FORM1_EXIT_LED)


def default_network_state():
	led_off(NETWORK_LED_0)
	led_off(NETWORK_LED_1)
	led_off(NETWORK_LED_2)
	led_off(NETWORK_LED_3)
	led_off(NETWORK_LED_4)


# changing digits
# def change_dig(value):
# 	command = bytearray(b'\x01\x0F\x00')
# 	#insert value conversion
# 	CHKSUM = generate_CHKSUM(command)
# 	command.append(CHKSUM)
#  	ser.write(command)


# changing strings
def change_string(index, message):
	command = bytearray(b'\x02')
	command.extend(index)
	command.append(len(message))
	command.extend(message.encode("ascii"))
	command.append(generate_CHKSUM(command))
	ser.write(command)
	response = ser.read()
	print(response)


def change_form(form): 			# Allows change of global variable "currentForm" without keyword
	global currentForm 
	currentForm = form
	command = bytearray(b'\x01\x0A')
	if(form == 0):
		command.extend(FORM_0_INDEX)
	if(form == 1):
		command.extend(FORM_1_INDEX)								# add in binary, more than one 1, equals 0. otherwise 1
	elif(form == 2):
		command.extend(FORM_2_INDEX)
	elif(form == 3):
		command.extend(FORM_3_INDEX)
	elif(form == 4):
		command.extend(FORM_4_INDEX)
	elif(form == 5):
		command.extend(FORM_5_INDEX)
	elif(form == 6):
		command.extend(FORM_6_INDEX)
	elif(form == 7):
		command.extend(FORM_7_INDEX)
	command.extend(bytearray(b'\x00\x00'))
	CHKSUM = generate_CHKSUM(command)
	command.append(CHKSUM)
	ser.write(command)
	response = ser.read()
	print(response)
	print("form ==> ", form)
	return None
	
#############################
# Selection Matrix Functions
#############################


def user_mode_select():
	print("entered user mode select")
	print("waiting user selection . . .")
	mode = 0
	default_mode_state()
	led_on(NETWORK_DETECT_LED)

	LED_DICT = {
		0: NETWORK_DETECT_LED,
		1: RF_DETECT_LED,
		2: FORM1_EXIT_LED
		}

	while(1):
		if(down_button_pressed() and (mode != 2)):
			led_off(LED_DICT[mode])
			mode += 1
			led_on(LED_DICT[mode])

		elif(up_button_pressed() and (mode != 0)):
			led_off(LED_DICT[mode])
			mode -= 1
			led_on(LED_DICT[mode])
		elif(ok_button_pressed()):
			break
	led_off(LED_DICT[mode])
	print("exited user mode select")
	return mode


def network_select():
	print("network select entered")
	print("waiting user selection . . .")
	mode = 0
	default_network_state()
	led_on(NETWORK_LED_0)

	NETWORK_DICT = {
		0: NETWORK_LED_0,
		1: NETWORK_LED_1,
		2: NETWORK_LED_2,
		3: NETWORK_LED_3,
		4: NETWORK_LED_4
		}

	output = sp.check_output(['nmcli', '-f', 'SSID', '-t', 'device', 'wifi'])
	output_string = output.decode()
	output_list = output_string.split("\n")
	SSID_list = []
	for x in output_list:
		if (x != "--"):
			SSID_list.append(x)
			print("SSID appended")
	print("Length of SSID list: ", len(SSID_list))

	try:
		change_string(NETWORK_STRING_0, SSID_list[0])
	except:
		print("not enough SSIDs")
	try:
		change_string(NETWORK_STRING_1, SSID_list[1])
	except:
		print("not enough SSIDs")
	try:
		change_string(NETWORK_STRING_2, SSID_list[2])
	except:
		print("not enough SSIDs")
	try:
		change_string(NETWORK_STRING_3, SSID_list[3])
	except:
		print("not enough SSIDs")
	try:
		change_string(NETWORK_STRING_4, SSID_list[4])
	except:
		print("not enough SSIDs")

	while(1):
		if(down_button_pressed() and (mode != 4)):
			led_off(NETWORK_DICT[mode])
			mode += 1
			led_on(NETWORK_DICT[mode])

		elif(up_button_pressed() and (mode != 0)):
			led_off(NETWORK_DICT[mode])
			mode -= 1
			led_on(NETWORK_DICT[mode])
		elif(ok_button_pressed()):
			break
	led_off(NETWORK_DICT[mode])
	print("exited network select mode")
	return SSID_list[mode]


def keypad_selection():
	print("entered keypad selection")
	print("waiting user password . . .")
	count = 0
	passcode = ""
	change_string(PASSWORD_STRING, passcode)
	default_keypad_state()
	led_on(ENTER_KEY_LED)

	KEYPAD_LED_DICT = {
		0: ENTER_KEY_LED,
		1: KEYPAD_LED_0,
		2: KEYPAD_LED_1,
		3: KEYPAD_LED_2,
		4: KEYPAD_LED_3,
		5: KEYPAD_LED_4,
		6: KEYPAD_LED_5,
		7: KEYPAD_LED_6,
		8: KEYPAD_LED_7,
		9: KEYPAD_LED_8,
		10: KEYPAD_LED_9,
		11: KEYPAD_LED_10,
		12: KEYPAD_LED_11,

		13: ENTER_KEY_LED,
		14: KEYPAD_LED_0,
		15: KEYPAD_LED_1,
		16: KEYPAD_LED_2,
		17: KEYPAD_LED_3,
		18: KEYPAD_LED_4,
		19: KEYPAD_LED_5,
		20: KEYPAD_LED_6,
		21: KEYPAD_LED_7,
		22: KEYPAD_LED_8,
		23: KEYPAD_LED_9,
		24: KEYPAD_LED_10,
		25: KEYPAD_LED_11
		}

# 				Zero and Thirteen reserved for Enter
	keypad = {	1: '!@#$1', 2: 'abc2', 3: 'def3',
				4: 'ghi4',  5: 'jkl5', 6: 'mnop6',
				7: 'qrs7',  8: 'tuv8', 9: 'wxyz9',
				10:'shift', 11: '0 ',  12: 'clear',

				14: '!@#$1', 15: 'ABC2', 16: 'DEF3',
				17: 'GHI4', 18: 'JKL5', 19: 'MNOP6',
				20: 'QRS7', 21: 'TUV8', 22: 'WXYZ9',
				23: 'shift', 24: '0 ',  25: 'clear'
				}

	while(1):
		if(ok_button_pressed()):                 # lower ==> upper
			if(count == 10):
				count += 13
				print("user shift up")
			elif(count == 23):
				count -= 13
				print("user shift down")
			elif((count == 12) or (count == 25)):
				passcode = passcode[:-1]
				change_string(PASSWORD_STRING, passcode)
				print("user backspace")
			elif((count == 0) or (count == 13)):
				led_off(KEYPAD_LED_DICT[count])
				print("exiting keypad selection mode")
				return passcode
			else:
				print("user made selection")
				pad_string = keypad[count]
				passcode = passcode + pad_string[0]
				change_string(PASSWORD_STRING, passcode)
				time.sleep(1)
				change_char_index = 0

				while (down_button_pressed() != 1):
					print("cycle loop entered")
					if (ok_button_pressed()):
						print("user cycle through array")
						if (change_char_index == (len(pad_string) - 1)):
							change_char_index = 0
						else:
							change_char_index += 1
						passcode = passcode[:-1]
						passcode = passcode + pad_string[change_char_index]
						change_string(PASSWORD_STRING, passcode)
						time.sleep(0.5)

		# if (down_button_pressed() and (count not in [12,25])):
		# 	print("down button pressed")
		# 	led_off(KEYPAD_LED_DICT[count])
		# 	count += 1
		# 	led_on(KEYPAD_LED_DICT[count])
		# if (up_button_pressed() and (count not in [0,13])):
		# 	print("up button pressed")
		# 	led_off(KEYPAD_LED_DICT[count])
		# 	count -= 1
		# 	led_on(KEYPAD_LED_DICT[count])

		elif(up_button_pressed() and (count not in [0,1,2,3,13,14,15,16])):
			led_off(KEYPAD_LED_DICT[count])
			count -= 3
			led_on(KEYPAD_LED_DICT[count])

		elif(down_button_pressed() and (count not in [0,10,11,12,13,23,24,25])):
			led_off(KEYPAD_LED_DICT[count])
			count += 3
			led_on(KEYPAD_LED_DICT[count])

		elif(left_button_pressed() and (count not in [0,4,7,10,13,17,20,23])):
			led_off(KEYPAD_LED_DICT[count])
			count -= 1
			led_on(KEYPAD_LED_DICT[count])

		elif(right_button_pressed() and (count not in [3,6,9,12,16,19,22,25])):
			led_off(KEYPAD_LED_DICT[count])
			count += 1
			led_on(KEYPAD_LED_DICT[count])

##############################
# Critical Functions For User
##############################


def boot_sequence():
	"""
		Anything that the NanoPi will need to initialize
		before proper function of the device
	"""
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)							# Sets numbering scheme for pin #'s
	GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   # pin11 ok button     Initializes pin input and it's pullup/down
	GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   # pin10 up button
	GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   # pin14 down button
	GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   # pin18 left button
	GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   # pin22 right button
	GPIO.setup(2, GPIO.OUT)	 # pin9 ok button							                        Initializes pin output
	GPIO.setup(8, GPIO.OUT)	 # pin8	up button
	GPIO.setup(16, GPIO.OUT)  # pin12 down button						  set up which pins on the nano pi we will use
	GPIO.setup(9, GPIO.OUT)  # pin16 left button
	GPIO.setup(12, GPIO.OUT)	 # pin20 right button
	GPIO.output(2, GPIO.HIGH)							# Sets level of output pins; 3.3V or 0V
	GPIO.output(8, GPIO.HIGH)
	GPIO.output(16, GPIO.HIGH)
	GPIO.output(9, GPIO.HIGH)
	GPIO.output(12, GPIO.HIGH)
	print("boot sequence completed")


def network_scan(network, password):
	print("entering network scan")
	print("scanning network . . .")

	MAC_DICT = {0: MAC_ADDRESS_STRING_0,
				1: MAC_ADDRESS_STRING_1,
				2: MAC_ADDRESS_STRING_2,
				3: MAC_ADDRESS_STRING_3,
				4: MAC_ADDRESS_STRING_4,
				5: MAC_ADDRESS_STRING_5,
				6: MAC_ADDRESS_STRING_6,
				7: MAC_ADDRESS_STRING_7,
				8: MAC_ADDRESS_STRING_8
				}
	DEVICE_DICT = { 0: DEVICE_STRING_0,
					1: DEVICE_STRING_1,
					2: DEVICE_STRING_2,
					3: DEVICE_STRING_3,
					4: DEVICE_STRING_4,
					5: DEVICE_STRING_5,
					6: DEVICE_STRING_6,
					7: DEVICE_STRING_7,
					8: DEVICE_STRING_8
					}

	sp.call(['nmcli', 'dev', 'wifi', 'connect', network, 'password', password, 'ifname', 'wlan0'])

	net_f = open("connect.txt", "w")

	sp.call(['nmcli', 'dev'], stdout=net_f)
	state = sp.check_output(['awk', 'FNR == 2 {print $3}', 'connect.txt'])
	connection = sp.check_output(['awk', 'FNR == 2 {print $4}', 'connect.txt'])

	state_string = state.decode()
	connection_string = connection.decode()
	connection_string = connection_string.rstrip()

	if((state_string == "connected\n") and (connection_string == network)):
		nmap_f = open("nmap.txt", "w")
		nmap_f2 = open("nmap2.txt", "w")
		sp.call(['ip', 'a'], stdout=nmap_f)
		sp.call(['grep', '-E', 'inet.*wlan0', 'nmap.txt'], stdout=nmap_f2)
		ip_address = sp.check_output(['awk', '{print $2}', 'nmap2.txt'])
		ip_string = ip_address.decode()
		print(ip_string)

		ip_string = ip_string.rstrip()
		ip_list = ip_string.split(".")
		print(ip_list)

		boundary = ip_list[0] + '.' + ip_list[1] + '.' + ip_list[2] + '.' + '0/24'
		print(boundary)

		mac_f = open("mac.txt", "w")
		sp.call(['sudo', 'nmap', '-sn', boundary], stdout=mac_f)
		MAC = sp.check_output(['awk', '/MAC Address/', 'mac.txt'])

		MAC_string = MAC.decode("ascii")
		print(MAC_string)
		MAC_list = MAC_string.split("\n")
		print(MAC_list)

		Devices = []
		MAC_addresses = []
		for x in MAC_list:
			MAC_addresses.append(x[13:30])
			Devices.append(x[30:])

		for y in range(len(MAC_addresses)):
			if (y == 0):
				change_form(4)
			elif (y == 2):
				change_form(5)
			elif (y == 5):
				change_form(6)
			change_string(MAC_DICT[y], MAC_addresses[y])
			change_string(DEVICE_DICT[y], Devices[y])
			time.sleep(3)

		print("exiting network scan, status: SUCCESS")
		return 0
	else:
		#retry password input
		print("exiting network scan, status: FAILURE")
		return 1

def rf_detect():
	"""
		This is where the GNU Radio code goes
		Should be copy paste, but will see about
		importing as class later
	"""

#################################### MAIN FUNCTION ##################################


print("This is the main function")
boot_sequence()

# Form 1
	# mode selection
# Form 2
	# select network
	# 5 labels, 5LEDs
# Form 3
	# enter network key
	# keypad, shift, clear
	# label as you enter keys
	# Okay LED to submit
# Form 4 - 6
	# mac address, possible device
	# 3 devices per form; 6 labels and 1 LED's per form
# Form 7
	# rf detection
	# 4 LEDs, 1 LED digits, 1 label for . . .

while(1):
	change_form(1)
	modeSelection = user_mode_select()
	if(modeSelection == 0):
		print("user mode 'Network Scan' selected")
		while(1):
			change_form(2)
			userNetwork = network_select()
			change_form(3)
			password = keypad_selection()
			net_exit_status = network_scan(userNetwork, password)
			if(net_exit_status == 1):
				print("Connection Failure, boot to network select")
				continue
			break
		print("End of network select, restarting from mode select")


	elif(modeSelection == 1):
		change_form(7)
		while(1):
			if(ok_button_pressed()):
				break


	elif(modeSelection == 2):
		change_form(0)
		time.sleep(3)
		sp.call(['reboot'])

	# exit sequence
