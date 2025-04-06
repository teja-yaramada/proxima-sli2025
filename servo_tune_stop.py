#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

SERVO_PIN = 18       # BCM pin number
INITIAL_DUTY_CYCLE = 6.85  # The typical neutral value for a continuous servo

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

pwm = GPIO.PWM(SERVO_PIN, 50)  # 50 Hz for standard servos
pwm.start(INITIAL_DUTY_CYCLE)

print("Interactive Continuous Servo Tuner")
print("----------------------------------")
print("Use '+' or '-' to adjust the duty cycle in small steps.")
print("Press 'q' to quit.\n")

try:
    current_duty_cycle = INITIAL_DUTY_CYCLE
    step = 0.1  # Step size for each increment/decrement

    while True:
        user_input = input("Enter + or - to adjust, q to quit: ").strip()
        if user_input == '+':
            current_duty_cycle += step
            pwm.ChangeDutyCycle(current_duty_cycle)
            print(f"Duty cycle set to {current_duty_cycle:.1f}%")
        elif user_input == '-':
            current_duty_cycle -= step
            pwm.ChangeDutyCycle(current_duty_cycle)
            print(f"Duty cycle set to {current_duty_cycle:.1f}%")
        elif user_input == 'q':
            break
        else:
            print("Invalid input. Please enter '+', '-', or 'q' to quit.")

except KeyboardInterrupt:
    pass
finally:
    print("Stopping PWM and cleaning up GPIO.")
    pwm.stop()
    GPIO.cleanup()
