.. _further_reading:
Further reading
===============

.. _concepts:
Concepts and background
+++++++++++++++++++++++

.. _concept_WCA:
* WCA (Word Clock Array): The center matrix, without minute-LEDs and other stuff
.. _concept_WCA_DIMENSION:
* WCA_WIDTH, WCA_HEIGHT: Height and width of the WCA.

  * Part of the wordclock software are png-files, which need to fit to these values.
  * Currently available: 11x10 png-files.
  * Support for wordclocks with other resolution available (untested).

.. _concept_WCD:
* WCD (Word Clock Display): Includes any led attached to the wordclock (such as minutes, possible/future ambilights/etc.)
.. _concept_coordinate:
* Coordinates (or: WCA-coordinates): Can be 1d or 2d, used to adress a LED on the word clock array
.. _concept_index:
* Index (or: strip index): Used to adress a LED depending on the position on the LED-strip


.. _expanding_the_wordclock:
Expanding the functionality of the wordclock
++++++++++++++++++++++++++++++++++++++++++++

Remote control of the wordclock
-------------------------------

The wordclock comes with a REST-API to control the major functionality of the clock.

To access the API documentation, visit::

    http://wordclock-ip/api

Adding a new plugin
-------------------

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

  * Add a section `[plugin_new_stuff]` to the reference config-file (wordclock_config/wordclock_config.reference.cfg) and store there all necessary config-values in a way that they are suitable for all wordclock users by default and out of the box.
    * Even consider disableing your plugin by default..
    * Disabling is mandatory, if additional hardware is required to run the plugin.
  * Add the same section `[plugin_new_stuff]` to your local config-file (wordclock_config/wordclock_config.cfg), holding the (custom) values you want to have setup for your own clock.
    * Your plugin will extract config values from wordclock_config.cfg first. If they are not set their, it will default to wordclock_config.reference.cfg

  * Document everything properly, so that others (and maybe you as well) can later understand it... ;)

  * Commit your changes using git and consider to create a pull-request at https://www.github.com/bk1285/rpi_wordclock

  * Consider, that this repository uses nvie's branching model: http://nvie.com/posts/a-successful-git-branching-model/

