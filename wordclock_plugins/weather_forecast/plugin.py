import logging
import os
import requests
import json
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

        self.weather_service = config.get('plugin_weather_forecast', 'weather_service')
        if self.weather_service == 'openweathermap':
            self.api_key = config.get('plugin_weather_forecast', 'api_key')
            self.city = config.get('plugin_weather_forecast', 'city')
        elif self.weather_service == 'meteoswiss':
            self.zipcode = config.get('plugin_weather_forecast', 'zipcode')

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
        if self.weather_service == 'openweathermap':
            outdoor_temp = str((json.loads(requests.get('http://api.openweathermap.org/data/2.5/weather?q=' + self.city + '&appid=' + self.api_key + '&units=metric').text))['main']['temp'])
        elif self.weather_service == 'meteoswiss':
            outdoor_temp = (json.loads(requests.get('https://www.meteoschweiz.admin.ch/product/output/weather-widget/forecast/version__20210514_1034/de/' + self.zipcode + '00.json', headers={'referer': 'https://www.meteoschweiz.admin.ch/home/service-und-publikationen/produkte.html'}).text))['data']['current']['temperature']
        else:
            logging.warning('No valid weather_forecast found!')
            return
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
