import board
from enum import Enum

class AttachmentChecker:

    BASE_EEPROM_ADDRESS = 0x50
    EEPROM_ADDRESS_OPTIONS = 8
    
    class AttachmentType(Enum):
    
        COIN_OP = 0x50
        MULTIPLEXER = 0x51
        
    @classmethod
    def scan(cls):
    
        i2c = board.I2C()
    
        attachment_dict = {}
    
        while not i2c.try_lock():
            pass
        try:
            for i2c_address in i2c.scan():
                if i2c_address in range(BASE_EEPROM_ADDRESS, BASE_EEPROM_ADDRESS+EEPROM_ADDRESS_OPTIONS):
                    attachment_dict[i2c_address] = cls.AttachmentType(i2c_address)
        finally:
            i2c.unlock()
            
        return attachment_dict