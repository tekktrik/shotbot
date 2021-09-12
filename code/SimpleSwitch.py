from digitalio import DigitalInOut, Direction, Pull

class SimpleSwitch():

    def __init__(self, input_gpio):
        self._input_gpio = DigitalInOut(input_gpio)
        self._input_gpio.direction = Direction.INPUT
        self._input_gpio.pull = Pull.DOWN

    def isSwitched(self):
        return self._input_gpio.value