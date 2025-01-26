import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


# List of pins connected to buttons

left_pin = 29
right_pin = 31
down_pin = 33
rotate_pin = 35

select_pin=38
start_pin=40


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
z = 0
try:
    while True:
        z+=1
        # Get button states
        states = read_button_states()
        for pin, state in states.items():
            print(f"{z} - Button on pin {pin} is {'Pressed' if state == GPIO.LOW else 'Released'}")
        
        time.sleep(0.2)  # Delay to reduce CPU usage

except KeyboardInterrupt:
    print("Program interrupted")

finally:
    GPIO.cleanup()  # Clean up GPIO settings
