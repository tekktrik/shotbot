class EEPROMBreakout:
    
    def __init__(self, i2c_address):
        
        self._i2c = board.I2C()
        self._address = i2c_address
        self._num_data_fields = None
        
    def readDataAt(self, memory_address):
        
        returndata = []
        
        self._i2c.writeto_then_readfrom(self._address, bytearray([self._address]), bytearray([returndata]))
        
        return returndata[0]
    
    def readAllDataFields(self):
        
        data_list = []
        
        if self._num_data_fields == None:
            self._num_data_fields = self.readDataAt(0x05)
            
        for datafield_num in range(self._num_data_fields):
        
            datafield = self.readDataAt(0x06+datafield_num)
            data_list.extend(datafield)
            
        return data_list
    
    def writeDataAt(self, memory_address, data):
        
        self._i2c.writeto(self._address, bytearray([memory_address, data]))
    
    def writeAllDataFields(self, data_list):
    
        for datafield_num in range(len(data_list)):
            self.writeDataAt(0x06+datafield_num, data_list[0])
            
    @classmethod
    def initialize(cls, i2c_address, attach_num, data_list):
    
        eeprom = cls(i2c_address)
        
        eeprom.writeDataAt(0x00, ord("T"))
        eeprom.writeDataAt(0x01, ord("e"))
        eeprom.writeDataAt(0x02, ord("k"))
        eeprom.writeDataAt(0x03, ord("k"))
        eeprom.writeDataAt(0x04, attach_num)
        eeprom.writeDataAt(0x05, len(data_list))
        eeprom.writeAllDataFields(data_list)
        
        return eeprom