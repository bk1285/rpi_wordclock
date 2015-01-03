import ConfigParser
from importlib import import_module
import inspect
import os
import time
import wordclock_tools.buttons as wcb
import wordclock_tools.wordclock_display as wcd

# Initializations for GPIO-input
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(wcb.button_left, GPIO.IN)
GPIO.setup(wcb.button_return, GPIO.IN)
GPIO.setup(wcb.button_right, GPIO.IN)


class wordclock:
    '''
    The class, which makes the wordclock run...
    '''

    def __init__(self):
        '''
        Initializations, executed at every startup of the wordclock
        '''
        # Get path of the directory where this file is stored
        self.basePath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

        # Get wordclock configuration from config-file
        pathToConfigFile=self.basePath + '/wordclock_config/wordclock_config.cfg'
        if not os.path.exists(pathToConfigFile):
            print('Warning: no config-file specified! falling back to example-config!')
            pathToConfigFile=self.basePath + '/wordclock_config/wordclock_config.example.cfg'
        print('Parsing ' + pathToConfigFile)
        self.config = ConfigParser.ConfigParser()
        self.config.read(pathToConfigFile)

        # Add to the loaded configuration the current base path to provide it
        # to other classes/plugins for further usage
        self.config.set('wordclock','base_path', self.basePath)

        # Create object to display any content on the wordclock display
        # Its implementation depends on your (individual) wordclock layout/wiring
        self.wcd = wcd.wordclock_display(self.config)

        # Import plugins, which can be operated by the wordclock:
        plugin_dir = os.path.join(self.basePath, 'wordclock_plugins')
        self.plugins = []
        for plugin in os.listdir(plugin_dir):

            # Perform a minimal (!) validity check
            # Check, if plugin is valid (if the plugin.py is provided)
            if not os.path.isfile(os.path.join(plugin_dir, plugin, 'plugin.py')):
                continue
            try:
                print('Importing plugin ' + plugin + '...')
                self.plugins.append(import_module('wordclock_plugins.' + plugin + '.plugin').plugin(self.config))
            except:
                print('Failed to import plugin ' + plugin + '!')

    def startup(self):
        '''
        Startup behavior
        '''
        if self.config.getboolean('wordclock', 'show_startup_message'):
            startup_message = self.config.get('wordclock', 'startup_message')
            self.wcd.showText(startup_message)

    def run(self):
        '''
        Makes the wordclock run... :)
        '''
        # start wordclock in plugin 0
        plugin_index = 4

        # The main menu
        # If we are here, a user interaction has been triggered
        # depending on further user input, a new plugin is selected
        while True:
            # Run selected plugin
            self.plugins[plugin_index].run(self.wcd)

            # Cleanup display after exiting plugin
            self.wcd.resetDisplay()

            # Wait for user input to select the next plugin
            while True:
                # The showIcon-command expects to have a plugin logo available
                self.wcd.showIcon(plugin=self.plugins[plugin_index].name, iconName='logo')
                pin = self.wcd.waitForEvent([wcb.button_left, wcb.button_return, wcb.button_right], cps=10)
                if pin == wcb.button_left:
                    plugin_index -=1
                    if plugin_index == -1:
                        plugin_index = len(self.plugins)-1
                    time.sleep(0.1)
                if pin == wcb.button_return:
                    print('Selected plugin .....: ' + str(plugin_index) +
                            ' (' + str(self.plugins[plugin_index].name) + ')')
                    time.sleep(0.1)
                    break
                if pin == wcb.button_right:
                    plugin_index +=1
                    if plugin_index == len(self.plugins):
                        plugin_index = 0
                    time.sleep(0.1)

if __name__ == '__main__':
    word_clock = wordclock()
    word_clock.startup()
    word_clock.run()
