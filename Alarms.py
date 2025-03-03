#initialization
import pygame
pygame.init()
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as paho
import sys
from paho import mqtt
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
#Visual Alarm GPIO ports
GPIO.setup(16,GPIO.OUT, initial = False)                  
GPIO.setup(18,GPIO.OUT, initial = False)
#sensor designation GPIO ports
GPIO.setup(11,GPIO.OUT, initial = False)
GPIO.setup(13,GPIO.OUT, initial = False)
GPIO.setup(15,GPIO.OUT, initial = False)
GPIO.setup(22,GPIO.OUT, initial = False)
#Acknowledgement switch GPIO ports
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

Moderate_Alarm = pygame.mixer.Sound('/home/freshair/Downloads/ModerateAlarm.wav')
Dangerous_Alarm = pygame.mixer.Sound('/home/freshair/Downloads/DangerousAlarm.wav')

connection_status = False

# Upon connection, print connection status and set global variable
def on_connect(client, userdata, flags, rc, properties=None):
    # THE FOLLOWING EXCERPT IS ADAPTED FROM AN AI GENERATED EXAMPLE:
    global connection_status
    if rc == 0:
        print("\n Successfully connected to the broker")
        connection_status = True
    else:
        print("Failed to connect, code %d" %rc)
        connection_status = False
    # END OF AI GENERATED CODE
    
def on_publish(client, userdata, mid, properties=None):
    print("\n Publish succesful")

# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)

# Set up for connection function
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set("Raspberry_Pi", "Raspberry_Pi1")
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect("447eeeb9cd214112bba5874c3722ece9.s1.eu.hivemq.cloud", 8883)
# Set up for publish function
client.on_publish = on_publish

client.loop_start()

class VariableWatcher:
    def __init__(self, value=None, identifier=None):
        self._value = value
        self.identifier = identifier  # To identify which watcher triggered the change
    
    # Getter for the variable
    @property
    def value(self):
        return self._value
    
    # Setter for the variable (called when the variable is modified)
    @value.setter
    def value(self, new_value):
        if self._value != new_value:  # Check if the value has changed
            self._value = new_value
            self.on_change(new_value)
    
    def on_change(self, new_value):
        # This method is triggered when the value is changed
        
        # Call the appropriate subroutine based on the identifier
        if self.identifier == "input1":
            visual_alarm(new_value)
        elif self.identifier == "input2":
            sensor_designation(new_value)
        else:
            end_program(new_value)


# Subroutine for when the first variable changes
def visual_alarm(changed_value):
    IAQ = int(changed_value)
    # Custom logic for input1
    if IAQ == 1:
        print("Environment is safe")
        GPIO.output(18, False)
        GPIO.output(16, False)
    elif IAQ == 2:
        print("Environment is Unhealthy")
        GPIO.output(18, False)
        GPIO.output(16, True)
        Moderate_Alarm.play()
        payload = "OFF"
        # Publish input to server
        client.publish("led/control", payload, qos=1)
	
    elif IAQ == 3: 
        print("Environment is Dangerous")
        GPIO.output(16, False)
        GPIO.output(18, True)
        Dangerous_Alarm.play()
        payload = "ON"
        # Publish input to server
        client.publish("led/control", payload, qos=1)
    else:
        print("Invalid input for the PM density entered. Please enter an integer from 1 - 3")
        GPIO.output(16, False)
        GPIO.output(18, False)
 

# Subroutine for when the second variable changes
def sensor_designation(changed_value):
    sensor = int(changed_value)
    if sensor == 1:
        print ("PM data has been sent from sensor 1")
        GPIO.output(11,True)
        GPIO.output(13,False)
        GPIO.output(15,False)
        GPIO.output(22,False)
    elif sensor == 2:
        print ("PM data has been sent from sensor 2")
        GPIO.output(11,False)
        GPIO.output(13,True)
        GPIO.output(15,False)
        GPIO.output(22,False)
    elif sensor == 3:
        print ("PM data has been sent from sensor 3")
        GPIO.output(11,False)
        GPIO.output(13,False)
        GPIO.output(15,True)
        GPIO.output(22,False)
    elif sensor == 4:
        print ("PM data has been sent from sensor 4")
        GPIO.output(11,False)
        GPIO.output(13,False)
        GPIO.output(15,False)
        GPIO.output(22,True)
    else:
        print("invalind input entered for the sensor. please input an integer from 1-4")
        GPIO.output(11,False)
        GPIO.output(13,False)
        GPIO.output(15,False)
        GPIO.output(22,False)
      
def end_program(changed_value):
    if changed_value == "exit":
        GPIO.output(16, False)
        GPIO.output(18, False)
        GPIO.output(11,False)
        GPIO.output(13,False)
        GPIO.output(15,False)
        GPIO.output(22,False)
        exit()
    else:
        print("Invalid input. Please enter exactly two values separated by a space or the 'exit' command.")
# Main program loop
def main():
    # Create two instances of the VariableWatcher class, one for each input
    watcher1 = VariableWatcher(identifier="input1")  # First input watcher
    watcher2 = VariableWatcher(identifier="input2")  # Second input watcher
    watcher3 = VariableWatcher(identifier="input3")
    while True:
        # Prompt the user for both inputs at once
        user_input = input("Please enter the PM data followed by a space and the sensor it was sent from. \n 1 = healthy \n 2 = moderate \n 3 = dangerous (e.g., '1 1')")
        
        # Split the input string into two parts (values)
        inputs = user_input.split()
         # check if input is a chacter or and integer... if two characters are entered the code breaks
        if len(inputs[0]) == 1:# Assign values to the watchers
            watcher1.value = inputs[0]
            watcher2.value = inputs[1]
        elif len(inputs) == 1: #new code
            watcher3.value = inputs[0]
        else:
            print("Invalid input. Please enter exactly two values separated by a space.")
 #another elsif: if input is q then exit program/ return

def button_callback(channel):
    GPIO.output(16,False)
    GPIO.output(18, False)

GPIO.add_event_detect(37,GPIO.RISING,callback=button_callback) # Setup event on pin 10 rising edge

if __name__ == "__main__":
    main()


#loop for a certain interval and exit loop and wait for user input


