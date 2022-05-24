#!/usr/bin/env python3 
import cgitb ; cgitb.enable() 
import spidev 
import time
import busio
import digitalio
import board
from adafruit_bus_device.spi_device import SPIDevice
import threading

from pushbullet import Pushbullet

 
# Initialize SPI bus
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialize control pins for adc
cs0 = digitalio.DigitalInOut(board.CE0)  # chip select
adc = SPIDevice(spi, cs0, baudrate= 1000000)

exit_event = threading.Event()
 
# read SPI data 8 possible adc's (0 thru 7) 
def readadc(adcnum): 
	if ((adcnum > 7) or (adcnum < 0)): 
		return -1 
	with adc:
		r = bytearray(3)
		spi.write_readinto([1,(8+adcnum)<<4,0], r)
		time.sleep(0.000005)
		adcout = ((r[1]&3) << 8) + r[2] 
		return adcout 

def push():

	API_KEY = "o.QCdVDvNwBIEaJxVsaUmDe50lm5KaQ8f9"
	filename = 'resolution.txt'
	filename2 = 'resolution2.txt'

	if (tmp0 > 200 ):
		with open(filename, mode='r') as f:
			text = f.read()
		pb = Pushbullet(API_KEY)
		push = pb.push_note("This is the title", text)

	if (tmp1 > 200 ):
		with open(filename2, mode='r') as f2:
			text2 = f2.read()
		pb = Pushbullet(API_KEY)
		push = pb.push_note("This is the title", text2)
		



try:
	while True:
		tmp0 = readadc(0) # read channel 0 
		tmp1 = readadc(1) # read channel 1
		print ("input0:",tmp0)
		print ("input1:",tmp1)
		push()
		time.sleep(0.2)

except KeyboardInterrupt:
    #cleanup
    GPIO.cleanup()
    print("clean closed")
