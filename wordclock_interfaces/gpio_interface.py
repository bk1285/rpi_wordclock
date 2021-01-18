import RPi.GPIO as GPIO
import logging


class gpio_interface:
    def __init__(self, config, evtHandler):
        '''
        Initialization
        '''
        interface_type = config.get('wordclock_interface', 'type')

        if interface_type == 'no_gpio':
            logging.info('GPIO interface disabled. If hardware buttons are attached, any input is ignored. Webinterface can be used instead.')
            return

        self.evtHandler = evtHandler

        # 3 buttons are required to run the wordclock.
        # Below, for each button, the corresponding GPIO-pin is specified.
        self.button_left = int(config.get('wordclock_interface', 'pin_button_left'))
        self.button_return = int(config.get('wordclock_interface', 'pin_button_return'))
        self.button_right = int(config.get('wordclock_interface', 'pin_button_right'))

        # Initializations for GPIO-input
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([self.button_left, self.button_return, self.button_right], GPIO.IN)

        if interface_type == 'gpio_high':
            self.polarity = GPIO.FALLING
        else:
            if interface_type != 'gpio_low':
                logging.warning('Unknown interface_type ' + interface_type)
                logging.warning('  Falling back to default')
                interface_type = 'gpio_low'
            self.polarity = GPIO.RISING

        logging.info('Interface type set to ' + interface_type)

        GPIO.add_event_detect(self.button_left,
                              self.polarity,
                              callback=lambda channel: self._left(),
                              bouncetime=100)
        GPIO.add_event_detect(self.button_return,
                              self.polarity,
                              callback=lambda channel: self._return(),
                              bouncetime=100)
        GPIO.add_event_detect(self.button_right,
                              self.polarity,
                              callback=lambda channel: self._right(),
                              bouncetime=100)

    def _left(self):
        self.evtHandler.setEvent(self.evtHandler.EVENT_BUTTON_LEFT)

    def _return(self):
        self.evtHandler.setEvent(self.evtHandler.EVENT_BUTTON_RETURN)

    def _right(self):
        self.evtHandler.setEvent(self.evtHandler.EVENT_BUTTON_RIGHT)
