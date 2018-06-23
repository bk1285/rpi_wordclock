import ConfigParser
from importlib import import_module
import netifaces
import inspect
import os
import time
from shutil import copyfile
import wordclock_tools.wordclock_display as wcd
import wordclock_interfaces.event_handler as wci
import wordclock_interfaces.web_interface as wciweb


class wordclock:
    """
    The class, which makes the wordclock run...
    """

    def __init__(self):
        """
        Initializations, executed at every startup of the wordclock
        """
        # Get path of the directory where this file is stored
        self.basePath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

        # Get wordclock configuration from config-file
        pathToConfigFile = self.basePath + '/wordclock_config/wordclock_config.cfg'
        if not os.path.exists(pathToConfigFile):
            pathToConfigFileExample = self.basePath + '/wordclock_config/wordclock_config.example.cfg'
            if not os.path.exists(pathToConfigFileExample):
                print('Error: No config-file available!')
                print('  Expected ' + pathToConfigFile + ' or ' + pathToConfigFileExample)
                raise Exception('Missing config-file')
            copyfile(pathToConfigFileExample, pathToConfigFile)
            print('Warning: No config-file specified! Was created from example-config!')
        print('Parsing ' + pathToConfigFile)
        self.config = ConfigParser.ConfigParser()
        self.config.read(pathToConfigFile)

        # Add to the loaded configuration the current base path to provide it
        # to other classes/plugins for further usage
        self.config.set('wordclock', 'base_path', self.basePath)

        self.developer_mode_active = self.config.get('wordclock', 'developer_mode', False)

        # Create object to interact with the wordclock using the interface of your choice
        self.wci = wci.event_handler()

        if not self.developer_mode_active:
            import wordclock_interfaces.gpio_interface as wcigpio
            self.gpio = wcigpio.gpio_interface(self.config, self.wci)

        # Create object to display any content on the wordclock display
        # Its implementation depends on your (individual) wordclock layout/wiring
        self.wcd = wcd.wordclock_display(self.config, self.wci)

        # Define path to general icons (not plugin-specific)
        self.pathToGeneralIcons = os.path.join(self.basePath, 'icons', self.wcd.dispRes())

        # Assemble path to plugin directory
        plugin_dir = os.path.join(self.basePath, 'wordclock_plugins')

        # Assemble list of all available plugins
        plugins = (plugin for plugin in os.listdir(plugin_dir) if os.path.isdir(os.path.join(plugin_dir, plugin)))

        # Import plugins, which can be operated by the wordclock:
        index = 0  # A helper variable (only incremented on successful import)
        self.plugins = []
        for plugin in plugins:
            # Check the config-file, whether to activate or deactivate the plugin
            try:
                if not self.config.getboolean('plugin_' + plugin, 'activate'):
                    print('Skipping plugin ' + plugin + ' since it is set to activate=false in the config-file.')
                    continue
            except:
                print('  INFO: No activate-flag set for plugin ' + plugin + ' within the config-file. Will be imported.')

            try:
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
                index += 1
            except:
                print('Failed to import plugin ' + plugin + '!')

        # Create object to interact with the wordclock using the interface of your choice
        self.plugin_index = 0
        self.wciweb = wciweb.web_interface(self)

    def startup(self):
        """
        Startup behavior
        """
        if self.config.getboolean('wordclock', 'show_startup_message'):
            startup_message = self.config.get('wordclock', 'startup_message')
            if startup_message == "ShowIP":
                interface = self.config.get('plugin_ip_address', 'interface')
                self.wcd.showText("IP: " + netifaces.ifaddresses(interface)[2][0]['addr'])
            else:
                self.wcd.showText(startup_message)

    def runPlugin(self):
        """
        Runs the currently selected plugin
        """

        try:
            print('Running plugin ' + self.plugins[self.plugin_index].name + '.')
            self.plugins[self.plugin_index].run(self.wcd, self.wci)
        except:
            print('ERROR: In plugin ' + self.plugins[self.plugin_index].name + '.')
            self.wcd.setImage(os.path.join(self.pathToGeneralIcons, 'error.png'))
            time.sleep(1)
            #self.wcd.showText('Error in ' + self.plugins[self.plugin_index].name, fg_color=wcc.RED, fps = 15)

        # Cleanup display after exiting plugin
        self.wcd.resetDisplay()

    def runNext(self, plugin_index=None):
        self.plugin_index = plugin_index if plugin_index is not None else self.default_plugin
        self.wci.setEvent(self.wci.EVENT_NEXT_PLUGIN_REQUESTED)

    def run(self):
        """
        Makes the wordclock run...
        """

        # Run the default plugin
        self.plugin_index = self.default_plugin

        # Run the wordclock forever
        while True:
            self.runPlugin()

            # If no plugin was requested yet, loop through menu to select next plugin
            if self.wci.nextAction == wci.next_action.RUN_DEFAULT_PLUGIN:
                self.plugin_index = self.default_plugin
            elif self.wci.nextAction == wci.next_action.GOTO_MENU:
                while True:
                    # The showIcon-command expects to have a plugin logo available
                    self.wcd.showIcon(plugin=self.plugins[self.plugin_index].name, iconName='logo')
                    time.sleep(self.wci.lock_time)
                    evt = self.wci.waitForEvent()
                    if evt == self.wci.EVENT_BUTTON_LEFT:
                        self.plugin_index -= 1
                        if self.plugin_index == -1:
                            self.plugin_index = len(self.plugins) - 1
                        time.sleep(self.wci.lock_time)
                    if evt == self.wci.EVENT_BUTTON_RETURN:
                        time.sleep(self.wci.lock_time)
                        break
                    if evt == self.wci.EVENT_EXIT_PLUGIN or evt == self.wci.EVENT_NEXT_PLUGIN_REQUESTED:
                        break
                    if evt == self.wci.EVENT_BUTTON_RIGHT:
                        self.plugin_index += 1
                        if self.plugin_index == len(self.plugins):
                            self.plugin_index = 0
                        time.sleep(self.wci.lock_time)


if __name__ == '__main__':
    word_clock = wordclock()
    word_clock.startup()
    word_clock.run()
