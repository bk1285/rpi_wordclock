.. _general_considerations:
General considerations
======================

.. _building_a_wordclock:
If you want to build a wordclock
++++++++++++++++++++++++++++++++

.. note:: This project is currently still in an experimental state:

  * The documentation contains the main steps to build a wordclock, but might not guide you through all steps in greatest detail
  * Depending on your language-dependent stencil-layout, you might need to adapt the software.
    Feel free to contribute here!
    Currently available:

      * Stancil layout and software:

          * german (including swabian and bavarian: Thanks to Timo and Euchkatzl)
          * english (Thanks to Alexandre)
          * dutch (Thanks to svenjacobi, resolution is 10x9. Therefore, not all plugins are supported!)

      * Stancil layout only (requiring some python-implementations: See wordclock_plugins/time_default):

          * french
          * italian
          * spanish
          * turkish

      * Further languages/stencil layouts can be created using the ''config-file'' and the script ''create_layout.py''

  * A collection of the main hardware components -- except sceleton and stencil -- are available for
      * Germany: http://astore.amazon.de/araspbepibase-21
      * UK: http://astore.amazon.co.uk/araspbepiba0c-21

  * A final note: Throughout this project, you will assemble electronic components, which can possibly harm you or others (or destroy your hardware).
    It's therefore important, that you know, what you are doing: By assembling this clock, you act on your own risk!

* Hardware requirements:

  * A (wooden) sceleton to hold LEDs, stencil, RPi, etc...
  * A stencil providing the letters
    * Find an overview over the different layouts here: https://github.com/bk1285/rpi_wordclock/tree/master/wordclock_layouts
    * You can create them on your own: Special plotters can produce adhesive stencils, which you can glue onto a glas plane.
    * Consider, that you might need to invert the layout to have the adhesive surface on top to attach to the glas plate.
    * Possible options for ordering a stencil are:
      * https://www.ponoko.com/ (thanks to StefanCarton).
      * http://www.mikrocontroller.net/articles/Word_Clock (thanks to euchkatzl)
    * Further reading:
      * http://diskussion.christians-bastel-laden.de/viewforum.php?f=12&sid=b90281d4a392f47503e9b9fc15495b19

  * A frame to enframe the wordclock

    * Possible materials: Wood, alumnium, etc.

  * A LED-strip running at 5V (e.g. WS2812 B Stripe 5m 150 LED)

    * Assure, that the spacing of the LEDs on the strip is equal or greater than the spacing of the letters
      of your stencil. If the spacing is smaller, you will not be able to get your LEDs into the correct position.

  * A Raspberry Pi (e.g. Review B, including SD-card)
  * A wifi-dongle to connect your RPi wireless to your local network
  * A power supply (e.g. 5V 10A 50W LED Power Supply)

    * 5V are required. The current, which needs to be provided at max depends on the number and power consumption of you LEDs.

  * A user-interface to run the wordclock

    * e.g. 3 buttons (each requiring a 1k and a 10k resistor)
    * e.g. a capacitive touch sensor
    * ...

  * Some plugs to connect cables to the Raspberry Pis GPIO-pins
  * A micro-usb cable to connect the Raspberry Pi to the power supply
  * Optional: Hardware for levelshifting as oulined in https://learn.adafruit.com/neopixels-on-raspberry-pi/wiring and http://youtu.be/V9TwvranJnY?t=23m08s
  * Optional: A temperature sensor like an AM2302. To connect the sensor, an additial 10k resistor is required.


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

