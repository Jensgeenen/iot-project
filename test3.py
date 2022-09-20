from bluedot import BlueDot 
from gpiozero import LED

bd = BlueDot()
led = LED(17)
switch = 0

while True:
    if ( bd.wait_for_press() == True)&(switch == 0):
        switch = 1
        led.on()
    elif(switch == 1)&(bd.wait_for_release() == True):
        led.off()
        switch = 0
