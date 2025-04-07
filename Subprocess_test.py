  
import subprocess
import os
import time

# Path to the sensor_id file
sensor_data_file = '/home/freshair/sensor_data.txt'

# Function to reset the sensor_id file and initialize sensor values
def reset_sensors():
    # Erase the sensor_id file if it exists
    if os.path.exists(sensor_data_file):
        os.remove(sensor_data_file)
        print(f"{sensor_data_file} has been erased.")

    # Initialize sensor values to 1
    global sensor_1, sensor_2, sensor_3, sensor_4
    sensor_1 = 1
    sensor_2 = 1
    sensor_3 = 1
    sensor_4 = 1
    print("All sensor values initialized to 1.")

# Define the possible IAQ and sensor values
IAQ_values = [1, 2, 3]  # You can extend this list with more IAQ values if needed
sensor_values = [1, 2, 3, 4]  # You can extend this list with more sensor values if needed

# Function to run tests for each combination of IAQ and sensor values
def run_tests(IAQ_values, sensor_values):
    # Loop through every combination of IAQ and sensor
    for IAQ in IAQ_values:
        for sensor in sensor_values:
            # Run the script using subprocess with the combination of IAQ and sensor
            print(f"Running test for IAQ: {IAQ}, Sensor: {sensor}")
            
            # Execute the script with the specific IAQ and sensor values
            subprocess.run(['python','/home/freshair/Documents/Testing_Codes/User_Interface/Testing_Plan_Main_Copy.py', str(IAQ), str(sensor)] ,text=True, timeout=3)
            
            # Check if the process completed successfully
                       
            # Optional: Add a delay between tests (if needed) to prevent overlap or system strain
            time.sleep(1)  # Adjust this delay as needed

# Reset sensors and erase sensor_id file
reset_sensors()

# Run tests in the original order
print("Running tests in the original order:")
run_tests(IAQ_values, sensor_values) 
reset_sensors()
# Run tests in reverse order (reversing the lists)
print("\nRunning tests in the reverse order:")
run_tests(IAQ_values[::-1], sensor_values[::-1])
