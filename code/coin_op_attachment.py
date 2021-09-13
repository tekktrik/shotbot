from coin_acceptor import CoinAcceptor
from led_backpack import LEDBackpack
from i2c_eeprom import EEPROMBreakout

class CoinOpAttachment:

    def __init__(self, eeprom_i2c_address, pulse_gpio, led_i2c_address):
        
        self.eeprom = EEPROMBreakout(eeprom_i2c_address)
        self.coin_acceptor = CoinAcceptor(pulse_gpio)
        self.led_backpack = LEDBackpack(led_i2c_address)
        
    def initialize(self):
        
        stored_data = self.eeprom.readAllData()
        
    def checkCoinInserted(self):
        
        self.