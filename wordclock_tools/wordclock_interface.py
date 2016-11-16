import RPi.GPIO as GPIO
import time

class wordclock_interface:
    '''
    A class taking control of the interface of the wordclock
    This might be buttons, rotary encoder, capacitive switches or others
    '''

    def __init__(self, config):
        '''
        Setup interface
        '''

        print('Setting up wordclock interface')
        self.interface = button_settings(config)
        self.button_left   = self.interface.button_left
        print('  Mapping button "left" to pin ' + str(self.interface.button_left) + '.')
        self.button_return = self.interface.button_return
        print('  Mapping button "return" to pin ' + str(self.interface.button_return) + '.')
        self.button_right  = self.interface.button_right
        print('  Mapping button "right" to pin ' + str(self.interface.button_right) + '.')

        self.virtual_button_left   = self.interface.virtual_button_left
        print('  Mapping button "virtual_left" to pin ' + str(self.interface.virtual_button_left) + '.')
        self.virtual_button_return = self.interface.virtual_button_return
        print('  Mapping button "virtual_return" to pin ' + str(self.interface.virtual_button_return) + '.')
        self.virtual_button_right  = self.interface.virtual_button_right
        print('  Mapping button "virtual_right" to pin ' + str(self.interface.virtual_button_right) + '.')

        self.lock_time = float(config.get('wordclock_interface', 'lock_time'))
        print('  Lock time of buttons is ' + str(self.lock_time) + ' seconds')

    def getPinState(self, pin):
        '''
        Return state of a given pin
        '''
        # Return "not" since triggered GPIOs go to ground (low)
        return self.interface.pinState(pin)

    def waitForEvent(self, pinrange_to_listen, cps=10):
        '''
        Waits forever for event on a given set of pin (events such as user interaction, button press, etc.)
        cps: Checks per second
        '''
        while True:
            for i in pinrange_to_listen:
                virtual_pin = -1
                if(i == self.button_left):
                    virtual_pin = self.virtual_button_left
                if(i == self.button_right):
                    virtual_pin = self.virtual_button_right
                if(i == self.button_return):
                    virtual_pin = self.virtual_button_return
                if self.interface.pinState(i) or not self.interface.pinState(virtual_pin):
                    print('Pin ' + str(i) + ' pressed.')
                    return i
            time.sleep(1.0/cps)

    def waitSecondsForEvent(self, pinrange_to_listen, seconds, cps=10):
        '''
        Waits for number of seconds for event on a given set of pin (events such as user interaction, button press, etc.)
        cps: Checks per second
        '''
        for _ in range(int(seconds*cps)):
            for i in pinrange_to_listen:
                virtual_pin = -1
                if(i == self.button_left):
                    virtual_pin = self.virtual_button_left
                if(i == self.button_right):
                    virtual_pin = self.virtual_button_right
                if(i == self.button_return):
                    virtual_pin = self.virtual_button_return
                if self.interface.pinState(i) or not self.interface.pinState(virtual_pin):
                    print('Pin ' + str(i) + ' pressed.')
                    return i
            time.sleep(1.0/cps)
        return -1

class button_settings:
    '''
    Class, implementing a wordclock interface using buttons.
    '''

    def __init__(self, config):
        '''
        Initialization
        '''

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
        GPIO.setup(self.button_left, GPIO.IN)
        GPIO.setup(self.button_return, GPIO.IN)
        GPIO.setup(self.button_right, GPIO.IN)
        GPIO.setup(self.virtual_button_left, GPIO.OUT)
        GPIO.setup(self.virtual_button_return, GPIO.OUT)
        GPIO.setup(self.virtual_button_right, GPIO.OUT)

        interface_type = config.get('wordclock_interface', 'type')
        if (interface_type == 'gpio_low'):
            self.alter_interface_state = False
        elif (interface_type == 'gpio_high'):
            self.alter_interface_state = True
        else:
            print('Warning: Unkonwn interface_type ' + interface)
            print('  Falling back to default')
            self.alter_interface_state = False
        print('Interface type set to ' + interface_type + ' (' + str(self.alter_interface_state) + ')')

    def pinState(self, i):
        return self.alter_interface_state == GPIO.input(i)

