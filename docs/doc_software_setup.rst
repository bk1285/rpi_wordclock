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

.. _3rd_party_deps_packages:

3rd party dependencies (packages)
---------------------------------

To install 3rd party dependencies (packages) enter in a terminal/commandline::

    sudo apt-get install git python3-full python3-virtualenv swig fonts-freefont-ttf libopenjp2-7

.. _download_software:

Download software
-----------------

Clone the wordclock software to the directory ~/rpi_wordclock (to run the actual wordclock)::

    cd ~
    git clone https://github.com/bk1285/rpi_wordclock.git


.. _python_venv:

Create Python virtual environment
---------------------------------

Create a python3 virtual environment in the ~/rpi_wordclock/venv folder where all python requirements will be installed in::

    python3 -m venv ~/rpi_wordclock/venv

.. _temperature_sensor:

(Optional) dependencies to readout temperature sensor
-----------------------------------------------------

To read out an temperature sensor (AM2302), which can additionally be connected to the raspberry via GPIOs, install the according dependencies:

These dependencies are http://www.airspayce.com/mikem/bcm2835/index.html

and::

    ~/rpi_wordclock/venv/bin/pip install am2302_rpi

.. _brightness_sensor:

(Optional) brightness sensor
----------------------------

For using brightness sensor (tsl2561) i2c must be activated via raspi-config::

    sudo raspi-config

use the arrow keys to select 'Interfacing Options' and 'I2C' to tell the RasPi to enable the I2C interface. Then select 'Finish' and reboot the RasPi

Install adafruit-circuitpython-tsl2561 lib::

    ~/rpi_wordclock/venv/bin/pip install adafruit-circuitpython-tsl2561


Set use_brightness_sensor config value to true and its address::

    # Set the brightness of the display (between 1 and 255)
    brightness = 200
    use_brightness_sensor = True
    sensor_address = 0x39

.. _3rd_party_deps_python:

3rd party dependencies (python packages)
----------------------------------------

To install 3rd party python dependencies (packages) run::

    ~/rpi_wordclock/venv/bin/pip install -r requirements.txt

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

    sudo ~/rpi_wordclock/venv/bin/python3 wordclock.py

In case the whole thing is not working as expected: Maybe the section :ref:`trouble-shooting` might help...

.. note:: Please be aware, that running the wordclock this way is mainly to ensure it is working. If you close the SSH
  connection or stop the command, the wordclock will no longer update.


.. _run_software_on_startup:

Make software run on every startup
----------------------------------

Link and enable the systemd unit by running the following commands::

    sudo ln -s /home/pi/rpi_wordclock/wordclock_config/wordclock.service /etc/systemd/system
    sudo systemctl daemon-reload
    sudo systemctl enable --now wordclock.service

For more information on systemd related operations, please see :ref:`systemd`.

Migration from the former crontab startup solution
--------------------------------------------------

If you have a working wordclock which was configured with the former `crontab` solution and like to migrate to systemd,
just run::

    sudo crontab -e

And remove the `@reboot python3 /home/pi/rpi_wordclock/wordclock.py` line. Now you can follow the steps above. Remember to do everything concerning the Python virtual environment.

.. note:: If the wordclock software is currently running, you should either omit the `--now` option from the command above
or reboot after the `daemon-reload` command. Else the wordclock software will run twice which will result in strange
behaviour. Just reboot if you run into this.

Access the wordclock via webinterface
-------------------------------------

Visit the wordclocks webinterface by entering the wordclocks IP to your browers address bar.
