.. _trouble-shooting:
Trouble shooting
================

Something is not working?

* The command::

    sudo pip install pytz astral feedparser pillow svgwrite freetype-py

  fails to install properly? If so, try to install further dependencies (thanks to SEBatHome)::

    sudo apt-get build-dep python-imaging libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev


* The leds do not light up as expected?

    * It is important to have common ground for LEDs and RPi. Assure, ground is same for all of them (Thanks to euchkatzl).

    * Assure to connect the LED strip in the right direction. Little arrows indicate that along the strip (Thanks to euchkatzl).

    * Assure correct functionality of leds::

      cd ~/rpi_ws281x/python/examples
      vim strandtest.py # Set number of leds, pin, etc.
      sudo python strandtest.py

      The leds should light up now...

    * You're using a Raspberry Pi 2 and the leds do not work?

      In this case, the library to address the leds ( https://github.com/jgarff/rpi_ws281x ) has not yet been updated for the RPi2.

      Consider to use Richards library instead as reported here: https://github.com/bk1285/rpi_wordclock/issues/12

* When starting the wordclock-script, "Pin 17 pressed" is logged all the time?

    To get rid of this message, you first need to finish the wordclock setup by attaching all 3 buttons to it.

    If you aim to run the wordclock without buttons, change the config-file settings as follows::

      [wordclock_interface]
      type = gpio_high

.. note:: The provided information might be completely unsatifying, leaving you here frustrated and annoyed without a working wordclock... :/

 However, if you have any issues during the setup, consider:

 * To update the provided documentation (or this trouble shooting section), as soon as you resolved your problem.

 * To report a software issue here: https://github.com/bk1285/rpi_wordclock/issues

