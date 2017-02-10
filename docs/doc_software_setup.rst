.. _software_installation:

Software setup
==============

Set locales
+++++++++++

Since the config-file contains layouts for multiple languages, assure to have a utf-8 compatible locale::

    echo $LANG

should return something, containing utf-8 at the end.
E.g.::

    en_US.UTF-8

If not, check this website, to adjust it: http://perlgeek.de/en/article/set-up-a-clean-utf8-environment


.. _3rd_party_deps_packages:

3rd party dependencies (packages)
+++++++++++++++++++++++++++++++++

To install 3rd party dependencies (packages) enter in a terminal/commandline::

    sudo apt-get install python-pip python-scipy scons git swig ttf-freefont


.. _3rd_party_deps_python:

3rd party dependencies (python packages)
+++++++++++++++++++++++++++++++++++++++++

Required python dependencies:

  * astral (to get moon/sun information)
  * feedparser (to get access to latest feeds)
  * scipy
  * netifaces (to get the ip of the pi)
  * pil
  * svgwrite (to plot stencil/wiring layouts)

To install use::

    sudo pip install pytz astral feedparser pillow svgwrite freetype-py netifaces monotonic


.. _temperature_sensor:

(Optional) dependencies to readout temperature sensor
+++++++++++++++++++++++++++++++++++++++++++++++++++++

To read out an temperature sensor (AM2302), which can additionally be connected to the raspberry via GPIOs, install the according dependencies:

These dependencies are http://www.airspayce.com/mikem/bcm2835/index.html

and::

    sudo pip install am2302_rpi


.. _3rd_party_deps_git:

3rd party dependencies (git repositories)
+++++++++++++++++++++++++++++++++++++++++

Install 3rd-party dependencies (compiled on your own).

Install rpi_ws281x to your home-directory (to access leds)::

    cd ~
    git clone https://github.com/jgarff/rpi_ws281x.git
    cd rpi_ws281x
    sudo scons
    cd ~/rpi_ws281x/python
    sudo python setup.py install

.. note::
    Since this library is continiously updated: A version, which is tested to work with the wordclock is commit 2f9e03c45:
    https://github.com/jgarff/rpi_ws281x/tree/2f9e03c45ba0964029204db565ad9d6233b3a1a6

Install fontdemo to your home-directory (to render strings)::

    cd ~
    git clone https://gist.github.com/5488053.git

This installs fontdemo.py to ~/5488053.

Install pywapi::

    cd ~
    wget https://launchpad.net/python-weather-api/trunk/0.3.8/+download/pywapi-0.3.8.tar.gz
    tar -zxf pywapi-0.3.8.tar.gz
    rm pywapi-0.3.8.tar.gz
    cd pywapi-0.3.8
    sudo python setup.py build
    sudo python setup.py install

Further details: https://code.google.com/p/python-weather-api/#Weather.com

.. _wordclock_software:

The wordclock software
++++++++++++++++++++++

.. _download_software:

Download software
-----------------

Clone the wordclock software to the directory ~/rpi_wordclock (to run the actual wordclock)::

    cd ~
    git clone https://github.com/bk1285/rpi_wordclock.git

Link the previously installed file fontdemo.py to ~/rpi_wordclock using a softlink::

    ln -s ~/5488053/fontdemo.py ~/rpi_wordclock/fontdemo.py


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
    sudo python wordclock.py

In case, the whole thing is not working as expected: Maybe the section :ref:`trouble-shooting` might help...


.. _run_software_on_startup:

Make software run on every startup
----------------------------------

Add the python-script to crontab by calling the command::

    sudo crontab -e

Add here::

    @reboot sudo python /home/pi/rpi_wordclock/wordclock.py

