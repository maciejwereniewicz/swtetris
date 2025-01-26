import RPi.GPIO as GPIO
from time import sleep
from sys import exit

pin=32
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)
p=GPIO.PWM(pin, 10)

notes = {'C' : 523.25, 'D' : 587.33, 'E' : 659.25, 'F' : 349.23, 'G' : 392.00, 'A' : 440.00, 'B' : 493.88, '#' : 0.5, 'Ab' : 415.30}
speed = {'sw' : 1,'w' : 0.8, 'h' : 0.6 , 'q' : 0.45, 'qh' : 0.25, 'qhh' : 0.15}

s1 = ['E-q','B-qh','C-qh','D-q','C-qh','B-qh','A-q',
'A-qh','C-qh','E-q','D-qh','C-q','B-qhh',
'C-q','D-q','E-q','C-h','A-qh','A-q',
'D-qh','F-qh','A-h','G-qhh','F-h','E-qh',
'C-qh','E-h','D-qhh','C-h','B-qh',
'B-qh','C-q','D-q','E-qh','C-h','A-h','A-h','#-w']

s2 = ['E-sw','C-sw','D-sw','B-sw','C-sw','A-sw','Ab-sw','B-w','#-q',
'E-sw','C-sw','D-sw','B-sw','C-h','A-h','A-h','Ab-sw','#-sw']

tetris = [s1,s1,s2,s1,s1,s2,s1]

p.start(50)

header = '[Note]\t[Frequency]\t[Duration]'+'\n------\t-----------\t----------'
printcount = 0

def goodbye(msg = ''):
	print(msg + '\n\nDone! Have fun. Like. Comment below. Kill yourself.')
	exit()

def play_song(song):
	global header,printcount,notes,speed
	try:
		print(header)
		songposition = 0
		for x in song:
			songposition += 1
			if(songposition >= (len(song))):
				goodbye('\nSong finished...')
			for y in x:
				y = y.split('-')
				note = y[0]
				length = y[1]
				actualspeed = round(float(speed[length]),2)
				print('  '+note + '\t   ' + str(notes[note]) + '\t   ' + str(actualspeed))
				printcount += 1
				if(printcount == 23):
					printcount = 0
					print(header)
				p.ChangeFrequency(notes[note])
				sleep(actualspeed)
				p.ChangeFrequency(10)
	except KeyboardInterrupt:
		goodbye()

while True:
	play_song(tetris)