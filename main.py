import RPi.GPIO as GPIO
from time import sleep

pin=32 
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(pin, GPIO.OUT)
p=GPIO.PWM(pin, 10)

notes = {'C' : 523.25, 'D' : 587.33, 'E' : 659.25, 'F' : 349.23, 'G' : 392.00, 'A' : 440.00, 'B' : 493.88, '#' : 0.5, 'Ab' : 415.30}

tetris = ["E","B","C","D","C","B","A","A","C","E","D","C","B","C","D","E","C","A","A","D","F","A","G","F","E","C","E","D","C","B","B","C","D","E","C","A","A","","E","B","C","D","C","B","A","A","C","E","D","C","B","C","D","E","C","A","A","D","F","A","G","F","E","C","E","D","C","B","B","C","D","E","C","A","A","","E","C","D","B","C","A","Ab","B","E","C","D","B","C","E","A","Ab","","E","B","C","D","C","B","A","A","C","E","D","C","B","C","D","E","C","A","A","D","F","A","G","F","E","C","E","D","C","B","B","C","D","E","C","A","A","","E","B","C","D","C","B","A","A","C","E","D","C","B","C","D","E","C","A","A","D","F","A","G","F","E","C","E","D","C","B","B","C","D","E","C","A","A","E","C","D","B","C","A","Ab","B","E","C","D","B","C","E","A","Ab"]

p.start(50)

def play_sound(sound):
    p.ChangeFrequency(notes[sound])
    sleep(0.2)
    p.ChangeFrequency(10)
	

def play_song(song):
	for sound in song:
		play_sound(sound)
while True:
	play_song(tetris)