#Possible shebang would go here

############################# IMPORTS & GLOBALS ################################
import serial			          #imports pySerial for comm with LCD
import RPi.GPIO as GPIO		#imports RPi.GPIO_NP to talk with GPIO pins
import time
ser = serial.Serial('/dev/ttyS1', 115200)
currentForm = 0					    #global variable that should follow the current LCD screen form
										            #Make sure to keep track of this value as it will change
										            #between fucntions

#FORM 1 INDEXES
FORM_1_INDEX					= bytearray(b'x\01')			#replace "index with hex code such as 00,01,1B, ETC."
NETWORK_DETECT_LED	 	= bytearray(b'x\00')
RF_DETECT_LED 			  = bytearray(b'x\01')
FORM1_EXIT_LED 		  	= bytearray(b'x\02')
#FORM 2 INDEXES
FORM_2_INDEX					= bytearray(b'x\02')
NETWORK_STRING_0			= bytearray(b'x\00')
NETOWRK_STRING_1	  	= bytearray(b'x\01')
NETWORK_STRING_2		  = bytearray(b'x\02')
NETWORK_STRING_3			= bytearray(b'x\03')
NETWORK_STRING_4			= bytearray(b'x\04')
NETWORK_LED_0		    	= bytearray(b'x\03')
NETWORK_LED_1	    	 	= bytearray(b'x\04')
NETWORK_LED_2	  	  	= bytearray(b'x\05')
NETWORK_LED_3			    = bytearray(b'x\06')
NETWORK_LED_4		    	= bytearray(b'x\07')
#FORM 3 INDEXES
FORM_3_INDEX					= bytearray(b'x\03')
ENTER_KEY_LED	    		= bytearray(b'x\14')
KEYPAD_LED_0	    		= bytearray(b'x\08')
KEYPAD_LED_1	  	  	= bytearray(b'x\09')
KEYPAD_LED_2		    	= bytearray(b'x\0A')
KEYPAD_LED_3		    	= bytearray(b'x\0B')
KEYPAD_LED_4		    	= bytearray(b'x\0C')
KEYPAD_LED_5	    		= bytearray(b'x\0D')
KEYPAD_LED_6	  	  	= bytearray(b'x\0E')
KEYPAD_LED_7		    	= bytearray(b'x\0F')
KEYPAD_LED_8		    	= bytearray(b'x\10')
KEYPAD_LED_9		    	= bytearray(b'x\11')
KEYPAD_LED_10		  	  = bytearray(b'x\12')
KEYPAD_LED_11			    = bytearray(b'x\13')
PASSWORD_STRING		  	= bytearray(b'x\05')
#FORM 4 INDEXES
FORM_4_INDEX					= bytearray(b'x\04')
MAC_ADDRESS_STRING_0	= bytearray(b'x\06')
DEVICE_STRING_0				= bytearray(b'x\07')
MAC_ADDRESS_STRING_1	= bytearray(b'x\08')
DEVICE_STRING_1				= bytearray(b'x\09')
MAC_ADDRESS_STRING_2	= bytearray(b'x\0A')
DEVICE_STRING_2				= bytearray(b'x\0B')
NEXT_FORM_LED_0 			= bytearray(b'x\15')

#FORM 5 INDEXES
FORM_5_INDEX					= bytearray(b'x\05')
MAC_ADDRESS_STRING_3	= bytearray(b'x\0C')
DEVICE_STRING_3				= bytearray(b'x\0D')
MAC_ADDRESS_STRING_4	= bytearray(b'x\0E')
DEVICE_STRING_4				= bytearray(b'x\0F')
MAC_ADDRESS_STRING_5	= bytearray(b'x\10')
DEVICE_STRING_5				= bytearray(b'x\11')
NEXT_FORM_LED_1 			= bytearray(b'x\16')

