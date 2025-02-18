#initialization
import RPi.GPIO as GPIO   
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
#Visual Alarm GPIO ports
GPIO.setup(16,GPIO.OUT)                  
GPIO.setup(18,GPIO.OUT)
#sensor designation GPIO ports
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
#Acknowledgement switch GPIO ports
GPIO.setup(37, GPIO.IN)

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


# Subroutine for when the first variable changes
def visual_alarm(changed_value):
    IAQ = int(changed_value)
    # Custom logic for input1
    if IAQ == 1:
        print("Environment is safe")
    
    elif IAQ == 2:
        print("Environment is Unhealthy")
        GPIO.output(18, False)
        GPIO.output(16, True)
	
    elif IAQ == 3: 
        print("Environment is Dangerous")
        GPIO.output(16, False)
        GPIO.output(18, True)
    else:
        GPIO.output(16, False)
        GPIO.output(18, False)
        GPIO.output(11,False)
        GPIO.output(13,False)
        GPIO.output(15,False)
        GPIO.output(22,False)

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
    elif senssor == 3:
        print ("PM data has been sent from sensor 3")
        GPIO.output(11,False)
        GPIO.output(13,False)
        GPIO.output(15,True)
        GPIO.output(22,False)
    else:
        print ("PM data has been sent from sensor 3")
        GPIO.output(11,False)
        GPIO.output(13,False)
        GPIO.output(15,False)
        GPIO.output(22,True)
# Main program loop
def main():
    # Create two instances of the VariableWatcher class, one for each input
    watcher1 = VariableWatcher(identifier="input1")  # First input watcher
    watcher2 = VariableWatcher(identifier="input2")  # Second input watcher
    
    while True:
        # Prompt the user for both inputs at once
        user_input = input("Please enter the PM data followed by a space and the sensor it was sent from. \n 1 = healthy \n 2 = moderate \n 3 = dangerous (e.g., '1 1')")
        
        # Split the input string into two parts (values)
        inputs = user_input.split()
        
        if len(inputs) == 2:
            # Assign values to the watchers
            watcher1.value = inputs[0]
            watcher2.value = inputs[1]
        else:
            print("Invalid input. Please enter exactly two values separated by a space.")
            
def Callback(channel):
   state = GPIO.input(channel)
   if state:
      GPIO.output(16,False)
      GPIO.output(18,False)
   else:
      return

GPIO.add_event_detect(37, GPIO.FALLING, callback = Callback, bouncetime = 300)  

while(True):
   time.sleep(1)


if __name__ == "__main__":
    main()


#loop for a certain interval and exit loop and wait for user input


