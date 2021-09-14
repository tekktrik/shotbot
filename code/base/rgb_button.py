from pulseio import PWMOut
#from digitalio import DigitalInOut, Direction, Pull
#import time
from base.simple_button import SimpleButton

class RGBButton(SimpleButton):

    class Color:
        RED = [0, 1, 1]
        GREEN = [1, 0, 1]
        BLUE = [1, 1, 0]
        PINK = [0, 1, 0]
        ORANGE = [0, 0.5, 1]
        YELLOW = [0, 0, 1]
        PURPLE = [0.5, 1, 0]
        AQUA = [1, 0, 0]
        LIGHT_BLUE = [1, 0.5, 0]
        WHITE = [0, 0, 0]
        MAGENTA = [0, 1, 0.5]
        NONE = [1, 1, 1]

    def __init__(self, input_gpio, red_gpio, green_gpio, blue_gpio):
        super().__init__(input_gpio)

        self._frequency = 5000
        self._delta_duty = 255

        freq = self._frequency

        self._red_gpio = PWMOut(red_gpio, frequency=freq, duty_cycle=0)
        self._green_gpio = PWMOut(green_gpio, frequency=freq, duty_cycle=0)
        self._blue_gpio = PWMOut(blue_gpio, frequency=freq, duty_cycle=0)

        self.current_color = [0, 0, 0]
        self.displayColor(self.Color.NONE)

    def displayColor(self, color_array):

        self._is_single_color = True

        for color_index in range(3):
            if color_array[color_index] < 0:
                color_array[color_index] = 0
            elif color_array[color_index] > 1:
                color_array[color_index] = 1

        self._red_gpio.duty_cycle = int(color_array[0]*65535)
        self._green_gpio.duty_cycle = int(color_array[1]*65535)
        self._blue_gpio.duty_cycle = int(color_array[2]*65535)

        self.current_color = color_array