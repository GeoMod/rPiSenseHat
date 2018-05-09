#!/usr/bin/python

from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from signal import pause
from subprocess import call
import time

sense = SenseHat()
threshold = float(0.3)

def pushed_up(event):
	if event.action != ACTION_RELEASED:
		pressure = sense.get_pressure()
		converted = (pressure * 1.029) * 0.0295301
		inHG = round(converted, 2)
		sense.show_message(str(inHG), text_colour = [0, 150, 150])
		
		
def pushed_down(event):
	if event.action != ACTION_RELEASED:
		X = [255, 0, 0] # Red
		O = [255, 255, 255] # White
		close = [
		O, O, O, X, X, O, O, O,
		O, O, X, O, O, X, O, O,
		O, X, X, O, O, O, X, O,
		X, O, O, X, O, O, O, X,
		X, O, O, O, X, O, O, X,
		O, X, O, O, O, X, X, O,
		O, O, X, O, O, X, O, O,
		O, O, O, X, X, O, O, O
		]
		sense.set_pixels(close)
		time.sleep(2)
		sense.clear()
		call("sudo nohup shutdown -h now", shell=True)
	
	
def pushed_left(event):
	if event.action != ACTION_RELEASED:
		tempCelsius = sense.get_temperature()
		# Actual C -> F converstion is C * 1.8 + 32. I dropped it by 14deg due to heating of the sensor by the RaspberryPi board beneath.
		tempFahrenheit = (tempCelsius * 1.8) + 18
		sense.show_message(str(round(tempFahrenheit, 1)), text_colour = [0, 0, 150])

	
def pushed_right(event):
	if event.action != ACTION_RELEASED:
		count = 0
		while count < 3000:
			gyro = sense.get_accelerometer_raw()
			accelleration = gyro['z']
			gyroSensing(accelleration)
			count += 1
		sense.clear()


def refresh():
	sense.clear()	

			
		
def gyroSensing(i):
	if i < -threshold:
#		Acceleration
		Y = [0, 100, 0] # Dark Green
		X = [0, 0, 0] # Unlit
		Z = [0, 0, 0]
		O = [0, 0, 0]
		drawPointer = [
		O, O, O, Y, Y, O, O, O,
		O, O, Y, Y, Y, Y, O, O,
		O, Y, Y, Y, Y, Y, Y, O,
		X, X, X, X, X, X, X, X,
		X, X, X, X, X, X, X, X,
		O, Z, Z, Z, Z, Z, Z, O,
		O, O, Z, Z, Z, Z, O, O,
		O, O, O, Z, Z, O, O, O
		]
		sense.set_pixels(drawPointer)
		time.sleep(2)
	elif i > threshold:
#		Deceleration
		X = [0, 0, 0]
		Y = [0, 0, 0]
		Z = [178, 34, 34] #Fire brick
		O = [0, 0, 0]
		drawPointer = [
		O, O, O, Y, Y, O, O, O,
		O, O, Y, Y, Y, Y, O, O,
		O, Y, Y, Y, Y, Y, Y, O,
		X, X, X, X, X, X, X, X,
		X, X, X, X, X, X, X, X,
		O, Z, Z, Z, Z, Z, Z, O,
		O, O, Z, Z, Z, Z, O, O,
		O, O, O, Z, Z, O, O, O
		]
		sense.set_pixels(drawPointer)
	else:
		X = [0, 206, 209] #Turquoise
		Z = [0, 0, 0]
		Y = [0, 0, 0]
		O = [0, 0, 0]
		drawPointer = [
		O, O, O, Y, Y, O, O, O,
		O, O, Y, Y, Y, Y, O, O,
		O, Y, Y, Y, Y, Y, Y, O,
		X, X, X, X, X, X, X, X,
		X, X, X, X, X, X, X, X,
		O, Z, Z, Z, Z, Z, Z, O,
		O, O, Z, Z, Z, Z, O, O,
		O, O, O, Z, Z, O, O, O
		]
		sense.set_pixels(drawPointer)
		
			
			

sense.stick.direction_up = pushed_up
sense.stick.direction_down = pushed_down
sense.stick.direction_left = pushed_left
sense.stick.direction_right = pushed_right
sense.stick.direction_middle = refresh
pause()