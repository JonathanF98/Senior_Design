# pip3 install wifi

from wifi import Cell, Scheme

cells = Cell.all('wlan0')
for cell in cells:
	print(cell.ssid)
