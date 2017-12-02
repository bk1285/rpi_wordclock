#!/bin/bash

# Check for root-privileges
if [ "$(whoami)" != "root" ]; then
    echo -e "\n\e[34mThis script must be executed as root.\e[0m"
    echo -e "\e[34mTry to add a \"sudo\" in front of the command.\e[0m\n"
    exit 1
fi

# Install latest updates of the os
echo -e "\e[34mNot installing latest updates of the current operating system:\e[0m"
#sudo apt-get update && sudo apt-get upgrade
echo -e "\e[34m  Done.\e[0m"

# Install 3rd party dependencies
echo -e "\e[34mInstalling 3rd party dependencies:\e[0m"
for pac in python-pip python-scipy scons git swig ttf-freefont
do
   echo -e "\e[34m  Installing dependency $pac...\e[0m"
   sudo apt-get install $pac
   echo -e "\e[34m  Done.\e[0m"
done

# Install 3rd party python dependencies
echo -e "\e[34mInstalling 3rd party python dependencies:\e[0m"
for pac in pytz astral feedparser pillow svgwrite freetype-py netifaces am2303_rpi
do
   echo -e "\e[34m  Installing python dependency $pac...\e[0m"
   sudo pip install $pac
   echo -e "\e[34m  Done.\e[0m"
done

# Install jgarffs LED library
echo -e "\e[34mInstalling jgarffs LED library\e[0m"
cd ~
git clone https://github.com/jgarff/rpi_ws281x.git
cd rpi_ws281x
sudo scons
cd ~/rpi_ws281x/python
sudo python setup.py install

# Install fontdemo to render strings
echo -e "\e[34mInstalling fontdemo to render strings\e[0m"
cd ~
git clone https://gist.github.com/5488053.git

# Install pywapi
echo -e "\e[34mInstalling pywapi\e[0m"
#Further details: https://code.google.com/p/python-weather-api/#Weather.com
cd ~
wget https://launchpad.net/python-weather-api/trunk/0.3.8/+download/pywapi-0.3.8.tar.gz
tar -zxf pywapi-0.3.8.tar.gz
rm pywapi-0.3.8.tar.gz
cd pywapi-0.3.8
sudo python setup.py build
sudo python setup.py install

# Install the actual wordclock software
echo -e "\e[34mInstalling the actual wordclock software...\e[0m"
    cd ~
    git clone https://github.com/bk1285/rpi_wordclock.git
    ln -s ~/5488053/fontdemo.py ~/rpi_wordclock/fontdemo.py

echo -e "\e[34mAdding the wordclock software to the startup scripts of the RPi...\e[0m"
sudo crontab -l > tmp_cron
echo "@reboot sudo python /home/pi/rpi_wordclock/wordclock.py" >> tmp_cron
crontab tmp_cron
rm tmp_cron

echo -e "\e[34mTo start the wordclock, system reboot required. Reboot now...?\e[0m"

echo -e "\e[34mTodo: Handle wifi-credentials, etc.\e[0m"

echo -e "\e[34m  Optional usage for temperature sensor\e[0m"
echo -e "\e[34m  To make use of it, install additional dependencies from http://www.airspayce.com/mikem/bcm2835/index.html\e[0m"

# Check for correct locale
echo -e "\e[34mSetup locales:\e[0m"
echo "  Current locale is $LANG"
echo "  Should be utf-8. E.g. en_US.UTF-8"
#If not, check this website, to adjust it: http://perlgeek.de/en/article/set-up-a-clean-utf8-environment

