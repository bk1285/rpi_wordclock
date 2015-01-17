import ConfigParser
from importlib import import_module
import inspect
import os
import time
import wordclock_tools.wordclock_colors as wcc
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

        # Define path to general icons (not plugin-specific)
        self.pathToGeneralIcons = os.path.join(self.basePath, 'icons', self.wcd.dispRes())

        # Import plugins, which can be operated by the wordclock:
        plugin_dir = os.path.join(self.basePath, 'wordclock_plugins')
        self.plugins = []
        for index, plugin in enumerate(os.listdir(plugin_dir)):
            # Perform a minimal (!) validity check
            # Check, if plugin is valid (if the plugin.py is provided)
            if not os.path.isfile(os.path.join(plugin_dir, plugin, 'plugin.py')):
                continue
            try:
                print('Importing plugin ' + plugin + '...')
                self.plugins.append(import_module('wordclock_plugins.' + plugin + '.plugin').plugin(self.config))
            except:
                print('Failed to import plugin ' + plugin + '!')
            if plugin == 'time_default':
                print('  Selected ' + plugin + ' as default plugin')
                self.default_plugin = index


    def startup(self):
        '''
        Startup behavior
        '''
        if self.config.getboolean('wordclock', 'show_startup_message'):
            self.wcd.showText(self.config.get('wordclock', 'startup_message'))


    def runPlugin(self, plugin_index):
        '''
        Runs a selected plugin
        '''
        print('Running plugin ' + self.plugins[plugin_index].name + '.')
        try:
            self.plugins[plugin_index].run(self.wcd)
        except:
            print('Error in plugin ' + self.plugins[plugin_index].name + '.')
            self.wcd.setImage(os.path.join(self.pathToGeneralIcons, 'error.png'))
            time.sleep(1)
            self.wcd.showText('Error in ' + self.plugins[plugin_index].name, fg_color=wcc.RED, fps = 15)

        # Cleanup display after exiting plugin
        self.wcd.resetDisplay()


    def run(self):
        '''
        Makes the wordclock run... :)
        '''
        plugin_index = self.default_plugin

        # Run the wordclock forever
        while True:

            # Wait for user input to select the next plugin
            while True:
                # Run the default plugin
                self.runPlugin(self.default_plugin)

                # If plugin exits, go to menu to select next plugin
                plugin_selected = False
                while not plugin_selected:
                    # The showIcon-command expects to have a plugin logo available
                    self.wcd.showIcon(plugin=self.plugins[plugin_index].name, iconName='logo')
                    pin = self.wcd.waitForEvent([wcb.button_left, wcb.button_return, wcb.button_right], cps=10)
                    if pin == wcb.button_left:
                        plugin_index -=1
                        if plugin_index == -1:
                            plugin_index = len(self.plugins)-1
                        time.sleep(0.1)
                    if pin == wcb.button_return:
                        time.sleep(0.1)
                        plugin_selected = True
                    if pin == wcb.button_right:
                        plugin_index +=1
                        if plugin_index == len(self.plugins):
                            plugin_index = 0
                        time.sleep(0.1)

                # Run selected plugin
                self.runPlugin(plugin_index)

                # After leaving selected plugin, we start over at the while loop
                # with the default plugin...

if __name__ == '__main__':
    word_clock = wordclock()
    word_clock.startup()
    word_clock.run()
