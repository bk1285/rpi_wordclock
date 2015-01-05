General considerations
======================


If you want to build a wordclock...
+++++++++++++++++++++++++++++++++++

.. note:: The state of this project is currently still in experimental mode:

  * Documentation contains the main steps, but might not guide you through all steps in greatest detail
  * Depending on your wordclock/stancil layout, you might need to adapt the LED-mapping.
    Feel free to contribute here!
    Currently available:

    * German stancil layout

* Hardware requirements:

  * A (wooden) sceleton to hold LEDs, stancil, RPi, etc...
  * A stancil providing the letters, ...
  * A frame to enframe the wordclock
  * A LED-strip (e.g. WS2812 B Stripe 5m 150 LED)
  * A Raspberry Pi (e.g. Review B, including SD-card)
  * A wifi-dongle to connect your RPi wireless to your local network
  * A power supply (e.g. 5V 10A 50W LED Power Supply)
  * A user-interface to run the wordclock

    * e.g. 3 buttons (requiring resistors, etc.)
    * e.g. a capacitive touch sensor
    * ...

 * Some plugs to connect cables to the Raspberry Pis GPIO-pins
 * A micro-usb cable to connect the Raspberry Pi to the power supply

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

