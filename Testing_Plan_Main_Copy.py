import RPi.GPIO as GPIO
import pygame
pygame.init()
import sys
import os

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Visual Alarm GPIO ports
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)

# Sensor GPIO ports
GPIO.setup(8, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)

# Acknowledgement switch GPIO ports
sensor_1 = 0
sensor_2 = 0
sensor_3 = 0
sensor_4 = 0
Moderate_Alarm = pygame.mixer.Sound('/home/freshair/Downloads/ModerateAlarm.wav')
Dangerous_Alarm = pygame.mixer.Sound('/home/freshair/Downloads/DangerousAlarm.wav')

# File path to save/load sensor data
sensor_data_file = '/home/freshair/sensor_data.txt'

# Function to save sensor values to a file
def save_sensor_data():
    with open(sensor_data_file, 'w') as file:
        file.write(f"{sensor_1},{sensor_2},{sensor_3},{sensor_4}\n")

# Function to load sensor values from a file
def load_sensor_data():
    global sensor_1, sensor_2, sensor_3, sensor_4
    if os.path.exists(sensor_data_file):
        with open(sensor_data_file, 'r') as file:
            data = file.readline().strip()
            if data:
                sensor_1, sensor_2, sensor_3, sensor_4 = map(int, data.split(','))
            else:
                # Default values if file is empty
                sensor_1, sensor_2, sensor_3, sensor_4 = 1, 1, 1, 1
    else:
        # If file doesn't exist, initialize with default values
        sensor_1, sensor_2, sensor_3, sensor_4 = 1, 1, 1, 1

# VariableWatcher class
class VariableWatcher:
    def __init__(self, value=None, identifier=None):
        self._value = value
        self.identifier = identifier  # To identify which watcher triggered the change

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self._value != new_value:
            self._value = new_value
            self.on_change(new_value)

    def on_change(self, new_value):
        if self.identifier == "input1":
            alarm(new_value)

# Subroutine for when the first variable changes
def alarm(IAQ, sensor, sensor_id):
    if 3 in sensor_id:
        GPIO.output(18, False)
        GPIO.output(16, True)
        Dangerous_Alarm.play()
    elif (2 in sensor_id and 3 not in sensor_id):
        GPIO.output(16, False)
        GPIO.output(18, True)
        Moderate_Alarm.play()
    if IAQ == 3:
        if sensor == 1:
            GPIO.output(8, False)
            GPIO.output(10, False)
            GPIO.output(12, True)
        elif sensor == 2:
            GPIO.output(11, False)
            GPIO.output(13, False)
            GPIO.output(15, True)
        elif sensor == 3:
            GPIO.output(19, False)
            GPIO.output(21, False)
            GPIO.output(23, True)
        else:
            GPIO.output(29, False)
            GPIO.output(31, False)
            GPIO.output(33, True)
    elif IAQ == 2:
        if sensor == 1:
            GPIO.output(8, False)
            GPIO.output(10, True)
            GPIO.output(12, False)
        elif sensor == 2:
            GPIO.output(11, False)
            GPIO.output(13, True)
            GPIO.output(15, False)
        elif sensor == 3:
            GPIO.output(19, False)
            GPIO.output(21, True)
            GPIO.output(23, False)
        else:
            GPIO.output(29, False)
            GPIO.output(31, True)
            GPIO.output(33, False)
    elif IAQ == 1:
        if sensor == 1:
            GPIO.output(8, True)
            GPIO.output(10, False)
            GPIO.output(12, False)
        elif sensor == 2:
            GPIO.output(11, True)
            GPIO.output(13, False)
            GPIO.output(15, False)
        elif sensor == 3:
            GPIO.output(19, True)
            GPIO.output(21, False)
            GPIO.output(23, False)
        else:
            GPIO.output(29, True)
            GPIO.output(31, False)
            GPIO.output(33, False)
# Main program loop
def main():
    global sensor_1, sensor_2, sensor_3, sensor_4

    # Load saved sensor data
    load_sensor_data()

    # Split the input string into two parts (values)
    IAQ = sys.argv[1]
    IAQ = int(IAQ)
    sensor = sys.argv[2]
    sensor = int(sensor)

    if sensor == 1:
        sensor_1 = IAQ
    elif sensor == 2:
        sensor_2 = IAQ
    elif sensor == 3:
        sensor_3 = IAQ
    elif sensor == 4:
        sensor_4 = IAQ

    sensor_id = (sensor_1, sensor_2, sensor_3, sensor_4)

    # Call alarm function based on sensor change
    alarm(IAQ, sensor, sensor_id)

    # Save the updated sensor data after processing
    save_sensor_data()

# If the script is executed directly, run the main function
if __name__ == "__main__":
    main()
