# servo_control.py

import RPi.GPIO as GPIO
import time

class Servo:
    def __init__(self, pin, frequency=50):
        """
        Initializes the Servo class with a GPIO pin and frequency for PWM.
        
        :param pin: The GPIO pin number where the servo is connected.
        :param frequency: The PWM frequency (default 50Hz, standard for servos).
        """
        self.pin = pin
        self.frequency = frequency

        # Set up GPIO mode
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

        # Set up PWM on the specified pin with the specified frequency
        self.pwm = GPIO.PWM(self.pin, self.frequency)
        self.pwm.start(7.5)  # Start PWM with a 7.5% duty cycle (stop position)

    def set_speed(self, speed):
        """
        Set the speed of the continuous rotation servo.

        :param speed: A float between -1 and 1 indicating the speed:
                      -1 for full reverse, 0 for stop, and 1 for full forward.
        """
        # Map the speed to a duty cycle between 2.5% and 12.5%
        if speed > 1:
            speed = 1
        elif speed < -1:
            speed = -1

        # Map the speed to a duty cycle range:
        duty_cycle = 7.5 + (speed * 5)  # Maps -1 -> 2.5%, 0 -> 7.5%, 1 -> 12.5%
        self.pwm.ChangeDutyCycle(duty_cycle)
        print(f"Set speed to {speed}, Duty Cycle: {duty_cycle}%")

    def run_continuously(self, speed, duration=5):
        """
        Run the servo continuously at a given speed for a specified duration.
        
        :param speed: A float between -1 and 1 indicating the speed.
        :param duration: The duration in seconds to run the servo.
        """
        print(f"Running for {duration} seconds at speed {speed}...")
        self.set_speed(speed)
        time.sleep(duration)
        print("Stopping servo...")
        self.set_speed(0)  # Stop the servo

    def stop(self):
        """
        Stops the PWM signal and cleans up the GPIO resources.
        """
        self.pwm.stop()
        # GPIO.cleanup()

    def test(self):
        """
        Runs a basic test sequence by making the servo run at various speeds.
        This helps verify that the servo is working as expected.
        """
        print("Running basic test sequence...")
        speeds = [-1, -0.5, 0, 0.5, 1]  # Full reverse, half reverse, stop, half forward, full forward
        for speed in speeds:
            print(f"Running at speed {speed}...")
            self.run_continuously(speed, duration=2)
        print("Test sequence complete.")


# Example usage
if __name__ == "__main__":
    # Create a Servo object on GPIO pin 1
    servo = Servo(pin=18)

    try:
        # Run the test sequence to verify functionality
        # servo.run_continuously(speed=1, duration=5)
        servo.test()

        # Optionally, run the servo at specific speeds
        # servo.run_continuously(1, duration=5)  # Full speed forward for 5 seconds
        # servo.run_continuously(-1, duration=5)  # Full speed reverse for 5 seconds

    except KeyboardInterrupt:
        print("Program interrupted by user.")

    finally:
        # Clean up and stop the PWM signal
        servo.stop()
