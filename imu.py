import time
import board
import busio
import adafruit_bno08x
from adafruit_bno08x.i2c import BNO08X_I2C

class BNO08XSensor:
    def __init__(self):
        """
        Initializes the BNO08X imu and sets up the I2C connection.
        """
        # Initialize I2C
        self.i2c = busio.I2C(board.SCL, board.SDA)

        # Initialize the BNO08X imu
        self.bno = BNO08X_I2C(self.i2c)

        # Enable required imu reports
        self.bno.enable_feature(adafruit_bno08x.BNO_REPORT_ACCELEROMETER)
        self.bno.enable_feature(adafruit_bno08x.BNO_REPORT_GYROSCOPE)
        self.bno.enable_feature(adafruit_bno08x.BNO_REPORT_MAGNETOMETER)

        # Initialize imu values
        self.accel_x = None
        self.accel_y = None
        self.accel_z = None
        self.gyro_x = None
        self.gyro_y = None
        self.gyro_z = None
        self.mag_x = None
        self.mag_y = None
        self.mag_z = None

    def read_data(self):
        """
        Reads the data from the BNO08X imu and stores it in the object.
        
        :return: A tuple containing acceleration, gyroscope, and magnetometer data
        """
        try:
            # Read the imu data
            self.accel_x, self.accel_y, self.accel_z = self.bno.acceleration
            self.gyro_x, self.gyro_y, self.gyro_z = self.bno.gyro
            self.mag_x, self.mag_y, self.mag_z = self.bno.magnetic

            # Print the data
            print("----------------------------------")
            print(f"Acceleration: X: {self.accel_x:.3f} Y: {self.accel_y:.3f} Z: {self.accel_z:.3f} m/s²")
            print(f"Gyroscope: X: {self.gyro_x:.3f} Y: {self.gyro_y:.3f} Z: {self.gyro_z:.3f} rad/s")
            print(f"Magnetometer: X: {self.mag_x:.3f} Y: {self.mag_y:.3f} Z: {self.mag_z:.3f} uT")
            print("----------------------------------")

            return (self.accel_x, self.accel_y, self.accel_z, 
                    self.gyro_x, self.gyro_y, self.gyro_z, 
                    self.mag_x, self.mag_y, self.mag_z)

        except RuntimeError as e:
            print(f"RuntimeError: {e}. Retrying...")
            time.sleep(1)
            return None

    def to_string(self):
        """
        Returns a string representation of the imu's current data.
        
        :return: A formatted string with imu data.
        """

        self.read_data()

        return (f"Acceleration: X: {self.accel_x:.3f} Y: {self.accel_y:.3f} Z: {self.accel_z:.3f} m/s², "
                f"Gyroscope: X: {self.gyro_x:.3f} Y: {self.gyro_y:.3f} Z: {self.gyro_z:.3f} rad/s, "
                f"Magnetometer: X: {self.mag_x:.3f} Y: {self.mag_y:.3f} Z: {self.mag_z:.3f} uT")

    def test(self):
        """
        Runs a basic test to ensure the imu is working by reading and printing data.
        """
        print("Testing BNO08X imu...")
        self.read_data()
        print("Test completed successfully!")

    def stop(self):
        """
        Perform any necessary cleanup actions.
        """
        print("Cleaning up imu resources...")
        time.sleep(1)  # Example cleanup action

# Example usage
if __name__ == "__main__":
    # Create BNO08X imu object
    imu = BNO08XSensor()

    try:
        # Run the test function
        imu.test()

        # Optionally, read and log the data continuously
        # while True:
        #     imu.read_data()
        #     print(imu.to_string())  # Logging the imu data
        #     time.sleep(1)  # Read every second

    except KeyboardInterrupt:
        print("Program interrupted by user.")
    
    finally:
        # Cleanup
        imu.stop()
