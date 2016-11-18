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

    * Disable the RPis soundcard (since it might interfere with the PMW-channel, sending data to the LEDs. Thanks to ELViTO12 for reporting)::

        sudo sh -c "echo blacklist snd_bcm2835 >> /etc/modprobe.d/alsa-blacklist.conf";
        sudo reboot;
        
    * In case the LEDs are flickering as shown in this video https://www.youtube.com/watch?v=UHxVS8SkXOU (Thanks to oxivanisher), consider the usage of a level-shifter to connect the GPIO-pin of the raspberry to the LED-strip. Further reading: https://github.com/jgarff/rpi_ws281x/issues/127 https://github.com/bk1285/rpi_wordclock/issues/38
    .. figure:: _images/74HCT125_wiring.png
        :scale: 40%
        :alt: Wiring of the a 74HCT125 level-shifter

* When starting the wordclock-script, "Pin 17 pressed" is logged all the time?

    To get rid of this message, you first need to finish the wordclock setup by attaching all 3 buttons to it.

    If you aim to run the wordclock without buttons, change the config-file settings as follows::

      [wordclock_interface]
      type = gpio_high

.. note:: The provided information might be completely unsatifying, leaving you here frustrated and annoyed without a working wordclock... :/

 However, if you have any issues during the setup, consider:

 * To update the provided documentation (or this trouble shooting section), as soon as you resolved your problem.

 * To report a software issue here: https://github.com/bk1285/rpi_wordclock/issues

