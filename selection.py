mode = 0
led_on(NETWORK_DETECT_LED)

while(!ok_button_pressed()):
	if(right_button_pressed() and mode != 2):
		mode += 1
		
	if(left_button_pressed() and mode != 0):
		mode -= 1
return mode
