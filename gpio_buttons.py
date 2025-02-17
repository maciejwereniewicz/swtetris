import RPi.GPIO as GPIO
import time
import os
import subprocess
import signal  # Ensure signal module is imported
import sys

# Set up GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# List of pins connected to buttons
K1_pin = 12
K2_pin = 16
K3_pin = 18

button_pins = [K1_pin, K2_pin, K3_pin]
button_state = {'K1': False, 'K2': False, 'K3': False}
main = None
started = False
# Set up each pin as input with an internal pull-up resistor
for pin in button_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def read_button_states():
    states = {}
    for pin in button_pins:
        # Read the state of each button (LOW when pressed, HIGH when not pressed)
        states[pin] = GPIO.input(pin)
    return states

def kill_main_script(main):
    if main:
        main.kill()

def restart_script():
    # Open a new gnome-terminal and run the button_control.sh script
    #subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', 'sh /home/malo/Desktop/swtetris/button_control.sh; exec bash'])
    sys.exit()  # Exit the current instance of the script
    
def run_main_script():
    # Run the main.py script in the background with correct argument formatting
    return subprocess.Popen(["python", "/home/malo/Desktop/swtetris/main.py"])

def git_pull():
    # Change directory and pull the latest from git
    subprocess.run(["bash", "-c", "cd /home/malo/Desktop/swtetris &&sudo git pull"])

try:
    while True:
        states = read_button_states()

        if states[K1_pin] == GPIO.LOW and button_state['K1'] == False:  # K1 button pressed
            button_state['K1'] = True
            if not started:
                print("No process to kill")
                continue
            print("K1 pressed - Killing main.py script.")
            kill_main_script(main)
            started = False

        if states[K2_pin] == GPIO.LOW and button_state['K2'] == False:  # K2 button pressed
            button_state['K2'] = True
            if started:
                print("Already started")
                continue
            print("K2 pressed - Running main.py.")
            main = run_main_script()
            started = True

        if states[K3_pin] == GPIO.LOW and button_state['K3'] == False:  # K3 button pressed
            button_state['K3'] = True
            print("K3 pressed - Running git pull and restarting script.")
            git_pull()
            GPIO.cleanup()  # Clean up GPIO settings
            restart_script()  # Restart the script after git pull
        if states[K1_pin]:
            button_state['K1'] = False
        if states[K2_pin]:
            button_state['K2'] = False
        if states[K3_pin]:
            button_state['K3'] = False

        time.sleep(0.2)  # Add a small delay to debounce the buttons

except KeyboardInterrupt:
    print("Program stopped by user.")
finally:
    GPIO.cleanup()  # Clean up GPIO settings
