from coin_acceptor import CoinAcceptor
from led_backpack import LEDBackpack
from i2c_eeprom import EEPROMBreakout
from AttachmentManager import AttachmentManager

class CreditAttachment:

    ModeCost = {
        0: 1,
        1: 4,
        2: 1
    }

    def __init__(self)):
        
        self.eeprom = EEPROMBreakout(AttachmentManager.Types["COIN_OP"])
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
        
    def hasEnoughCredits(self, num_credits):
        return self._credits >= num_credits
        
    def setPouring(self):
        self.led_backpack.setText("POUR")
        
    def setMoving(self):
        self.led_backpack.setText("MOVE")
        
    def setFree(self):
        self.led_backpack.setText("FREE")
        
    def setDone(self):
        self.led_backpack.setText("DONE")
        
    def flashDone(self, duration=2):
        self.led_backpack.flashText("DONE")
        
    def setPush(self):
        self.led_backpack.setText("PUSH")
        
    def setCreditsInserted(self):
        cent_text = '{:.2f}'(0.25*self._credits)
        self.led_backpack.setText(cent_text)
        
    def setSleep(self)
        self.led_backpack.setText("zzzz")
        
    def setLEDBrightness(self, setting):
        self.led_backpack._display.brightness = setting