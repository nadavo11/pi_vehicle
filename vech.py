from periphery import GPIO
import keyboard
from periphery import I2C
from periphery import PWM
import time

#-------parser-------------

def on_press(key):
    if key = 




#------ in1,2 Settings-----

in1 = GPIO("/dev/gpiochip2",9,"out") #pin 16
in2 = GPIO("/dev/gpiochip4",10,"out") #pin 18
##button = GPIO("/dev/gpiochip4",13,"out")

#spin direction
in1.write( True )
in2.write( False)

#------PWM Settings-------

#init PWM pin 33
pwm =PWM(1,0)

#set PWM frequency                                                                                                                    
pwm.frequency =1e3

#start PWM from 0
pwm.duty_cycle = 0
duty = 0  

#start PWM from 0
pwm.duty_cycle = 0
duty = 0
pwm.enable()


#------physics setup------
v = 0
a = 0
direction = True 

i=0
#loop
try:
    while i<30:
        
        #change led intensity, print status
        pwm.duty_cycle = duty
        print(duty)
        
        #increase each 1/10 sec  
        duty = (v)%1
        time.sleep(0.1)
        i+=1

finally:
    in1.write(False)
    pwm.close()
   # button.close()
       

