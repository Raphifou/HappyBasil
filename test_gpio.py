#!/usr/bin/env python3
#
# Use this script to test your hardware
# Requirements: GrovePi sensors, PiCamera, LED strip
#
#CONNECTIONS:
#	*	Sensor Connections on the GrovePi:
#			-> Grove Moisture sensor	- Port A1
#			-> Grove light sensor		- Port A2
#			-> Grove DHT sensors		- Port D2
#			-> Relay			- Port D4
#	*	GPIO connections:
#			-> LED strip			- GPIO 18
# NOTE:
#	*	Make sure that the Pi camera is enabled and works. Directions here: https://www.raspberrypi.org/help/camera-module-setup/
# 	*	The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi

import time
import datetime
import subprocess
import math
import argparse

import grovepi
from rpi_ws281x  import *

#analog sensor port number
moisture_sensor			= 1
light_sensor			= 2

#digital sensor
temp_humidity_sensor	= 2
motor					= 4
green_led				= 3

#temp_humidity_sensor type
blue			= 0
white 			= 1

#loop
time_to_sleep	= 1

# LED strip configuration:
LED_COUNT      = 60      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN       = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Define functions which animate LEDs in various ways.
def led_strip(strip, LED):
	if LED == 1:
		#print("LED ON")
		for i in range(strip.numPixels()):
			if i%2 == 0:
				strip.setPixelColor(i, Color(0, 0, 255))
			else:
				strip.setPixelColor(i, Color(0, 255, 0))
			strip.show()
	elif LED == 0:
		#print("LED OFF")
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, Color(0, 0, 0))
			strip.show()
			
#Read the data from the sensors
def read_sensor():
	try:
		print("Reading sensors...\n")
		moisture=grovepi.analogRead(moisture_sensor)
		light=grovepi.analogRead(light_sensor)
		[temp,humidity] = grovepi.dht(temp_humidity_sensor,blue)
		#Return -1 in case of bad temp/humidity sensor reading
		if math.isnan(temp) or math.isnan(humidity):		#temp/humidity sensor sometimes gives nan
			return [-1,-1,-1,-1]
		return [moisture,light,temp,humidity]
	#Return -1 in case of sensor error
	except IOError as TypeError:
			return [-1,-1,-1,-1]

#Take a picture with the current time using the Raspberry Pi camera. Save it in the same folder
def take_picture():
	try:
		cmd="raspistill -rot 180 -t 1 -o plant_monitor_"+str(time.strftime("%Y_%m_%d__%H_%M_%S"))+".jpg"
		process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
		output = process.communicate()[0]
		print("Picture taken\n------------>\n")
	except:
		print("Camera problem,please check the camera connections and settings")		

if __name__ == '__main__':
	print 
	print ('Press Ctrl-C to quit.')
	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
	# Intialize the library (must be called once before other functions).
	strip.begin()	
	
	#Save the initial time, we will use this to find out when it is time to take a picture or save a reading
	last_read_sensor=last_pic_time= int(time.time())
	try:
		while True:
			grovepi.digitalWrite(green_led, 1)
			led_strip(strip, 1)
			print ("LED strip switched on\n")
			grovepi.digitalWrite(motor,1)
			print ("Pump turned on")
			take_picture()
			print ("Picture taken\n")
			[moisture,light,temp,humidity]=read_sensor()
			print("***SENSORS***\nMoisture: %d\nLight: %d\nTemp: %.2f\nHumidity:%.2f %%\n" %(moisture,light,temp,humidity))
			
	except KeyboardInterrupt:
		print("\nSystem stopped\n")
		grovepi.digitalWrite(green_led, 0)
		grovepi.digitalWrite(motor,0)
		led_strip(strip, 0)
