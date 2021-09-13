class EEPROMBreakout:

    BASE_ADDRESS = 0x50
    FIELD_NUM_DATAFIELDS = 0x00
    BASE_DATA_FIELDS = FIELD_NUM_DATAFIELDS + 1
    
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
            self._num_data_fields = self.getNumOfDataFields()
            
        for datafield_num in range(self._num_data_fields):
        
            datafield = self.readDataAt(BASE_DATA_FIELDS+datafield_num)
            data_list.extend(datafield)
            
        return data_list
    
    def writeDataAt(self, memory_address, data):
        
        self._i2c.writeto(self._address, bytearray([memory_address, data]))
    
    def writeAllDataFields(self, data_list):
    
        for datafield_num in range(len(data_list)):
            self.writeDataAt(BASE_DATA_FIELDS+datafield_num, data_list[0])
            
    def getAttachmentNum(self):
    
        return (self._address - self.BASE_ADDRESS) + 1
            
    def getNumOfDataFields(self):
        
        return self.readDataAt(self.FIELD_NUM_DATAFIELDS)
        
    def setNumOfDataFields(self, num_datafields):
    
        self.writeDataAt(self.FIELD_NUM_DATAFIELDS, num_datafields)
            
    @classmethod
    def initialize(cls, i2c_address, attach_num, data_list):
    
        eeprom = cls(i2c_address)
        
        eeprom.setNumOfDataFields(len(data_list))
        eeprom.writeAllDataFields(data_list)
        
        return eeprom
        
    @classmethod
    def wipe(cls, i2c_address):
    
        eeprom = cls(i2c_address)
            
        num_datafields = eeprom.getNumOfDataFields()
        eeprom.setNumOfDataFields(0)
        eeprom.writeAllDataFields([0]*num_datafields)
        
        return eeprom
        
    @classmethod
    def manual_wipe(cls, i2c_address, num_entries=255):
    
        eeprom = cls(i2c_address)
        
        for entry_num in range(num_entries):
            eeprom.writeDataAt(entry_num, 0)
            
        return eeprom