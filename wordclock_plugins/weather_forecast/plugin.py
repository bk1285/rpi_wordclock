import logging
import os
import pywapi
import time
import wordclock_tools.wordclock_colors as wcc


class plugin:
    """
    A class to display the expected weather for a given location.
    Uses pywapi to retrieve information...
    """

    def __init__(self, config):
        '''
        Initializations for the startup of the weather forecast
        '''
        # Get plugin name (according to the folder, it is contained in)
        self.name = os.path.dirname(__file__).split('/')[-1]
        self.pretty_name = "Weather forecast"
        self.description = "Displays the current temperature"

        self.location_id = config.get('plugin_' + self.name, 'location_id')
        self.weather_service = config.get('plugin_weather_forecast', 'weather_service')

        try:
            import am2302_ths
            self.pin_temp_sensor = int(config.get('wordclock_interface', 'pin_temp_sensor'))
            self.temp_sensor_registered = True
            logging.info('Registered temperature sensor at pin ' + str(self.pin_temp_sensor) + '.')
        except:
            logging.warning('Assumes no temperature sensor to be attached.')
            self.temp_sensor_registered = False

    def run(self, wcd, wci):
        """
        Displaying expected temperature
        """
        # Get current forecast
        if self.weather_service == 'yahoo':
            current_weather_forecast = pywapi.get_weather_from_yahoo(self.location_id)
        elif self.weather_service == 'weather_dot_com':
            current_weather_forecast = pywapi.get_weather_from_weather_com(self.location_id)
        else:
            logging.warning('No valid weather_forecast found!')
            return
        outdoor_temp = current_weather_forecast['current_conditions']['temperature']
        if self.temp_sensor_registered:
            try:
                indoor_temp = str(int(round(am2302_ths.get_temperature(self.pin_temp_sensor))))
                wcd.showText(outdoor_temp + '*', count=1, fps=8)
                wcd.showText(indoor_temp + '*', count=1, fg_color=wcc.GREEN, fps=8)
                wcd.showText(outdoor_temp + '*', count=1, fps=8)
                wcd.showText(indoor_temp + '*', count=1, fg_color=wcc.GREEN, fps=8)
            except:
                logging.error('Failed to read temperature sensor!')
                wcd.showText(outdoor_temp + '*   ' + outdoor_temp + '*   ' + outdoor_temp + '*', count=1, fps=8)
        else:
            wcd.showText(outdoor_temp + '*   ' + outdoor_temp + '*   ' + outdoor_temp + '*', count=1, fps=8)

        if wci.waitForExit(1.0):
            return
