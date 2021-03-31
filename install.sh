### To be translated in bash ####
Raspberry UPDATE/UPGRADE

LED
sudo apt-get install gcc make build-essential python-dev git scons swig
sudo nano /etc/modprobe.d/snd-blacklist.conf --EDIT--  blacklist snd_bcm2835
sudo nano /boot/config.txt   --COMMENT #-- dtparam=audio=on
git clone https://github.com/jgarff/rpi_ws281x
cd rpi_ws281x/
sudo scons
cd python
sudo python3 setup.py build 
sudo python3 setup.py install 
sudo pip3 install adafruit-circuitpython-neopixel

GrovePi
sudo curl -kL dexterindustries.com/update_grovepi | bash -s -- --bypass-gui-installation

WEB
sudo apt install apache2 php libapache2-mod-php mariadb-server php-mysql
sudo apt install php-curl php-gd php-intl php-json php-mbstring php-xml php-zip

PYTHON CONNECTOR
# sudo apt-get install ca-certificates
# sudo apt-get instal apt-transport-https
# curl -LsS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | sudo bash
sudo apt install libmariadb3 libmariadb-dev
sudo pip3 install mariadb

DB
CREATE DATABASE happybasil_db;
USE happybasil_db;
