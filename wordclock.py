import ConfigParser
from importlib import import_module
import inspect
import os
import time
import wordclock_tools.wordclock_colors as wcc
import wordclock_tools.wordclock_display as wcd
import wordclock_tools.wordclock_interface as wci


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
            print('Warning: No config-file specified! Falling back to example-config!')
            pathToConfigFile=self.basePath + '/wordclock_config/wordclock_config.example.cfg'
        print('Parsing ' + pathToConfigFile)
        self.config = ConfigParser.ConfigParser()
        self.config.read(pathToConfigFile)

        # Add to the loaded configuration the current base path to provide it
        # to other classes/plugins for further usage
        self.config.set('wordclock','base_path', self.basePath)

        # Create object to interact with the wordclock using the interface of your choice
        self.wci = wci.wordclock_interface(self.config)

        # Create object to display any content on the wordclock display
        # Its implementation depends on your (individual) wordclock layout/wiring
        self.wcd = wcd.wordclock_display(self.config)

        # Define path to general icons (not plugin-specific)
        self.pathToGeneralIcons = os.path.join(self.basePath, 'icons', self.wcd.dispRes())

        # Assemble path to plugin directory
        plugin_dir = os.path.join(self.basePath, 'wordclock_plugins')

        # Assemble list of all available plugins
        plugins = (plugin for plugin in os.listdir(plugin_dir) if os.path.isdir(os.path.join(plugin_dir, plugin)))

        # Import plugins, which can be operated by the wordclock:
        index = 0 # A helper variable (only incremented on successful import)
        self.plugins = []
        for plugin in plugins:
            # Check the config-file, whether to activate or deactivate the plugin
            try:
                if not self.config.getboolean('plugin_'+plugin, 'activate'):
                    print('Skipping plugin ' + plugin + ' since it is set to activate=false in the config-file.')
                    continue
            except:
                print('  INFO: No activate-flag set for plugin '+plugin+' within the config-file. Will be imported.')

            # Perform a minimal (!) validity check
            # Check, if plugin is valid (if the plugin.py is provided)
            if not os.path.isfile(os.path.join(plugin_dir, plugin, 'plugin.py')):
                raise
            self.plugins.append(import_module('wordclock_plugins.' + plugin + '.plugin').plugin(self.config))
            # Search for default plugin to display the time
            if plugin == 'time_default':
                print('  Selected "' + plugin + '" as default plugin')
                self.default_plugin = index
            print('Imported plugin ' + str(index) + ': "' + plugin + '".')
            index +=1
            try:
                pass
            except:
                print('Failed to import plugin ' + plugin + '!')


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
        try:
            print('Running plugin ' + self.plugins[plugin_index].name + '.')
            self.plugins[plugin_index].run(self.wcd, self.wci)
        except:
            print('ERROR: In plugin ' + self.plugins[plugin_index].name + '.')
            self.wcd.setImage(os.path.join(self.pathToGeneralIcons, 'error.png'))
            time.sleep(1)
            self.wcd.showText('Error in ' + self.plugins[plugin_index].name, fg_color=wcc.RED, fps = 15)

        # Cleanup display after exiting plugin
        self.wcd.resetDisplay()


    def run(self):
        '''
        Makes the wordclock run...
        '''

        # Run the wordclock forever
        while True:

            # Run the default plugin
            self.runPlugin(self.default_plugin)
            plugin_index = self.default_plugin

            # If plugin.run exits, loop through menu to select next plugin
            plugin_selected = False
            while not plugin_selected:
                # The showIcon-command expects to have a plugin logo available
                self.wcd.showIcon(plugin=self.plugins[plugin_index].name, iconName='logo')
                time.sleep(self.wci.lock_time)
                pin = self.wci.waitForEvent([self.wci.button_left, self.wci.button_return, self.wci.button_right], cps=10)
                if pin == self.wci.button_left:
                    plugin_index -=1
                    if plugin_index == -1:
                        plugin_index = len(self.plugins)-1
                    time.sleep(self.wci.lock_time)
                if pin == self.wci.button_return:
                    plugin_selected = True
                    time.sleep(self.wci.lock_time)
                if pin == self.wci.button_right:
                    plugin_index +=1
                    if plugin_index == len(self.plugins):
                        plugin_index = 0
                    time.sleep(self.wci.lock_time)

            # Run selected plugin
            self.runPlugin(plugin_index)

            # After leaving selected plugin, start over again with the default plugin...

if __name__ == '__main__':
    word_clock = wordclock()
    word_clock.startup()
    word_clock.run()
