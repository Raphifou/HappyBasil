#!/usr/bin/env python3
#
#				**********HapPy Basil V0.1**********
#
# 	https://github.com/raphifou/happybasil
#
#	*	The script reads periodically the data from moisture, light, temperature and humidity sensor, 
#		takes pictures from the Pi camera and logs them into a CSV file.
#		All the data are saved in a database(MariaDB) and sent to a web interface.
#	* Sensor connections on the GrovePi:
#			-> Grove Moisture sensor	- Port A1
#			-> Grove light sensor		- Port A2
#			-> Grove DHT sensors		- Port D2
#			-> Relay					- Port D4
#	* GPIO connections :
#			-> LED strip				- GPIO 18
#			
# NOTE:
#	* Make sure that your database is created and connected
#	* Make sure that the Pi camera is enabled and works. Directions here: https://www.raspberrypi.org/help/camera-module-setup/
# 	* The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
#
import os
import time
import math
import sys
import subprocess
import argparse

import mariadb
import grovepi
from rpi_ws281x import *
from getpass import getpass

#analog sensor port number
moisture_sensor			= 1
light_sensor			= 2

#digital sensor
temp_humidity_sensor	= 2
motor					= 4
green_led				= 3

#temp_humidity_sensor type
blue					= 0
white 					= 1

#variables
watered 		= 0
light_state		= 0
motor_state		= 0
mode_state		= 0
pi_state		= 1
light 			= 0
temp  			= 0
humidity 		= 0
moisture 		= 0

#timings
#for debug
#time_for_sensor		= 4		#  4 seconds
#time_for_picture	= 12	# 12 seconds
#for script
time_for_sensor		= 1*60*60	#1hr
time_for_picture	= 8*60*60	#8hr
time_to_sleep		= 1

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
				strip.setPixelColor(i, Color(255, 0, 0))
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
		return [light,temp,humidity,moisture]
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
		print("Camera issue,please check the camera connections and settings")
		
###### TO DO ######
def auto_mode():
    #If the time is in between an interval of +- 15 mins, while the moisture level < thresh keep motor running, else turn off motor
	thresh = 30.00
	global watered
	print ("Watered?", watered)
	my_time = time.strftime("%H:%M")
	print ("current time", my_time)
	#FLAG IS REQUIRED
	if ((my_time > "8:00") and (my_time < "20:00")):
		#led_strip(strip, 1)
		cur.execute("UPDATE data SET value=%s WHERE variable=%s",("1", "light_state"))
	else:
		#led_strip(strip, 0)
		cur.execute("UPDATE data SET value=%s WHERE variable=%s",("0", "light_state"))
	if (((my_time > "19:45") and (my_time < "20:40")) or ((my_time > "3:45") and (my_time < "4:15"))):
		if not watered:
			while True:
				moisture = grovepi.analogRead(moisture_sensor)
				moisture = 100 ( 100*moisture/1023) #Dryness
				if (moisture > thresh):
					#grovepi.digitalWrite(motor, 0)
					cur.execute("UPDATE data SET value=%s WHERE variable=%s",("0", "motor_state"))
					watered = True
					cur.execute("UPDATE data SET value=%s WHERE variable=%s",("1", "watered"))
					break
				else:
					#grovepi.digitalWrite(motor,1)
					cur.execute("UPDATE data SET value=%s WHERE variable=%s",("1", "motor_state"))
		else:
			watered = False
			#grovepi.digitalWrite(motor,0)
			cur.execute("UPDATE data SET value=%s WHERE variable=%s",("0", "motor_state"))
			
