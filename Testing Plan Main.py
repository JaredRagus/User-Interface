#initialization
import RPi.GPIO as GPIO   
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(4,GPIO.out)                  #Visual Alarm GPIO ports
GPIO.setup(5,GPIO.out)
#sensor designation GPIO ports

#Acknowledgement switch GPIO ports
GPIO.setup(25, GPIO.in)

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
    if GPIO.input(25):
    # Custom logic for input1
        if IAQ == 1:
            print("Environment is safe")
    
        elif IAQ == 2:
            print("Environment is Unhealthy")
            #GPIO.output(5, false)
            #GPIO.output(4, true)
	
        else: 
            print("Environment is Dangerous")
            #GPIO.output(4, false)
            #GPIO.output(5, true)
    else:
        GPIO.output(4,false)
        GPIO.output(5,false)

# Subroutine for when the second variable changes
def sensor_designation(changed_value):
    sensor = int(changed_value)
    if sensor == 1:
        print ("PM data has been sent from sensor 1")
        #GPIO.output()
    elif sensor == 2:
        print ("PM data has been sent from sensor 2")
        #GPIO.output()
    elif senssor == 3:
        print ("PM data has been sent from sensor 3")
        #GPIO.output()
    else:
        print ("PM data has been sent from sensor 3")
        #GPIO.output()
# Main program loop
def main():
    # Create two instances of the VariableWatcher class, one for each input
    watcher1 = VariableWatcher(identifier="input1")  # First input watcher
    watcher2 = VariableWatcher(identifier="input2")  # Second input watcher
    
    while True:
        # Prompt the user for both inputs at once
        user_input = input("Please enter the PM data followed by a space and the sensor it was sent from. \n 1 = healthy \n 2 = moderate \n 3 = dangerous (e.g., '1 1')")
        
        if user_input.lower() == 'exit':
            break
        
        # Split the input string into two parts (values)
        inputs = user_input.split()
        
        if len(inputs) == 2:
            # Assign values to the watchers
            watcher1.value = inputs[0]
            watcher2.value = inputs[1]
        else:
            print("Invalid input. Please enter exactly two values separated by a space.")
        

if __name__ == "__main__":
    main()


#loop for a certain interval and exit loop and wait for user input