#FORM 6 INDEXES
FORM_6_INDEX					= bytearray(b'x\06')
MAC_ADDRESS_STRING_6	= bytearray(b'x\12')
DEVICE_STRING_6				= bytearray(b'x\13')
MAC_ADDRESS_STRING_7	= bytearray(b'x\14')
DEVICE_STRING_7				= bytearray(b'x\15')
MAC_ADDRESS_STRING_8	= bytearray(b'x\16')
DEVICE_STRING_8				= bytearray(b'x\17')
NEXT_FORM_LED_2 			= bytearray(b'x\17')

#FORM 7 INDEXES
FORM_7_INDEX					= bytearray(b'x\07')
PROXIMITY_LED_0				= bytearray(b'x\18')
PROXIMITY_LED_1				= bytearray(b'x\19')
PROXIMITY_LED_2				= bytearray(b'x\1A')
PROXIMITY_LED_3				= bytearray(b'x\1B')
LED_DIGITS_0 					= bytearray(b'x\00')
ELIPSES_STRING				= bytearray(b'x\18')

############################# FUNCTION - DEFINITIONS ################################

#############################
# Helper Functions For Modes
#############################

#buttons
#ok button
def ok_button_pressed():
	if GPIO.input(11):
		time.sleep(200)
		return 1
	else:
		return 0

#up button
def up_button_pressed():
	if GPIO.input(10):
		time.sleep(200)
		return 1
	else:
		return 0

#down button
def down_button_pressed():
	if GPIO.input(14):
		time.sleep(200)
		return 1
	else:
		return 0

#left button 
def left_button_pressed():
	if GPIO.input(18):
		time.sleep(200)
		return 1
	else:
		return 0

#right button
def right_button_pressed():
	if GPIO.input(4):
		time.sleep(200)
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
	command.append(LED)
	command.extend(b'\x00\x01')
	CHKSUM = generate_CHKSUM(command)
	command.append(CHKSUM)
	ser.write(command)

def led_off(LED):
	command = bytearray(b'\x01\x13')
	command.append(LED)
	command.extend(b'\x00\x00')
	CHKSUM = generate_CHKSUM(command)
	command.append(CHKSUM)
	ser.write(command)
 
#changing digits
# def change_dig(value):
# 	command = bytearray(b'\x01\x0F\x00')
# 	#insert value conversion
# 	CHKSUM = generate_CHKSUM(command)
# 	command.append(CHKSUM)
#  	ser.write(command)


#changing strings
def change_string(index, message):
	command = bytearray(b'\x02')
	command.extend(index)
	command.append(len(message))
	command.extend(message.encode("ascii"))
	command.append(generate_CHKSUM(command))
	ser.write(command)
 

def change_form(form): 			#Allows change of global variable "currentForm" without keyword
	global currentForm 
	currentForm = form
	command = bytearray(b'\x01\x0A')
	if(form == 1):
		command.append(FORM_1_INDEX)								# add in binary, more than one 1, equals 0. otherwise 1
	elif(form == 2):
		command.append(FORM_2_INDEX)
	elif(form == 3):
		command.append(FORM_3_INDEX)
	elif(form == 4):
		command.append(FORM_4_INDEX)
	elif(form == 5):
		command.append(FORM_5_INDEX)
	elif(form == 6):
		command.append(FORM_6_INDEX)
	elif(form == 7):
		command.append(FORM_7_INDEX)
	command.extend(bytearray(b'\x00\x00'))
	CHKSUM = generate_CHKSUM(command)
	command.append(CHKSUM)
	ser.write(command)
	return None

