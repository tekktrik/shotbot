import board
import time
from adafruit_ht16k33.segments import Seg14x4

class LEDBackpack:

    def __init__(self, i2c_address):
    
        self._address = i2c_address
        self._i2c = board.I2C()
        self._display = Seg14x4(self._i2c, address=self._address)
        self._current_text = ""
        self._flash_text = ""
        self._flash_end = None
        self._display.fill(0)
        
    def setText(self, input_text):
        
        self._current_text = input_text
        self._display.print(input_text)
        
    def flashText(self, input_text, duration=2):
        
        if (input_text != self._flash_text):
            self._flash_text = input_text
            self._display.print(self._flash_text)
            self._flash_end = time.monotonic() + duration
        elif time.monotonic() >= self._flash_end:
            pass
        else:
            self.setText(self._current_text)
        
    def setPouring(self):
        self.setText("POUR")
        
    def setMoving(self):
        self.setText("MOVE")
        
    def setDone(self):
        self.setText("DONE")
        
    def setPush(self):
        self.setText("PUSH")
        
    def flashSingleGlass(self):
        self.flashText("SING")
        
    def flashAllGlasses(self):
        self.flashText("ALL")
        
    def flashRandomGlass(self):
        self.flashText("RAND")
        
    def setInputQuarters(self, num_quarters):
        cent_text = '{:.2f}'(0.25*num_quarters)
        self.setText(cent_text)
        
    def flashShotBotName(self):
        self._display.marquee("SHOTBOT BY TEKKTRIK", 0.25, False)
    
    def checkFlashText(self):
        self.flashText(self._flash_text)