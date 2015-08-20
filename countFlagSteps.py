import time
from wiringx86 import GPIOEdison as GPIO
gpio = GPIO(debug=False)
pin1 = 3
pin2 = 4
pin3 = 5
pin4 = 6
index = 0

print 'Setting up pin %d' % pin1
gpio.pinMode(pin1, gpio.OUTPUT)
print 'Setting up pin %d' % pin2
gpio.pinMode(pin2, gpio.OUTPUT)
print 'Setting up pin %d' % pin3
gpio.pinMode(pin3, gpio.OUTPUT)
print 'Setting up pin %d' % pin4
gpio.pinMode(pin4, gpio.OUTPUT)

print 'Go up now...'
try:
  while(True):
    gpio.digitalWrite(pin4, gpio.LOW)     
    gpio.digitalWrite(pin2, gpio.HIGH)    
    time.sleep(0.01)                      
                                              
    gpio.digitalWrite(pin1, gpio.LOW)     
    gpio.digitalWrite(pin3, gpio.HIGH)    
    time.sleep(0.01)                      
                                              
    gpio.digitalWrite(pin2, gpio.LOW)     
    gpio.digitalWrite(pin4, gpio.HIGH)    
    time.sleep(0.01)                      
                                              
    gpio.digitalWrite(pin3, gpio.LOW)     
    gpio.digitalWrite(pin1, gpio.HIGH)    
    time.sleep(0.01)                      
                                              
    index=index+1
    
# When you get tired of seeing the led blinking kill the loop with Ctrl-C.
except KeyboardInterrupt:                                                 
  print '\nCleaning up...'                                              
  print 'total step %d' % index                                           
  gpio.digitalWrite(pin1, gpio.LOW)                                     
  gpio.digitalWrite(pin2, gpio.LOW)                                     
  gpio.digitalWrite(pin3, gpio.LOW)                                     
  gpio.digitalWrite(pin4, gpio.LOW)                                     
                                                                          
  # Do a general cleanup. Calling this function is not mandatory.       
  gpio.cleanup()     
