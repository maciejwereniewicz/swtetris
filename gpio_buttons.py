import RPi.GPIO as GPIO
import time
import os
import subprocess

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

def kill_python_processes():
    # Avoid killing this script by excluding it from the kill command
    pid = os.getpid()
    # Get all Python 3 process IDs, exclude the current script's PID, then kill them
    processes = subprocess.check_output("pgrep -f python3", shell=True).decode().splitlines()
    for process_pid in processes:
        if process_pid != str(pid):  # Make sure not to kill the current script
            os.kill(int(process_pid), signal.SIGTERM)  # Send SIGTERM to kill the process


def run_main_script():
    # Run the main.py script in the background
    subprocess.Popen(["python3", "/home/malo/Desktop/swtetris/main.py"])

def git_pull():
    # Change directory and pull the latest from git
    subprocess.run(["bash", "-c", "cd /home/malo/Desktop/swtetris && git pull"])

try:
    while True:
        states = read_button_states()

        if states[K1_pin] == GPIO.LOW:  # K1 button pressed
            print("K1 pressed - Killing all Python processes.")
            kill_python_processes()

        if states[K2_pin] == GPIO.LOW:  # K2 button pressed
            print("K2 pressed - Running main.py.")
            run_main_script()

        if states[K3_pin] == GPIO.LOW:  # K3 button pressed
            print("K3 pressed - Running git pull.")
            git_pull()

        time.sleep(0.2)  # Add a small delay to debounce the buttons

except KeyboardInterrupt:
    print("Program stopped by user.")
finally:
    GPIO.cleanup()  # Clean up GPIO settings
