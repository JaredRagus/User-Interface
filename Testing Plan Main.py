#initialization
#import RPi.GPIO as GPIO   
#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)

#GPIO.setup(4,GPIO.out)                  #Visual Alarm GPIO ports
#GPIO.setup(5,GPIO.out)
#sensor designation GPIO ports

#Acknowledgement switch GPIO ports

def User_Input():
    IAQ_String = input("What is the current PM density?")
    Sensor_String = input("Which sensor is detecting PM density?")
    IAQ = int(IAQ_String)
    Sensor = int(Sensor_String)
    return (IAQ,Sensor)
    
User_Input()


#loop for a certain interval and exit loop and wait for user input

#def on_value_change(old_value, new_value):
#    print("Value changed from", old_value, "to", new_value)

#def watch_variable(variable, callback):
#   def wrapper(new_value):
#       nonlocal variable
#        old_value = IAQ
#        variable = new_value
#        callback(old_value, new_value)
#    return wrapper

class ValueWatcher:
    def __init__(self, value):
        self._value = IAQ

    @property
    def IAQ(self):
        return self._value

    @IAQ.setter
    def IAQ(self, new_value):
        if new_value != self._value:
            print("Value changed from", self._value, "to", new_value)
            self._value = new_value

def Visual_Alarm():
    if IAQ == 1:
        print("Environment is safe")
        IAQ_String()
    elif IAQ == 2:
        print("Environment is Unhealthy")
        GPIO.output(5, false)
        GPIO.output(4, true)
	
    else: 
        print("Environment is Dangerous")
        GPIO.output(4, false)
        GPIO.output(5, true)
        

Visual_Alarm()