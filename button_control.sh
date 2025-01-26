#!/bin/sh
xinput disable "ADS7846 Touchscreen"
while true
do
python3 /home/malo/Desktop/swtetris/gpio_buttons.py
done