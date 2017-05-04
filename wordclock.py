import ConfigParser
from importlib import import_module
import inspect
import os
import time
import traceback
import threading
import wordclock_tools.wordclock_colors as wcc
import wordclock_tools.wordclock_display as wcd
import wordclock_tools.wordclock_socket as wcs
import wordclock_interfaces.event_handler as wci
import wordclock_webinterface.web_interface as wwi

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
        pathToConfigFile = self.basePath + '/wordclock_config/wordclock_config.cfg'
        if not os.path.exists(pathToConfigFile):
            print('Warning: No config-file specified! Falling back to example-config!')
            pathToConfigFile = self.basePath + '/wordclock_config/wordclock_config.example.cfg'
        print('Parsing ' + pathToConfigFile)
        self.config = ConfigParser.ConfigParser()
        self.config.read(pathToConfigFile)

        # Add to the loaded configuration the current base path to provide it
        # to other classes/plugins for further usage
        self.config.set('wordclock', 'base_path', self.basePath)

        # Create object to interact with the wordclock using the interface of your choice
        self.wci = wci.event_handler()
        try:
            import wordclock_interfaces.gpio_interface as wcigpio
            self.gpio = wcigpio.gpio_interface(self.config, self.wci)
        except:            
            print("No GPIO interface")

        # Create object to display any content on the wordclock display
        # Its implementation depends on your (individual) wordclock layout/wiring
        self.wcd = wcd.wordclock_display(self.config,self.wci)

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
                index +=1
            except:
                #traceback.print_exc()
                print('Failed to import plugin ' + plugin + '!')

        # Create object to interact with the wordclock using the interface of your choice
        self.plugin_index = 0
        self.run_next_index = None
        self.wcs = wcs.wordclock_socket(self)
        self.wwi = wwi.wordclock_webinterface(self)
    def startup(self):
        '''
        Startup behavior
        '''
        if self.config.getboolean('wordclock', 'show_startup_message'):
            self.wcd.showText(self.config.get('wordclock', 'startup_message'))


    def runPlugin(self):
        '''
        Runs the currently selected plugin
        '''        
        self.wcs.sendCurrentPlugin(self.plugin_index)

        #try:
        print('Running plugin ' + self.plugins[self.plugin_index].name + '.')
        self.plugins[self.plugin_index].run(self.wcd, self.wci)
        #except:
        #    print('ERROR: In plugin ' + self.plugins[self.plugin_index].name + '.')
        #    self.wcd.setImage(os.path.join(self.pathToGeneralIcons, 'error.png'))
        #    time.sleep(1)
        #    self.wcd.showText('Error in ' + self.plugins[self.plugin_index].name, fg_color=wcc.RED, fps = 15)

        # Cleanup display after exiting plugin
        self.wcd.resetDisplay()

    def runNext(self, plugin_index = None):
        self.run_next_index = plugin_index

    def run(self):
        '''
        Makes the wordclock run...
        '''

        # Run the default plugin
        self.run_next_index = self.default_plugin

        # Run the wordclock forever
        while True:
            while self.run_next_index != None:
                self.plugin_index = self.run_next_index
                self.run_next_index = None
                self.runPlugin()

            # If plugin.run exits, loop through menu to select next plugin
            while True:
                # The showIcon-command expects to have a plugin logo available
                self.wcd.showIcon(plugin=self.plugins[self.plugin_index].name, iconName='logo')
                time.sleep(self.wci.lock_time)
                evt = self.wci.waitForEvent()
                if evt == self.wci.EVENT_BUTTON_LEFT:
                    self.plugin_index -=1
                    if self.plugin_index == -1:
                        self.plugin_index = len(self.plugins)-1
                    time.sleep(self.wci.lock_time)
                if evt == self.wci.EVENT_BUTTON_RETURN or evt == self.wci.EVENT_EXIT_PLUGIN:
                    time.sleep(self.wci.lock_time)
                    break
                if evt == self.wci.EVENT_BUTTON_RIGHT:
                    self.plugin_index +=1
                    if self.plugin_index == len(self.plugins):
                        self.plugin_index = 0
                    time.sleep(self.wci.lock_time)

            # Run selected plugin
            self.runPlugin()

    def run_forever(self):
        self.startup()        
        self.run()
            # After leaving selected plugin, start over again with the default plugin...

if __name__ == '__main__':
    gpio_support = True
    try:
        import wordclock_interfaces.gpio_interface as wcigpio        
    except:
        gpio_support = False
        print("No GPIO support")

    if not (gpio_support):
        # must be created first
        import wx
        app = wx.App()

    word_clock = wordclock()    
    if(gpio_support):
        word_clock.run_forever()
    else:
        print("We are not on raspberry...open simulation window")        
        wordclock_thread = threading.Thread(target=word_clock.run_forever)
        # Exit the server thread when the main thread terminates
        wordclock_thread.daemon = True
        wordclock_thread.start()    
        app.MainLoop()    
    

    
