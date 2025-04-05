import time
import os
import threading
from imu import BNO08XSensor  # Import the IMU sensor class
from sensor import BME688Sensor  # Import the sensor class
from servo import Servo
from solenoid import SolenoidController
import logging
from datetime import datetime

collection_period = 2
collection_range_maximum = 1
collection_range_minimum = 0.1
plateau_count = 0
plateau_threshold = 3
triggered = False

# Global objects for IMU and Sensor
imu = BNO08XSensor()  # Instantiate IMU sensor
sensor = BME688Sensor()  # Instantiate the BME688 sensor
servo = Servo(pin=18)
solenoid = SolenoidController(pin=4)

# Ensure the 'logs' directory exists
log_directory = 'sli/logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Set up logging configuration
log_filename = os.path.join(log_directory, datetime.now().strftime("telemetry_log_%Y-%m-%d_%H-%M-%S.log"))
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(message)s')

def log_telemetry():
    """
    Logs telemetry data from both the IMU and the sensor to the log file.
    """
    # Get the telemetry data from both IMU and sensor
    imu_data = imu.to_string()  # Get string representation of IMU data
    sensor_data = sensor.to_string()  # Get string representation of Sensor data

    # Log the telemetry data
    logging.info(f"IMU Telemetry: {imu_data}")  # Log the IMU data
    logging.info(f"Sensor Telemetry: {sensor_data}")  # Log the sensor data
    logging.info("-----------------------------------------------------------------------------------------------")

def poll():

    global plateau_count, plateau_threshold,  collection_period, collection_range_maximum, collection_range_minimum, triggered

    if plateau_count >= plateau_threshold and not triggered:
        sample()
        triggered = True

    if sensor.calculate_displacement() <= collection_range_maximum and sensor.calculate_displacement() >= collection_range_minimum and (not triggered):
        plateau_count = plateau_count + 1
        logging.info(f"Plateau Count: {plateau_count}")
    else:
        plateau_count = 0

    print(f"Plateau Count: {plateau_count}")


def sample():
    logging.info("--------------Sampling Start--------------")
    solenoid.activate()
    servo.run_continuously(speed=1, duration=collection_period)
    solenoid.deactivate()
    logging.info("--------------Sampling End--------------")


def sequential_execution():
    logging.info("*** Sequential Execution ***")
    print("Starting telemetry logging...")
    solenoid.deactivate()
    servo.set_speed(0)

    # Run a continuous loop to log both IMU and sensor data
    while True:
        # Log both IMU and sensor telemetry data
        log_telemetry()
        poll()
            
        time.sleep(0.5)  # Wait before reading again
        #sample()

def parallel_execution():
    logging.info("*** Parallel Execution ***")
    solenoid.deactivate()
    servo.set_speed(0)

    telemetry_thread = threading.Thread(target=log_telemetry)
    sampling_thread = threading.Thread(target=poll)

    telemetry_thread.start()
    sampling_thread.start()

    telemetry_thread.join()
    sampling_thread.join()



def main():
    try:
        sequential_execution()

    except KeyboardInterrupt:
        print("Telemetry logging stopped by user.")
    
    finally:
        # Clean up and stop the PWM signal
        servo.stop()
        solenoid.stop()
        sensor.stop()
        imu.stop()

if __name__ == "__main__":
    main()

