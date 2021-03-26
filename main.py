#!/usr/bin/env python3
#
#	Smart Garden Project V1.0.2
#	*	Reads the data from moisture, light, temperature and humidity sensor 
#		and takes pictures from the Pi camera periodically and logs them
#	* IoT: All the data are saved in a DB and sent to a website: ?
#	*	Sensor Connections on the GrovePi:
#			-> Grove Moisture sensor	- Port A1
#			-> Grove light sensor		- Port A2
#			-> Grove DHT sensors		- Port D2
#	* Pump and LED strip are connected :AUTO / MANUAL mode are availables
#			-> LED strip				- GPIO 18
#	*	Sensor Connections on the GrovePi:
#			-> Relay					- Port D4
# NOTE:
#	*	Make sure that the Pi camera is enabled and works. Directions here: https://www.raspberrypi.org/help/camera-module-setup/
#	
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#

import time
from datetime import datetime
import grovepi
import subprocess
import math
import argparse
from neopixel import *


#analog sensor port number
moisture_sensor			= 1
light_sensor			= 2

#digital sensor
temp_humidity_sensor	= 2
motor					= 4
green_led				= 3

#temp_humidity_sensor type
blue	= 0
white 	= 1

#variables
watered = False

#timings
#test 
#time_for_sensor		= 4		#  4 seconds
#time_for_picture		= 12	# 12 seconds

#final
time_for_sensor			= 1*60*60	#1hr
time_for_picture		= 8*60*60	#8hr
time_to_sleep			= 1

#logfile
log_file="plant_monitor_log.csv"

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

# To be UPDATED !!!
def auto_mode():
    #If the time is in between an interval of +- 15 mins, while the moisture level < thresh keep motor running, else turn off motor
	thresh = 30
	global watered
	print ("Watered?", watered)
	my_time = datetime.now().strftime("%H:%M") #TO BE UPDATED
	print ("current time", my_time)
	#FLAG IS REQUIRED
	if ((my_time > "10:00") and (my_time < "20:00")):
		led_strip(strip, 1)
	else:
		led_strip(strip, 0)
	if (((my_time > "19:45") and (my_time < "20:40")) or ((my_time > "3:45") and (my_time < "4:15"))):
		if not watered:
			while True:
				moisture = grovepi.analogRead(moisture_sensor)
				moisture = 100 - (100*moisture/1023)
				if (moisture > thresh):
					grovepi.digitalWrite(motor, 0)
					watered = True
					break
				else:
					grovepi.digitalWrite(motor,1)
    	else:
			watered = False
			grovepi.digitalWrite(motor,0)
			
# Main program logic follows:
if __name__ == '__main__':
	print ('Press Ctrl-C to quit.')
	
	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
	strip.begin()	
	
	#Save the initial time, we will use this to find out when it is time to take a picture or save a reading
	last_read_sensor=last_pic_time= int(time.time())
	try:
		while True:
			curr_time_sec=int(time.time())
			grovepi.digitalWrite(green_led, 1)
			#Variables
			light_state = 0
			motor_state = 0
			#update 	= 0
			pi_state 	= 0
			#print light_state
			#print motor_state
			#print pi_state
			
			#Data
			if (pi_state == unicode("0")):
				led_strip(strip, 0)
				grovepi.digitalWrite(green_led, 0)
				grovepi.digitalWrite(motor,0)
				break
				#To be UPDATED !!!
			#LED
			if (light_state == unicode("1")):
				#switch on the LED strip
				print ("LED strip switched on\n")
				led_strip(strip, 1)
			elif (light_state == unicode("0")):
				#switch off the LED strip
				print("LED strip switched off\n")
				led_strip(strip, 0)
			#Motor	
			if (motor_state == unicode("1")):
				#turn on motor
				print ("Motor turned on\n")
				grovepi.digitalWrite(motor,1)
			elif (motor_state == unicode("2")):
				print("Pump is now in auto mode !\n")
				auto_mode()
			else:
				#turn off motor
				print("Motor turned off\n")
				grovepi.digitalWrite(motor,0)
				
			# If it is time to take the sensor reading
			if curr_time_sec-last_read_sensor>time_for_sensor:
				#Sensor reading and variables updating
				[moisture,light,temp,humidity]=read_sensor()
				light = 100*light/1023
				moisture = 100 - (100*moisture/1023)
				print("Updating data...\n")
				#Uptade the database
				# TO DO
				# If any reading is a bad reading, skip the loop and try again
				if moisture==-1:
					print("Bad reading")
					time.sleep(1)
					continue
					
				curr_time = time.strftime("%Y-%m-%d:%H-%M-%S")
				print(("Time:%s\nMoisture: %d\nLight: %d\nTemp: %.2f\nHumidity:%.2f %%\n" %(curr_time,moisture,light,temp,humidity)))
			
				# Save the sensors value in a CSV file
				f=open(log_file,'a')
				f.write("%s,%d,%d,%.2f,%.2f;\n" %(curr_time,moisture,light,temp,humidity))
				f.close()
				print("Logfile updated at %s \n" % curr_time)
				
				#Update the last read time
				last_read_sensor=curr_time_sec		

			# If it is time to take the picture
			if curr_time_sec-last_pic_time>time_for_picture:
				take_picture()
				last_pic_time=curr_time_sec

			#Slow down the loop
			time.sleep(time_to_sleep)
			
	except KeyboardInterrupt:
		print("\nSystem stopped\n")
		grovepi.digitalWrite(green_led, 0)
		grovepi.digitalWrite(motor,0)
		led_strip(strip, 0)
		
