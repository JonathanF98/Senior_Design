# Possible shebang would go here

############################# IMPORTS & GLOBALS ################################
import subprocess as sp
import serial  # imports pySerial for comm with LCD
import RPi.GPIO as GPIO  # imports RPi.GPIO_NP to talk with GPIO pins
import time

ser = serial.Serial('/dev/ttyS1', 115200)
currentForm = 0  # global variable that should follow the current LCD screen form
# Make sure to keep track of this value as it will change
# between functions
# FORM 0 INDEX
FORM_0_INDEX = bytearray(b'\x00')
# FORM 1 INDEXES
FORM_1_INDEX = bytearray(b'\x01')  # replace "index with hex code such as 00,01,1B, ETC."
NETWORK_DETECT_LED = bytearray(b'\x00')
RF_DETECT_LED = bytearray(b'\x01')
FORM1_EXIT_LED = bytearray(b'\x02')
# FORM 2 INDEXES
FORM_2_INDEX = bytearray(b'\x02')
NETWORK_STRING_0 = bytearray(b'\x00')
NETWORK_STRING_1 = bytearray(b'\x01')
NETWORK_STRING_2 = bytearray(b'\x02')
NETWORK_STRING_3 = bytearray(b'\x03')
NETWORK_STRING_4 = bytearray(b'\x04')
NETWORK_LED_0 = bytearray(b'\x03')
NETWORK_LED_1 = bytearray(b'\x04')
NETWORK_LED_2 = bytearray(b'\x05')
NETWORK_LED_3 = bytearray(b'\x06')
NETWORK_LED_4 = bytearray(b'\x07')
# FORM 3 INDEXES
FORM_3_INDEX = bytearray(b'\x03')
ENTER_KEY_LED = bytearray(b'\x14')
KEYPAD_LED_0 = bytearray(b'\x08')
KEYPAD_LED_1 = bytearray(b'\x09')
KEYPAD_LED_2 = bytearray(b'\x0A')
KEYPAD_LED_3 = bytearray(b'\x0B')
KEYPAD_LED_4 = bytearray(b'\x0C')
KEYPAD_LED_5 = bytearray(b'\x0D')
KEYPAD_LED_6 = bytearray(b'\x0E')
KEYPAD_LED_7 = bytearray(b'\x0F')
KEYPAD_LED_8 = bytearray(b'\x10')
KEYPAD_LED_9 = bytearray(b'\x11')
KEYPAD_LED_10 = bytearray(b'\x12')
KEYPAD_LED_11 = bytearray(b'\x13')
PASSWORD_STRING = bytearray(b'\x05')
# FORM 4 INDEXES
FORM_4_INDEX = bytearray(b'\x04')
MAC_ADDRESS_STRING_0 = bytearray(b'\x06')
DEVICE_STRING_0 = bytearray(b'\x07')
MAC_ADDRESS_STRING_1 = bytearray(b'\x08')
DEVICE_STRING_1 = bytearray(b'\x09')
MAC_ADDRESS_STRING_2 = bytearray(b'\x0A')
DEVICE_STRING_2 = bytearray(b'\x0B')
NEXT_FORM_LED_0 = bytearray(b'\x15')

# FORM 5 INDEXES
FORM_5_INDEX = bytearray(b'\x05')
MAC_ADDRESS_STRING_3 = bytearray(b'\x0C')
DEVICE_STRING_3 = bytearray(b'\x0D')
MAC_ADDRESS_STRING_4 = bytearray(b'\x0C')
DEVICE_STRING_4 = bytearray(b'\x0D')
MAC_ADDRESS_STRING_5 = bytearray(b'\x10')
DEVICE_STRING_5 = bytearray(b'\x11')
NEXT_FORM_LED_1 = bytearray(b'\x16')

# FORM 6 INDEXES
FORM_6_INDEX = bytearray(b'\x06')
MAC_ADDRESS_STRING_6 = bytearray(b'\x12')
DEVICE_STRING_6 = bytearray(b'\x13')
MAC_ADDRESS_STRING_7 = bytearray(b'\x14')
DEVICE_STRING_7 = bytearray(b'\x15')
MAC_ADDRESS_STRING_8 = bytearray(b'\x16')
DEVICE_STRING_8 = bytearray(b'\x17')
NEXT_FORM_LED_2 = bytearray(b'\x17')

