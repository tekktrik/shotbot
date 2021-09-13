import board
from enum import Enum
from AttachmentTypes import AttachmentTypes

class AttachmentChecker:
        
    def __init__(self):
        
        self._attachments = []
        
    def scan(self):
    
        i2c = board.I2C()
    
        attachment_list = []
    
        while not i2c.try_lock():
            pass
        try:
            for i2c_address in i2c.scan():
                if i2c_address in [attachment.value for attachment in AttachmentTypes]:
                    attachment_list.extend(AttachmentTypes(i2c_address))
        finally:
            i2c.unlock()
            
        self._attachments = attachment_list
        return attachment_list
        
    def isConnected(self, attachment_type):
    
        return attachment_type in self._attachments