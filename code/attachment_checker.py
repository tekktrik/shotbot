import board

class AttachementChecker:

    def __init__(self, ):
        
        self._i2c = board.I2C()

    def scan(self):
    
        while not self._i2c.try_lock():
            pass
        
        try:
            for i2c_address in self._i2c.scan():
                
                self._i2c.
                
        finally:
            self._i2c.unlock()