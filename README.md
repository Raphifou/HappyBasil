# HappyBasil
A plant monitoring system based on RPi, Python using a web interface

Prerequisites:
- RaspberryPi
- GrovePi Sensors :
- A small pump
- A WS2812 LED stripe

/!\ Disclaimer/!\
I have done some "code re-use" from DexterIndustries plant_monitoring example and from the openclassroom.com HTML/CSS tutorial. Thank you !
Feel free to visit their amazing work:
- https://github.com/DexterInd/GrovePi/
- https://openclassrooms.com/fr/courses/1603881-apprenez-a-creer-votre-site-web-avec-html5-et-css3/

And this tutorial from Instructable was a source of inspiration as well: https://www.instructables.com/Raspberry-Pi-Powered-IOT-Garden/

How to install the HapPy Basil smart garden:
1) Install Raspbian
2) Update the RaspberryPi: sudo apt-get update | sudo apt-get upgrade
3) Install the LAMP server package: sudo apt install apache2 php libapache2-mod-php mariadb-server php-mysql
4) Set up an apache2 web server
5) Set up the MariaDB database
6) PHP script and web interface UNDER DEV.


/!\ This project works in local ! I am a beginner regarding web server development and network security. So, if you want to extand you HapPy Basil in the world wide web make sure to securize you web server /!\
