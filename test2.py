#!/usr/bin/env python3 
import cgitb
from tempfile import tempdir ; cgitb.enable() 
import spidev 
import time
import busio
import digitalio
import board
from adafruit_bus_device.spi_device import SPIDevice
import requests 
from pushbullet import Pushbullet
import threading

url = "http://tibedk1.hub.ubeac.io/projectiot"  #ubeac link om te uploaden
uid = "raspivantibe"                            #ubeac Unique IDs

exit_event = threading.Event()

# Start SPI op
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Start analogDigitalConvertor op
cs0 = digitalio.DigitalInOut(board.CE0)
adc = SPIDevice(spi, cs0, baudrate= 1000000)
 
def lees(sensor): 
    if sensor == 'temp':
        with adc:
            r = bytearray(3)
            spi.write_readinto([1,(8)<<4,0], r)
            time.sleep(0.000005)
            adcout = ((r[1]&3) << 8) + r[2] 
            return adcout 
    elif sensor == 'weight':
        with adc:
            r = bytearray(3)
            spi.write_readinto([1,(9)<<4,0], r)
            time.sleep(0.000005)
            adcout = ((r[1]&3) << 8) + r[2]
            return adcout 
    else: 
        return -1

# def stuurData(temp, gew):
#     data = {                                            #Pak alle data in om te versturen
# 		"id": uid,
# 		"sensors":[{
# 			'id': 'adc kanaal0',
# 			'data': temp
# 			}, {
#             'id': 'adc kanaal1',
# 			'data': gew
#             }]}
#     requests.post(url, verify=False,  json=data)        #Verstuur deze data door een http request

def push():
    API_KEY = "o.QCdVDvNwBIEaJxVsaUmDe50lm5KaQ8f9"
    filename1 = 'resolution.txt'
    # waarde = 'resolution2.txt'

    if (temperatuur > 200 ):
        with open(filename1, mode='r') as f:
            text = f.read()
        pb = Pushbullet(API_KEY)
        push = pb.push_note("This is the title", text)

    # if (gewicht > 200 ):
	# 	with open(waarde, mode='r') as b:
	# 		text2 = b.read()
	# 	pb = Pushbullet(API_KEY)
	# 	push = pb.push_note("This is the title", text2)

try:
    while True:
        temperatuur = lees('temp')
        gewicht = lees('weight')
        push()
        print ("input0:",temperatuur)
		print ("input1:",gewicht)
        time.sleep(0.2)

except KeyboardInterrupt:
    #cleanup
    GPIO.cleanup()
    print("clean closed")
  
