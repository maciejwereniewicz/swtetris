import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)

# Set PWM frequency (Hz) and duty cycle (percentage)
pwm = GPIO.PWM(32, 440)  # 440Hz (A4 note, for example)
pwm.start(50)  # 50% duty cycle

try:
    while True:
        time.sleep(0.1)  # Keeps the program running

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
