from coin_acceptor import CoinAcceptor
from led_backpack import LEDBackpack
from i2c_eeprom import EEPROMBreakout

class CreditAttachment:

    def __init__(self, eeprom_i2c_address):
        
        self.eeprom = EEPROMBreakout(eeprom_i2c_address)
        eeprom_data = self.eeprom.readAllData()
        
        led_i2c_address = eeprom_data[0]
        pulse_gpio = eeprom_data[1]
        self._shot_price = eeprom_data[2]
        
        self.led_backpack = LEDBackpack(led_i2c_address)
        self.coin_acceptor = CoinAcceptor(pulse_gpio)
        
        self._credits = 0
        
        self.led_backpack.marqueeShotBotName()
        
    def checkCoinInserted(self):
        if self.coin_acceptor.checkCoinInserted():
            self._credits += 1
            self.led_backpack.setCreditsInserted(self._credits)
            
    def spendCredit(self, num_credits=1):
        self._credits -= num_credits