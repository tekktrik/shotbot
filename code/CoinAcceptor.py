from digitalio import DigitalInOut, Direction, Pull

class CoinAcceptor:

    def __init__(self, pulse_pin):
        
        self._pulse_pin = DigitalInOut(pulse_pin)
        self._pulse_pin.direction = Direction.INPUT
        self._pulse_pin.pull = Pull.DOWN
        
    def checkCoinInserted(self):
        
        if self._pulse_pin.value == True:
            while self._pulse_pin.value == True:
                pass
            return True
        else:
            return False