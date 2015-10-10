import os
import pywapi
import time

class plugin:
    '''
    A class to display the expected weather for a given location.
    Uses pywapi to retrieve information...
    '''

    def __init__(self, config):
        '''
        Initializations for the startup of the weather forecast
        '''
        # Get plugin name (according to the folder, it is contained in)
        self.name = os.path.dirname(__file__).split('/')[-1]
        self.location_id = config.get('plugin_' + self.name, 'location_id')
        self.weather_service = config.get('plugin_weather_forecast', 'weather_service')

    def run(self, wcd, wci):
        '''
        Displaying expected temperature
        '''
        # Get current forecast
        if self.weather_service == 'yahoo':
            current_weather_forecast = pywapi.get_weather_from_yahoo(self.location_id)
        elif self.weather_service == 'weather_dot_com':
            current_weather_forecast = pywapi.get_weather_from_weather_com(self.location_id)
        else:
            print('Warning: No valid weather_forecast found!')
            return
        temp=current_weather_forecast['current_conditions']['temperature']
        wcd.showText('    ' + temp + '*   ' + temp + '*   ' + temp + '*   ', count=1, fps=8)
        time.sleep(1)