# FORM 7 INDEXES
FORM_7_INDEX = bytearray(b'\x07')
PROXIMITY_LED_0 = bytearray(b'\x18')
PROXIMITY_LED_1 = bytearray(b'\x19')
PROXIMITY_LED_2 = bytearray(b'\x1A')
PROXIMITY_LED_3 = bytearray(b'\x1B')
LED_DIGITS_0 = bytearray(b'\x00')
ELIPSES_STRING = bytearray(b'\x18')


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


# def left_button_pressed():
# 	if GPIO.input(18):
# 		time.sleep(0.3)
# 		return 1
# 	else:
# 		return 0


# def right_button_pressed():
# 	if GPIO.input(4):
# 		time.sleep(0.3)
# 		return 1
# 	else:
# 		return 0


def generate_CHKSUM(command):
    for x in range(len(command)):
        if (x == 0):
            result = command[x] ^ command[x + 1]
        elif (x >= 2):
            result = result ^ command[x]
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
    print("string changed: index:", index)


def change_form(form):  # Allows change of global variable "currentForm" without keyword
    global currentForm
    currentForm = form
    command = bytearray(b'\x01\x0A')
    if (form == 0):
        command.extend(FORM_0_INDEX)
    if (form == 1):
        command.extend(FORM_1_INDEX)  # add in binary, more than one 1, equals 0. otherwise 1
    elif (form == 2):
        command.extend(FORM_2_INDEX)
    elif (form == 3):
        command.extend(FORM_3_INDEX)
    elif (form == 4):
        command.extend(FORM_4_INDEX)
    elif (form == 5):
        command.extend(FORM_5_INDEX)
    elif (form == 6):
        command.extend(FORM_6_INDEX)
    elif (form == 7):
        command.extend(FORM_7_INDEX)
    command.extend(bytearray(b'\x00\x00'))
    CHKSUM = generate_CHKSUM(command)
    command.append(CHKSUM)
    ser.write(command)
    response = ser.read()
    print(response)
    print("form ==> ", form)
    return None


def boot_sequence():
    """
		Anything that the NanoPi will need to initialize
		before proper function of the device
	"""
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)  # Sets numbering scheme for pin #'s
    GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # pin11 ok button     Initializes pin input and it's pullup/down
    GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # pin10 up button
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # pin14 down button
    # GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   # pin18 left button
    # GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   # pin22 right button
    GPIO.setup(2, GPIO.OUT)  # pin9 ok button							                        Initializes pin output
    GPIO.setup(8, GPIO.OUT)  # pin8	up button
    GPIO.setup(16, GPIO.OUT)  # pin12 down button						  set up which pins on the nano pi we will use
    # GPIO.setup(16, GPIO.OUT)  # pin16 left button
    # GPIO.setup(2, GPIO.OUT)	 # pin20 right button
    GPIO.output(2, GPIO.HIGH)  # Sets level of output pins; 3.3V or 0V
    GPIO.output(8, GPIO.HIGH)
    GPIO.output(16, GPIO.HIGH)
    # GPIO.output(16, GPIO.HIGH)
    # GPIO.output(2, GPIO.HIGH)
    print("boot sequence completed")


boot_sequence()
change_form(4)

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
DEVICE_DICT = {0: DEVICE_STRING_0,
               1: DEVICE_STRING_1,
               2: DEVICE_STRING_2,
               3: DEVICE_STRING_3,
               4: DEVICE_STRING_4,
               5: DEVICE_STRING_5,
               6: DEVICE_STRING_6,
               7: DEVICE_STRING_7,
               8: DEVICE_STRING_8
               }

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

print(MAC_addresses)
print(Devices)

for y in range(len(MAC_addresses)):
    change_string(MAC_DICT[y], MAC_addresses[y])
    change_string(DEVICE_DICT[y], Devices[y])
    time.sleep(3)
    if(y == 2):
        change_form(5)
    if(y == 5):
        change_form(6)

print("exiting network scan, status: SUCCESS")
