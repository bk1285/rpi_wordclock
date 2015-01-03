
Software installation
=====================

.. note:: `~` indicates the path to the users home-directory (default on a RPi: /home/pi)

3rd party dependencies (packages)
+++++++++++++++++++++++++++++++++

To install 3rd party dependencies (packages) enter in a terminal/commandline::

    sudo apt-get install python-pip scons git


3rd party dependencies (git-repositories)
+++++++++++++++++++++++++++++++++++++++++

Install 3rd-party dependencies (compiled on your own).
.. todo:: Improve installation location.

Install rpi_ws281x to your home-directory (to access leds)::

    cd ~
    git clone https://github.com/jgarff/rpi_ws281x.git
    cd rpi_ws281x
    sudo scons

Install fontdemo to your home-directory (to render strings)::

    cd ~
    git clone https://gist.github.com/5488053.git

This installs fontdemo.py to ~/5488053.

Link the file fontdemo.py to ~/rpi_wordclock using a softlink::

    ln -s ~/5488053/fontdemo.py ~/rpi_wordclock/fontdemo.py

Install pywapi as indicated on https://code.google.com/p/python-weather-api/#Weather.com

Install astral (to get moon/sun information)::

    sudo pip install pytz astral

The wordclock software
++++++++++++++++++++++

Install software
----------------

Install the wordclock software to the directory ~/rpi_wordclock (to run the actual wordclock)::

    Clone from github
    Todo: Needs proper documentation

Adopt software
--------------

To adjust the wordclock to your own settings, create/edit the file ~/rpi_wordclock/wordclock_config/wordclock_config.cfg

To start over, you might just copy the file ~/rpi_wordclock/wordclock_config/wordclock_config.example.cfg and adopt this file.

Each class of the wordclock project has its own section in the config-file (create it, if needed, but not existant)

Make software run on every startup
++++++++++++++++++++++++++++++++++

Add the python-script to crontab by calling the command::

    sudo crontab -e

Add here::

    @reboot sudo python /home/pi/rpi_wordclock/wordclock.py


