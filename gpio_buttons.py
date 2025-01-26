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
    pid = os.getpid()  # Get current script's PID
    try:
        # Get all Python 3 process IDs
        processes = subprocess.check_output("pgrep -f python3", shell=True).decode().splitlines()
        for process_pid in processes:
            if process_pid != str(pid):  # Exclude the current script's PID
                try:
                    # Attempt to send SIGTERM to the process
                    os.kill(int(process_pid), signal.SIGTERM)
                    print(f"Terminating process {process_pid}")
                except ProcessLookupError:
                    # Process already terminated
                    print(f"Process {process_pid} already terminated or not found.")
    except subprocess.CalledProcessError:
        # If no Python processes are found or other errors with pgrep
        print("No Python processes found to kill.")

def run_main_script():
    # Run the main.py script in the background
    subprocess.Popen(["python3", "/home/malo/Desktop/swtetris/main.py"])

def git_pull():
    # Change directory and pull the latest from git
    subprocess.run(["bash", "-c", "cd /home/malo/Desktop/swtetris && git pull"])

def restart_script():
    # Restart the current script after git pull
    python = sys.executable
    script = sys.argv[0]
    subprocess.Popen([python, script])
    sys.exit()  # Exit the current instance of the script

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
            print("K3 pressed - Running git pull and restarting script.")
            git_pull()
            restart_script()  # Restart the script after git pull

        time.sleep(0.2)  # Add a small delay to debounce the buttons

except KeyboardInterrupt:
    print("Program stopped by user.")
finally:
    GPIO.cleanup()  # Clean up GPIO settings
