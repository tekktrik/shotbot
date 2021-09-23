class DeviceMap:

    def __init__(self):
        self._device_dict = {}
        self._colors = {}
        self._run_mode = None
        
    def addDevice(self, device_name, device):
        self._device_dict[device_name] = device
        
    def getDevice(self, device_name):
        return self._device_dict[device_name]
    
    def getDevices(self):
        return self._device_dict
        
    def removeDevice(self, device_name):
        del self._device_dict[device_name]
        
    def getDeviceNames(self):
        return self._device_dict.keys()
        
    def getDeviceList(self):
        return self._device_dict.values()
        
    def addAttachmentManager(self, attachment_manager):
        self._attachment_manager = attachment_manager
        
    def getAttachmentManager(self):
        return self._attachment_manager
        
    def addModeColors(self, color_list):
        self._colors["mode_colors"] = color_list
        
    def getModeColors(self):
        return self._colors["mode_colors"]
        
    def addInProgressColor(self, in_progress_color):
        self._colors["in_progress_color"] = in_progress_color
        
    def getInProgressColor(self):
        return self._colors["in_progress_color"]
        
    def addRunMode(self, run_mode):
        self._run_mode = run_mode
        
    def getRunMode(self):
        return self._run_mode