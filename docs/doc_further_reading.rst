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

