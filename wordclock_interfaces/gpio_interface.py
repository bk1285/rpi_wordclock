import RPi.GPIO as GPIO


class gpio_interface:
    def __init__(self, config, evtHandler):
        '''
        Initialization
        '''
        self.evtHandler = evtHandler

        # 3 buttons are required to run the wordclock.
        # Below, for each button, the corresponding GPIO-pin is specified.
        self.button_left = int(config.get('wordclock_interface', 'pin_button_left'))
        self.button_return = int(config.get('wordclock_interface', 'pin_button_return'))
        self.button_right = int(config.get('wordclock_interface', 'pin_button_right'))

        # Initializations for GPIO-input
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([self.button_left, self.button_return, self.button_right], GPIO.IN)

        interface_type = config.get('wordclock_interface', 'type')
        if interface_type == 'gpio_low':
            self.polarity = GPIO.RISING
        elif interface_type == 'gpio_high':
            self.polarity = GPIO.FALLING
        else:
            print('Warning: Unknown interface_type ' + interface_type)
            print('  Falling back to default')
            self.polarity = GPIO.RISING
        print('Interface type set to ' + interface_type)

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
