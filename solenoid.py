import time
import RPi.GPIO as GPIO

class SolenoidController:
    def __init__(self, pin, relay_state=False):
        """
        Initializes the SolenoidController to control a relay and solenoid.
        
        :param pin: The GPIO pin number to control the relay.
        :param relay_state: The initial state of the relay (True to activate, False to deactivate).
        """
        # Set up GPIO mode (BCM or BOARD depending on your wiring)
        GPIO.setmode(GPIO.BCM)  # Use Broadcom pin-numbering scheme (BCM)
        
        # Set up the GPIO pin for output
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        
        # Set the initial state of the relay (True: activated, False: deactivated)
        self.relay_state = relay_state
        
        # Control the relay immediately based on the initial state
        # self.set_relay_state(self.relay_state)

    def set_relay_state(self, state):
        """
        Set the state of the relay (True to activate, False to deactivate).
        
        :param state: True to turn on the relay, False to turn off.
        """
        if state:
            GPIO.output(self.pin, GPIO.HIGH)  # Activate relay (solenoid ON)
            print("Solenoid activated (Relay ON).")
        else:
            GPIO.output(self.pin, GPIO.LOW)  # Deactivate relay (solenoid OFF)
            print("Solenoid deactivated (Relay OFF).")
        self.relay_state = state

    def activate(self):
        """
        Activates the solenoid (turns on the relay).
        """
        self.set_relay_state(True)

    def deactivate(self):
        """
        Deactivates the solenoid (turns off the relay).
        """
        self.set_relay_state(False)

    def toggle(self):
        """
        Toggles the state of the relay (activates if it's off, deactivates if it's on).
        """
        self.set_relay_state(not self.relay_state)

    def test(self):
        """
        Runs a basic test to actuate the solenoid.
        """
        print("Testing SolenoidController...")
        self.deactivate()
        time.sleep(2)
        self.activate()  # Turn on the solenoid
        time.sleep(2)   # Wait for 2 seconds
        self.deactivate()  # Turn off the solenoid
        print("Test completed successfully.")

    def stop(self):
        """
        Cleans up the GPIO setup and releases the resources.
        """
        print("Cleaning up GPIO resources...")
        GPIO.cleanup()

# Example usage
if __name__ == "__main__":
    # Create SolenoidController object and specify the GPIO pin for the relay
    solenoid = SolenoidController(pin=4)  # Pin 17 as example

    try:
        # Run the test function to activate and deactivate the solenoid
        solenoid.test()

        # Optionally, you can continuously toggle or control the solenoid
        # while True:
        #     solenoid.toggle()
        #     time.sleep(2)

    except KeyboardInterrupt:
        print("Program interrupted by user.")
    
    finally:
        # Cleanup GPIO resources when done
        solenoid.stop()
