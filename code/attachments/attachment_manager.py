import board

class AttachmentManager:

    Types = {
        "COIN_OP": 0x50
    }
        
    def __init__(self):
    
        self._attachments = []
        self.scan()
        
    def scan(self):
        i2c = board.I2C()
        attachment_list = []
    
        while not i2c.try_lock():
            pass
        try:
            for i2c_address in i2c.scan():
                if i2c_address in [address for address in Attachments.Types.values()]:
                    attachment_list.extend(i2c_address)
        finally:
            i2c.unlock()
            
        self._attachments = attachment_list
        return attachment_list
        
    def hasAttachment(self, attachment_type):
        return attachment_type in self._attachments
    
    @classmethod
    def getNameForAddress(cls, input_address):
    
        for name, address in cls.Types.items():
            if address == input_address:
                return name