def keypad_selection():
  count = 0
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
      12: KEYPAD_LED_11

      13: KEYPAD_LED_0,
      14: KEYPAD_LED_1,
      15: KEYPAD_LED_2,
      16: KEYPAD_LED_3,
      17: KEYPAD_LED_4,
      18: KEYPAD_LED_5,
      19: KEYPAD_LED_6,
      20: KEYPAD_LED_7,
      21: KEYPAD_LED_8,
      22: KEYPAD_LED_9,
      23: KEYPAD_LED_10,
      24: KEYPAD_LED_11
  }

  keypad = {1: '!@#$1', 2: 'abc2', 3: 'def3',
            4: 'ghi4',  5: 'jkl5', 6: 'mnop6',
            7: 'qrs7',  8: 'tuv8', 9: 'wxyz9',
            10:'shift', 11: '0 ' , 12: 'clear'
            
            13: '!@#$', 14: 'ABC2', 15: 'DEF3',
            16: 'GHI4', 17: 'JKL5', 18: 'MNOP6',
            19: 'QRS7', 20: 'TUV8', 21: 'WXYZ9',
            22: 'shift', 23: '0 ',   24: 'clear'}

  passcode = ""
  secrets = ""
  shift_val = 0

  while(1):

    if(ok_button_pressed && (count == 10)):                  # lower ==> upper
      count += 12

    elif(ok_button_pressed && (count == 22)):                # upper ==> lower
      count -= 12

    elif(ok_button_pressed && (count == 12)):                # clear
      passcode = passcode[:-1]
      change_string(PASSWORD_STRING, passcode)

    elif(ok_button_pressed && (count == 24)):                # clear
      passcode = passcode[:-1]
      change_string(PASSWORD_STRING, passcode)

    elif(ok_button_pressed && (count != 0)):
      pad_string = keypad[count]
      passcode = passcode + pad_string[0]
      change_string(PASSWORD_STRING, passcode)

      change_char_index = 0
      
      t_end = time.time() + 6
      while(time.time() < t_end):
        if(ok_button_pressed):
          if(change_char_index == (len(pad_string)-1)):
            change_char_index = 0
          else:
            change_char_index += 1
          passcode = passcode[:-1]
          passcode = passcode + pad_string[change_char_index]
          change_string(PASSWORD_STRING, passcode)
    elif(ok_button_pressed && count == 0)
      return passcode

    elif(up_button_pressed && (count not in [0,1,2,3,13,14,15]):
      led_off(KEYPAD_LED_DICT[count])
      count -= 3
      led_on(KEYPAD_LED_DICT[count])

    elif(down_button_pressed && (count not in [0,10,11,12,22,23,24])):
      led_off(KEYPAD_LED_DICT[count])
      count += 3
      led_on(KEYPAD_LED_DICT[count])

    elif(left_button_pressed && (count not in [0,1,4,7,10,13,16,19,22])):
      led_off(KEYPAD_LED_DICT[count])
      count -= 1
      led_on(KEYPAD_LED_DICT[count])

    elif(right_button_pressed && (count not in [3,6,9,12,15,18,21,24])):
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
	GPIO.setmode(GPIO.BOARD)							#Sets numbering scheme for pin #'s
	GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   #pin11 ok button       	#Initializes pin input and it's pullup/down
	GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   #pin10 up button
	GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   #pin14 down button
	GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   #pin18 left button
	GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)   #pin22 right button
	GPIO.setup(9, GPIO.OUT)	 #pin9 ok button							                        #Initializes pin output
	GPIO.setup(8, GPIO.OUT)	 #pin8	up button						                            
	GPIO.setup(12, GPIO.OUT) #pin12 down button						                        #set up which pins on the nano pi we will use
	GPIO.setup(16, GPIO.OUT) #pin16 left button
	GPIO.setup(2, GPIO.OUT) #pin20 right button
	GPIO.output(9, GPIO.HIGH)							#Sets level of output pins; 3.3V or 0V
	GPIO.output(8, GPIO.HIGH)
	GPIO.output(12, GPIO.HIGH)
	GPIO.output(16, GPIO.HIGH)
	GPIO.output(2, GPIO.HIGH)
  
#################################### MAIN FUNCTION ##################################
print("This is the main function")
boot_sequence()
change_form(2)
password = keypad_selection()
print(password)