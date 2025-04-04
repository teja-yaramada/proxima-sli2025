import time
import board
import busio
import adafruit_bme680  # BME688 can be used with BME680 library
import adafruit_bno08x
from adafruit_bno08x.i2c import BNO08X_I2C  # Corrected to use BNO08X for IMU
import math

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize BME688 (same library as BME680)
bme = adafruit_bme680.Adafruit_BME680_I2C(i2c)

# Initialize BNO08X
imu = BNO08X_I2C(i2c)
imu.enable_feature(adafruit_bno08x.BNO_REPORT_LINEAR_ACCELERATION)  # Enable linear acceleration reporting

# Constants
g = 9.80665  # Gravity (m/s^2)

# Minimal threshold for accelerometer (e.g., if total acceleration is below 0.2g)
min_threshold = 0.2  # The threshold value you want to set

# Reference pressure at ground level
p0 = bme.pressure

# Function to calculate altitude from pressure
def pressure_altitude(pressure, temperature):
    return ( ( (p0 / pressure) ** (1/5.257) - 1 ) * (temperature + 273.15) ) / 0.0065

# IMU Bias Calibration
print("Calibrating IMU... Hold still.")
num_samples = 100
accel_bias = [0, 0, 0]
for _ in range(num_samples):
    ax, ay, az = imu.linear_acceleration
    accel_bias[0] += ax
    accel_bias[1] += ay
    accel_bias[2] += az
    time.sleep(0.01)
accel_bias = [x / num_samples for x in accel_bias]
accel_bias[2] -= g  # Compensate for gravity
print("Calibration complete.")

# Time tracking
prev_time = time.monotonic()

while True:
    # Read sensor data
    pressure = bme.pressure
    temperature = bme.temperature
    altitude_pressure = pressure_altitude(pressure, temperature)

    accel_x, accel_y, accel_z = imu.linear_acceleration

    # Calculate total acceleration (magnitude)
    total_acceleration = math.sqrt(accel_x**2 + accel_y**2 + accel_z**2)

    # Time delta
    current_time = time.monotonic()
    dt = current_time - prev_time
    prev_time = current_time

    # Only trust the pressure reading if total acceleration is below the threshold
    if total_acceleration < min_threshold:
        altitude = altitude_pressure  # Trust the pressure-based altitude

    print(f"Altitude: {altitude:.2f} m (Pressure-based)")

    time.sleep(0.1)
