#initialization
import RPi.GPIO as GPIO   
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
#Visual Alarm GPIO ports
GPIO.setup(16,GPIO.OUT)                  
GPIO.setup(18,GPIO.OUT)
#sensor 1 designation GPIO ports
GPIO.setup(3,GPIO.OUT)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(7,GPIO.OUT)
#sensor 2 designation GPIO ports
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
#sensor 3 designation GPIO ports
GPIO.setup(19,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
#sensor 4 designation GPIO ports
GPIO.setup(29,GPIO.OUT)
GPIO.setup(31,GPIO.OUT)
GPIO.setup(33,GPIO.OUT)
#Acknowledgement switch GPIO ports
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

Moderate_Alarm = pygame.mixer.Sound('/home/freshair/Downloads/ModerateAlarm.wav')
Dangerous_Alarm = pygame.mixer.Sound('/home/freshair/Downloads/DangerousAlarm.wav')


class VariableWatcher:                               
    def __init__(self, value=None, identifier=None):     #THIS SECTION OF CODE WAS ADAPTED FROM AN AI-GENERATED EXAMPLE
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
        # Call the appropriate subroutine based on the identifier
        if self.identifier == "input1":
            alarm(new_value)

# Subroutine for when the first variable changes
def alarm(changed_value):
    IAQ = int(changed_value)
    # Custom logic for input1
    if IAQ == 1:
        if sensor == 1:
            GPIO.output(3,True)
            GPIO.output(5,False)
            GPIO.output(7,False)
        elif sensor == 2:
            GPIO.output(11,True)
            GPIO.output(13,False)
            GPIO.output(15,False)
        elif sensor == 3:
            GPIO.output(19,True)
            GPIO.output(21,False)
            GPIO.output(23,False)
        else:
            GPIO.output(29,True)
            GPIO.output(31,False)
            GPIO.output(33,False)
    elif IAQ == 2:
        GPIO.output(18, False)
        GPIO.output(16, True)
        Moderate_Alarm.play()
        if sensor == 1:
            GPIO.output(3,False)
            GPIO.output(5,True)
            GPIO.output(7,False)
        elif sensor == 2:
            GPIO.output(11,False)
            GPIO.output(13,True)
            GPIO.output(15,False)
        elif sensor == 3:
            GPIO.output(19,False)
            GPIO.output(21,True)
            GPIO.output(23,False)
        else:
            GPIO.output(29,False)
            GPIO.output(31,True)
            GPIO.output(33,False)
    elif IAQ == 3: 
        GPIO.output(16, False)
        GPIO.output(18, True)
        Dangerous_Alarm.play()
        if sensor == 1:
            GPIO.output(3,False)
            GPIO.output(5,False)
            GPIO.output(7,True)
        elif sensor == 2:
            GPIO.output(11,False)
            GPIO.output(13,False)
            GPIO.output(15,True)
        elif sensor == 3:
            GPIO.output(19,False)
            GPIO.output(21,False)
            GPIO.output(23,True)
        else:
            GPIO.output(29,False)
            GPIO.output(31,False)
            GPIO.output(33,True)
# Main program loop
def main():		#THIS SECTION OF CODE WAS ADAPTED FROM AN AI-GENERATED EXAMPLE
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
            print("Invalid input. Please enter exactly two values separated by a space.")		#END OF AI-GENERATED EXAMPLE


def button_callback(channel):
    GPIO.output(16,False)
    GPIO.output(18, False)

GPIO.add_event_detect(37,GPIO.RISING,callback=button_callback) # Setup event on pin 10 rising edge

if __name__ == "__main__":
    main()


#loop for a certain interval and exit loop and wait for user input


