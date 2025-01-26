import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


# List of pins connected to buttons

K1_pin = 12
K2_pin = 16
K3_pin = 18


button_pins = [K1_pin, K2_pin, K3_pin]


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
