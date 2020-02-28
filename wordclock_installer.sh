#!/bin/bash

# Check for root-privileges
if [ "$(whoami)" != "root" ]; then
    echo -e "\n\e[34mThis script must be executed as root.\e[0m"
    echo -e "\e[34mAdd \"sudo\" in front of the command.\e[0m\n"
    exit 1
fi

# Install 3rd party dependencies
echo -e "\e[34mInstalling 3rd party dependencies:\e[0m"
for pac in python-pip python-scipy scons git swig ttf-freefont flask flask_restplus
do
   echo -e "\e[34m  Installing dependency $pac...\e[0m"
   sudo apt-get install -y $pac
   echo -e "\e[34m  Done.\e[0m"
done

# Install 3rd party python dependencies
echo -e "\e[34mInstalling 3rd party python dependencies:\e[0m"
for pac in pytz astral feedparser pillow svgwrite freetype-py netifaces am2303_rpi monotonic
do
   echo -e "\e[34m  Installing python dependency $pac...\e[0m"
   sudo pip install $pac
   echo -e "\e[34m  Done.\e[0m"
done

# Install jgarffs LED library
echo -e "\e[34mInstalling jgarffs LED library\e[0m"
cd /home/pi
git clone https://github.com/jgarff/rpi_ws281x.git
cd rpi_ws281x
sudo scons
cd /home/pi/rpi_ws281x/python
sudo python setup.py install

# Install pywapi
echo -e "\e[34mInstalling pywapi\e[0m"
#Further details: https://code.google.com/p/python-weather-api/#Weather.com
cd /home/pi
wget https://launchpad.net/python-weather-api/trunk/0.3.8/+download/pywapi-0.3.8.tar.gz
tar -zxf pywapi-0.3.8.tar.gz
rm pywapi-0.3.8.tar.gz
cd pywapi-0.3.8
sudo python setup.py build
sudo python setup.py install

# Install the actual wordclock software
echo -e "\e[34mInstalling the actual wordclock software...\e[0m"
cd /home/pi
git clone https://github.com/bk1285/rpi_wordclock.git
sudo chown -R pi /home/pi/rpi_wordclock

echo -e "\e[34mAdding the wordclock software to the startup scripts of the RPi...\e[0m"
sudo crontab -l > tmp_cron
echo "@reboot sudo python /home/pi/rpi_wordclock/wordclock.py" >> tmp_cron
crontab tmp_cron
rm tmp_cron

echo
echo "################################################################################"
echo -e "\e[34m  If you have an temperature sensor connected to your clock,\e[0m"
echo -e "\e[34m  install additional dependencies from http://www.airspayce.com/mikem/bcm2835/index.html\e[0m"

# Check for correct locale
echo -e "\e[34mSetup locales:\e[0m"
echo "  Note: Current locale is $LANG"
echo "  Should be utf-8. E.g. en_US.UTF-8"
echo "  If this is not the case, adjust it: http://perlgeek.de/en/article/set-up-a-clean-utf8-environment"

echo
echo "################################################################################"
echo
echo -e "\e[34mraspi-config will be invoked now.\e[0m"
echo
echo "  * Set your wifi credentials via (1 Network Options) -> (N2 Wifi)"
echo "  * Set the correct time zone via (4 Localisation Options) -> (I2 Change Timezone)"
echo
read -p ""
sudo raspi-config
echo
echo
echo "################################################################################"
echo
echo -e "\e[34mTo start the wordclock, system reboot required.\e[0m"

