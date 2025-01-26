import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setwarnings(False)

# List of pins connected to buttons

left_pin = 21
right_pin = 22
down_pin = 23
rotate_pin = 24

select_pin=28
start_pin=29

button_pins = [left_pin, right_pin, down_pin, rotate_pin, select_pin, start_pin]


# Set up each pin as input with an internal pull-up resistor
for pin in button_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def read_button_states():
    states = {}
    for pin in button_pins:
        # Read the state of each button (LOW when pressed, HIGH when not pressed)
        states[pin] = GPIO.input(pin)
    return states

try:
    while True:
        # Get button states
        states = read_button_states()
        for pin, state in states.items():
            print(f"Button on pin {pin} is {'Pressed' if state == GPIO.LOW else 'Released'}")
        
        time.sleep(0.2)  # Delay to reduce CPU usage

except KeyboardInterrupt:
    print("Program interrupted")

finally:
    GPIO.cleanup()  # Clean up GPIO settings
