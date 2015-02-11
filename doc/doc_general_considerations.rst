.. _general_considerations:
General considerations
======================

.. _building_a_wordclock:
If you want to build a wordclock...
+++++++++++++++++++++++++++++++++++

.. note:: This project is currently still in an experimental state:

  * The documentation contains the main steps of building a wordclock, but might not guide you through all steps in greatest detail
  * Depending on your language-dependent stancil-layout, you might need to adapt the software.
    Feel free to contribute here!
    Currently available:

      * Stancil layout and software:

          * german (including swabian: Thanks to Timo)

      * Stancil layout only (requiring some python-implementations: See wordclock_plugins/time_default):

          * english
          * french
          * italian
          * spanish
          * turkish

      * Further languages/stancil layouts can be created using the ''config-file'' and the script ''create_layout.py''

* Hardware requirements:

  * A (wooden) sceleton to hold LEDs, stancil, RPi, etc...
  * A stancil providing the letters

    * You can order them online or create your own layout: Special plotters can produce adhesive stancils, which you can glue onto a glas plane .
    * Consider, that you might need to invert the layout to have the adhesive surface on top to attach to the glas plate.

  * A frame to enframe the wordclock

    * Possible materials: Wood, alumnium, etc.

  * A LED-strip running at 5V (e.g. WS2812 B Stripe 5m 150 LED)

    * Assure, that the spacing of the LEDs on the strip is equal or greater than the spacing of the letters
      of your stancil. If the spacing is smaller, you will not be able to get your LEDs into the correct position.

  * A Raspberry Pi (e.g. Review B, including SD-card)
  * A wifi-dongle to connect your RPi wireless to your local network
  * A power supply (e.g. 5V 10A 50W LED Power Supply)

    * 5V are required. The current, which needs to be provided at max depends on the number and power consumption of you LEDs.

  * A user-interface to run the wordclock

    * e.g. 3 buttons (requiring resistors, ... as outlined here in the background-section: https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/robot/buttons_and_switches/)
    * e.g. a capacitive touch sensor
    * ...

  * Some plugs to connect cables to the Raspberry Pis GPIO-pins
  * A micro-usb cable to connect the Raspberry Pi to the power supply
  * Optionally: Consider hardware for levelshifting as oulined in https://learn.adafruit.com/neopixels-on-raspberry-pi/wiring and http://youtu.be/V9TwvranJnY?t=23m08s


* You need to setup the software on your own

  * Some first documentation available here
  * This might require some python programming (to adopt the software to your needs)

* You should be ready to...

  * Setup the hardware (glueing, soldering, etc.)
  * Setup a Raspberry Pi (raspbian)

    * Connect to the RPi via ssh
    * Install external dependencies of the wordclock project
    * Do some python programming (to adopt the software to your needs)

  * Contribute to this project

    * by sharing your implementations/improvements/enhancements/... ;)

.. _expanding_the_wordclock:
Expanding the functionality of the wordclock
++++++++++++++++++++++++++++++++++++++++++++

You might be interested in expanding the wordclocks functionality by adding a new
plugin to the wordclock

To do so, you need to...

  * Think about the name of this plugin: E.g. `new_stuff`
  * Add a new folder `new_stuff` to the folder wordclock_plugins

    * Create a plugin.py-file with a class `plugin`, which has at
      least the following functions implemented:

      * __init__(self, config): You can use the config-object to pass data
        from the config-file for initialization purposes
      * run(): Run the actual plugin

  * For the actual implementation, you can access the provided methods of the class `wordclock_display`
    * If necessary you might extend it... ;)

  * Add an icon (with resolution 11x10 pixel) for the new plugin to the
    directory wordclock_plugins/`new_stuff`/icons/11x10/`logo.png`

  * Add optional values to the config-file under the section `[plugin_new_stuff]`

  * Document everything properly, so that others (and maybe you as well) can later understand it... ;)

