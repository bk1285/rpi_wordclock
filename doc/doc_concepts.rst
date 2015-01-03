Concepts
========

* WCA (Word Clock Array): The center matrix, without minute-LEDs and other stuff
* WCA_WIDTH, WCA_HEIGHT: Height and width of the wordclock array. Part of the wordclock software are png-files, which need to fit to these values.
  Currently supported: 11x10 arrays.
* WCD (Word Clock Display): Includes any led attached to the wordclock (such as minutes, possible/future ambilights/etc.)
* Coordinates: Can be 1d or 2d, used to adress a LED on the word clock array
* Index: Is always 1d. Used to adress a LED depending on the position on the LED-strip

... To be expanded to explain further important concepts within this library.
