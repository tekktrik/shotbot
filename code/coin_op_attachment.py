from coin_acceptor import CoinAcceptor
from led_backpack import LEDBackpack

class CoinOpAttachment:

    def __init__(self, pulse_gpio, led_i2c):
        
        self._i2c = i2c_object
        self._coin_acceptor = CoinAcceptor(pulse_gpio)
        self._led_backpack = LEDBackpack(led_i2c)
        
    def check for 