.. _software_installation:

Software setup
==============


Setup your raspberry pi 
+++++++++++

Setup your raspberry pi (e.g. using Raspberry Pi Imager) by downloading and installing latest Raspian on the SD card.

During the installation process, configure the location according to your needs (incl. time zone, etc.) 

Set locales
+++++++++++

Since the config-file contains layouts for multiple languages, assure to have a utf-8 compatible locale after setting up your raspberry::

    echo $LANG

should return something, containing utf-8 at the end.
E.g.::

    en_US.UTF-8

If not, check this website, to adjust it: http://perlgeek.de/en/article/set-up-a-clean-utf8-environment


.. _wordclock_software:

The wordclock software
++++++++++++++++++++++

.. _download_software:

Download software
-----------------

Clone the wordclock software to the directory ~/rpi_wordclock (to run the actual wordclock)::

    cd ~
    git clone https://github.com/bk1285/rpi_wordclock.git


.. _3rd_party_deps_packages:

3rd party dependencies (packages)
---------------------------------

To install 3rd party dependencies (packages) enter in a terminal/commandline::

    sudo apt-get install python3-pip python3-scipy swig fonts-freefont-ttf libopenjp2-7

.. _temperature_sensor:

(Optional) dependencies to readout temperature sensor
-----------------------------------------------------

To read out an temperature sensor (AM2302), which can additionally be connected to the raspberry via GPIOs, install the according dependencies:

These dependencies are http://www.airspayce.com/mikem/bcm2835/index.html

and::

    sudo pip install am2302_rpi

.. _brightness_sensor:

(Optional) brightness sensor
----------------------------

For using brightness sensor (tsl2561) i2c must be activated via raspi-config::

    sudo raspi-config

use the arrow keys to select 'Interfacing Options' and 'I2C' to tell the RasPi to enable the I2C interface. Then select 'Finish' and reboot the RasPi

Install adafruit-circuitpython-tsl2561 lib::

    sudo pip3 install adafruit-circuitpython-tsl2561


Set use_brightness_sensor config value to true and its address::

    # Set the brightness of the display (between 1 and 255)
    brightness = 200
    use_brightness_sensor = True
    sensor_address = 0x39

.. _3rd_party_deps_python:

3rd party dependencies (python packages)
----------------------------------------

To install 3rd party python dependencies (packages) run::

    cd ~/rpi_wordclock
    sudo pip3 install -r requirements.txt


.. _adopt_software:

Adopt software
--------------

To adjust the wordclock to your own settings, create and edit the file ~/rpi_wordclock/wordclock_config/wordclock_config.cfg

To start over, you might just copy the file ~/rpi_wordclock/wordclock_config/wordclock_config.example.cfg and adopt this file.

Note: Each plugin of the wordclock project has its own section in the config-file (create it, if needed, but not existant)

.. note:: If your wordclock has a stencil layout or display resolution, which is not supported yet, you might need to adopt the
  software by providing your own `wiring`-class (to the file wordclock_tools/wiring.py)


.. _run_software:

Run software
------------

To run the wordclock software (with adapted wiring and config-file) do::

    cd ~/rpi_wordclock
    sudo python3 wordclock.py

In case, the whole thing is not working as expected: Maybe the section :ref:`trouble-shooting` might help...


.. _run_software_on_startup:

Make software run on every startup
----------------------------------

Add the python-script to crontab by calling the command::

    sudo crontab -e

Add here::

    @reboot sudo python3 /home/pi/rpi_wordclock/wordclock.py

Access the wordclock via webinterface
-------------------------------------

Visit the wordclocks webinterface by entering the wordclocks IP to your browers address bar.

