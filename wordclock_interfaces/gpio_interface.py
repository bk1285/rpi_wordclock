
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

        self.virtual_button_left = int(config.get('wordclock_interface', 'virtual_pin_button_left'))
        self.virtual_button_return = int(config.get('wordclock_interface', 'virtual_pin_button_return'))
        self.virtual_button_right = int(config.get('wordclock_interface', 'virtual_pin_button_right'))

        # Initializations for GPIO-input
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([self.button_left, self.button_return, self.button_right], GPIO.IN)
        GPIO.setup([self.virtual_button_left, self.virtual_button_return, self.virtual_button_right], GPIO.OUT)

        interface_type = config.get('wordclock_interface', 'type')
        if (interface_type == 'gpio_low'):
            self.polarity = GPIO.RISING
        elif (interface_type == 'gpio_high'):
            self.polarity = GPIO.FALLING
        else:
            print('Warning: Unkonwn interface_type ' + interface_type)
            print('  Falling back to default')
            self.polarity = GPIO.RISING
        print('Interface type set to ' + interface_type)
        
        GPIO.add_event_detect(self.button_left,
                              self.polarity,
                              callback = lambda channel: self._left(),
                              debouncetime=100)
        GPIO.add_event_detect(self.button_return,
                              self.polarity,
                              callback = lambda channel: self._return(),
                              debouncetime=100)
        GPIO.add_event_detect(self.button_right,
                              self.polarity,
                              callback = lambda channel: self._right()(),
                              debouncetime=100)
        GPIO.add_event_detect(self.virtual_button_left,
                              self.polarity,
                              callback = lambda channel: self._left(),
                              debouncetime=100)
        GPIO.add_event_detect(self.virtual_button_return,
                              self.interface.polarity,
                              callback = lambda channel: self._return(),
                              debouncetime=100)
        GPIO.add_event_detect(self.virtual_button_right,
                              self.interface.polarity,
                              callback = lambda channel: self._right(),
                              debouncetime=100)
    
    def _left(self):
        self.evtHandler.setEvent(self.evtHandler.EVENT_BUTTON_LEFT)
    
    def _return(self):
        self.evtHandler.setEvent(self.evtHandler.EVENT_BUTTON_RETURN)
    
    def _right(self):
        self.evtHandler.setEvent(self.evtHandler.EVENT_BUTTON_RIGHT)

