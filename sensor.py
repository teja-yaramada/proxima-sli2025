import time
import board
import adafruit_bme680

class BME688Sensor:
    def __init__(self, sea_level_pressure=1013.25):
        """
        Initializes the BME688 sensor and sets up I2C connection.
        
        :param sea_level_pressure: The standard sea level pressure in hPa.
        """
        # Create I2C object
        self.i2c = board.I2C()  # Uses default I2C pins (SCL, SDA)

        # Create BME688 sensor object
        self.bme = adafruit_bme680.Adafruit_BME680_I2C(self.i2c)

        # Adjust settings (optional)
        self.bme.sea_level_pressure = sea_level_pressure

        # Initialize sensor values
        self.temperature = None
        self.humidity = None
        self.pressure = None
        self.gas_resistance = None
        self.altitude = None
        self.displacement = None

        self.init_pressure = self.bme.pressure
        self.init_temperature = self.bme.temperature

    def read_data(self):
        """
        Reads the data from the BME688 sensor.
        
        :return: A tuple containing temperature, humidity, pressure, gas resistance, and altitude
        """
        # Read sensor data
        self.temperature = self.bme.temperature
        self.humidity = self.bme.humidity
        self.pressure = self.bme.pressure
        self.gas_resistance = self.bme.gas

        # Calculate altitude using the pressure and sea level pressure
        self.altitude = self.calculate_altitude(pressure=self.pressure, temperature=self.temperature)
        self.displacement = self.calculate_displacement()

        # Print the data
        print("----------------------------------")
        print(f"Temperature: {self.temperature:.2f} C")
        print(f"Humidity: {self.humidity:.2f} %")
        print(f"Pressure: {self.pressure:.2f} hPa")
        print(f"Gas Resistance: {self.gas_resistance:.2f} ohms")
        print(f"Altitude: {self.altitude:.2f} meters")
        print(f"Displacement: {self.displacement:.2f} meters")
        print("----------------------------------")

        return (self.temperature, self.humidity, self.pressure, self.gas_resistance, self.altitude)

    def to_string(self):
        """
        Returns a string representation of the sensor's current data.
        
        :return: A formatted string with sensor data.
        """

        self.read_data()

        return (f"Temperature: {self.temperature:.2f} C, "
                f"Humidity: {self.humidity:.2f} %, "
                f"Pressure: {self.pressure:.2f} hPa, "
                f"Gas Resistance: {self.gas_resistance:.2f} ohms, "
                f"Altitude: {self.altitude:.2f} meters, "
                f"Displacment: {self.displacement:.2f} meters")

    def calculate_altitude(self, pressure, temperature, sea_level_pressure=1013.25):
        """
        Calculates the altitude based on the current pressure, temperature, and sea level pressure.
        
        :param pressure: The current atmospheric pressure in hPa (from the sensor).
        :param temperature: The current temperature in Celsius (from the sensor).
        :param sea_level_pressure: The sea level pressure in hPa (defaults to 1013.25).
        :return: The calculated altitude in meters.
        """
        # Constants
        T0 = 288.15  # Standard temperature at sea level (15°C or 288.15K)
        L = 0.00649  # Temperature lapse rate in K/m
        R = 8.314  # Universal gas constant in J/(mol·K)
        g = 9.80665  # Acceleration due to gravity in m/s²
        M = 0.0289644  # Molar mass of Earth's air in kg/mol

        # Convert temperature to Kelvin
        temperature_kelvin = temperature + 273.15

        # Calculate the altitude using the temperature-adjusted formula
        altitude = (T0 / L) * (1 - (pressure / sea_level_pressure) ** ((R * L) / (g * M)))

        return altitude
    
    def calculate_displacement(self, sea_level_pressure=1013.25):
        starting_altitude = self.calculate_altitude(pressure=self.init_pressure, temperature=self.init_temperature)
        current_altitude = self.calculate_altitude(pressure=self.pressure, temperature=self.temperature)
        return current_altitude - starting_altitude

    def test(self):
        """
        Runs a basic test to ensure the sensor is working by reading data.
        """
        print("Testing BME688 sensor...")
        self.read_data()
        print("Test completed successfully!")

    def stop(self):
        """
        Perform any necessary cleanup actions.
        """
        print("Cleaning up sensor resources...")
        time.sleep(1)  # Example cleanup action

# Example usage
if __name__ == "__main__":
    # Create BME688 sensor object
    sensor = BME688Sensor()

    try:
        # Run the test function
        sensor.test()

        # Optionally, read and log the data continuously
       # while True:
        #    sensor.read_data()
         #   print(sensor.to_string())  # Logging the sensor data
          #  time.sleep(1)  # Read every second

    except KeyboardInterrupt:
        print("Program interrupted by user.")
    
    finally:
        # Cleanup
        sensor.stop()