# Main program
if __name__ == '__main__':
	print ("***************************")
	print ("**** HapPy Basil V.0.1 ****")
	print ("***************************")
	print ("Press Ctrl-C to quit.\n")
	# Connect to MariaDB Platform
	print ("Connecting to the database....................")
	try:
	       conn = mariadb.connect(
				user=input("Enter your username: "),
				password=getpass("Enter your password: "),
		        host="localhost",
		        port=3306,
		        database="happybasil_db",
		        autocommit=True
	       )
	except mariadb.Error as e:
	       print (f"Error connecting to MariaDB Platform: {e}")
	       sys.exit(1)
	print ("Done")
	# Get Cursor
	conn.autocommit = True
	cur = conn.cursor()
	#Initialize the database
	print ("Setting up the database....................", end = '')
	cur.execute("UPDATE data SET value = '0'")
	cur.execute("UPDATE data SET value = %s WHERE variable = %s ", ("1","pi_state"))
	#conn.commit() 
	print ("Done")
	       
	# Create NeoPixel object with appropriate configuration.
	print ("Setting up the LEDs....................", end = '')
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
	# Intialize the library (must be called once before other functions).
	strip.begin()	
	print ("Done")
	       
	#Save the initial time, we will use this to find out when it is time to take a picture or save a reading
	last_read_sensor=last_pic_time= int(time.time())
	print ("****HapPy Basil is now ready !****\n")
	       
	#Main loop
	try:
		while True:
			curr_time_sec=int(time.time()) # Current time
			grovepi.digitalWrite(green_led, 1) #I am alive ;)
			
			#Read the database and update the variables
			cur.execute("SELECT value FROM data")
			data = cur.fetchall()
			data = [i[0] for i in data]
			print (data)
			light_state = data[0]
			motor_state = data[1]
			mode_state 	= data[2]
			pi_state	= data[3]
			
			#Test the state variables
			# LED
			if (light_state == "1"):
				#Switch on the LED strip
				print ("LED strip switched on")
				led_strip(strip, 1)
			elif (light_state == "0"):
				#Switch off the LED strip
				print("LED strip switched off\n")
				led_strip(strip, 0)
				
			# Pump	
			if (motor_state == "1"):
				#turn on motor
				print ("Pump turned on\n")
				grovepi.digitalWrite(motor,1)
			elif (motor_state == 0):
				#turn off motor
				print("Pump turned off\n")
				grovepi.digitalWrite(motor,0)

			# Mode
			if (mode_state == "1"):
				auto_mode()
				print ("HapPy Basil is now in auto mode !\n")
			elif (mode_state == "0"):
				print("HapPy Basil is now in manual mode !\n")

			#System
			if (pi_state == "0"):
				led_strip(strip, 0)
				grovepi.digitalWrite(green_led, 0)
				grovepi.digitalWrite(motor,0)
				print("\nHapPy Basil turned off !")
				break

			# Sensors
			# If it is time to take the sensor reading
			if curr_time_sec-last_read_sensor>time_for_sensor:
				#Sensor reading and variables updating
				[light,temp,humidity,moisture]=read_sensor()
				light = 100*light/1023
				moisture = 100*moisture/1023 #To be checked
				print("Updating data...\n")
				# If any reading is a bad reading, skip the loop and try again
				if moisture == -1:
					print("Bad reading")
					time.sleep(1)
					continue
				# What time is it ?
				curr_time = time.strftime("%d/%m/%Y-%H:%M:%S")
				print(("Time:%s\nMoisture: %d %%\nLight: %d\nTemp: %.2f\nHumidity:%.2f %%\n" %(curr_time,moisture,light,temp,humidity)))
				# Update the database
				light = str(light)
				light = light[:2]
				moisture = str(moisture)
				moisture = moisture[:2]
				mydate = time.strftime("%d/%m/%Y")
				mytime = time.strftime("%H:%M:%S")
				cur.execute("UPDATE data SET value=%s WHERE variable=%s",(light, "light"))
				cur.execute("UPDATE data SET value=%s WHERE variable=%s",(temp, "temp"))
				cur.execute("UPDATE data SET value=%s WHERE variable=%s",(humidity, "humidity"))
				cur.execute("UPDATE data SET value=%s WHERE variable=%s",(moisture, "moisture"))
				cur.execute("UPDATE data SET value=%s WHERE variable=%s",(mydate, "date"))
				cur.execute("UPDATE data SET value=%s WHERE variable=%s",(mytime, "time"))
				print ("Database updated !")
				# Save the sensors value in a CSV file
				f=open(log_file,'a')
				f.write("%s,%s,%d,%d,%s;\n" %(curr_time,light,temp,humidity,moisture))
				f.close()
				print("Logfile updated at %s \n" % curr_time)
				#Update the last read time
				last_read_sensor=curr_time_sec		
			
			# Picture
			# If it is time to take the picture
			if curr_time_sec-last_pic_time > time_for_picture:
				take_picture()
				last_pic_time = curr_time_sec

			#Slow down the loop
			time.sleep(time_to_sleep)
			
	except KeyboardInterrupt:
		# Turn off the the LED stripe and the pump
		grovepi.digitalWrite(green_led, 0)
		grovepi.digitalWrite(motor,0)
		led_strip(strip, 0)
		# Close the database connection
		conn.close()
		print("\nHapPy Basil turned off !\n")
				     
		
