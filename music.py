import RPi.GPIO as GPIO
from time import sleep

pin=32 
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(pin, GPIO.OUT)
p=GPIO.PWM(pin, 10)

notes = {'C' : 523.25, 
         'D' : 587.33, 
         'E' : 659.25, 
         'F' : 349.23, 
         'G' : 392.00, 
         'A' : 440.00, 
         'B' : 493.88, 
         'Ab' : 415.30,
		 'rotate': 100}

tet1 = ["E","B","C","D","C","B","A",
		  "A","C","E","D","C","B",
		  "C","D","E","C","A","A",
		  "D","F","A","G","F","E",
		  "C","E","D","C","B",
		  "B","C","D","E","C","A","A",]

tet2 = ["E","C","D","B","C","A","Ab","B",
		  "E","C","D","B","C","E","A","Ab"]

tetris = [*tet1,*tet1,*tet2,*tet1,*tet1,*tet2]

rotate = ["rotate"]
line = ['B', 'D']


p.start(50)
p.ChangeDutyCycle(0)

def play_sound(sound):
    p.ChangeDutyCycle(50)
    p.ChangeFrequency(notes[sound])
    sleep(0.35)
    p.ChangeFrequency(10)
    p.ChangeDutyCycle(0)

def play_song(song):
	for sound in song:
		play_sound(sound)
	
def rotate_sound():
	play_sound('rotate')
	
def tetris_theme():
	while True:
	    play_song(tetris)
	
def line_sound():
    for i in ['B','D']:
        print(i)
        play_sound(i)
        sleep(0.1)