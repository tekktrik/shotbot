from digitalio import DigitalInOut, Direction, Pull
import time

class SimpleButton:

    def __init__(self, input_gpio):
        self._input_gpio = DigitalInOut(input_gpio)
        self._input_gpio.direction = Direction.INPUT
        self._input_gpio.pull = Pull.DOWN

    def isPushed(self):
        return self._input_gpio.value

    def isPushedFor(self, target_time):
        frequency = 0.1
        numAttempts = int(target_time/frequency)

        for attempt in range(numAttempts):
            if self.isPushed():
                time.sleep(frequency)
            else:
                return False

        return True