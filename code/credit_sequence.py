import time

class ShotBotSequence:
    
    def __init__(self, device_map):
        self._device_map = device_map
        
        self._run_mode = device_map.getRunMode()
        self._mode_colors = device_map.getModeColors()
        self._inprogress_color = device_map.getInProgressColor()
        
		self._devices = device_map.getDevices()
        self._rgb_button = self._devices["rgb_button"]
        self._shot_stepper = self._devices["shot_stepper"]
        self._motor_button = self._devices["motor_button"]
        self._pump_motor = self._devices["pump_motor"]
        self._prime_switch = self._devices["prime_switch"]
        
        self._attachment_manager = device_map.getAttachmentManager()
        self._credit_attachment = self._devices["credit_attachment"]

    def switchMode():
            try:
                self._run_mode.advanceMode()
            except:
                self._rgb_button.displayColor(self._rgb_button.Color.ORANGE)
                quit
        self._.led_backpack.flashText(RunMode.ModeNames[run_mode.getMode()])

    def checkInputs(self):
        if not self._run_mode.isAsleep():
            self._rgb_button.displayColor(self._mode_colors[self._run_mode.getMode()])
            self._credit_attachment.setLEDBrightness(1)
            self._credit_attachment.setCreditsInserted()
            self._credit_attachment.checkCoinInserted()
            if self._shot_stepper.isPastReleaseTimeout():
                self._run_mode.setToSleepMode()
                self._shot_stepper.release()
                self._credit_attachment.setSleep()
                self._credit_attachment.setLEDBrightness(0.5)
            elif self._motor_button.isPushed():
                self.moveGlassesCheck()
            elif self._prime_switch.isSwitched():
                self.runPriming()
            elif self._rgb_button.isPushed():
                if self._rgb_button.isPushedFor(2):
                    self.switchMode()
                    time.sleep(0.75)
                    return
                else:
                    if not self._credit_attachment.hasEnoughCredits(CreditAttachment.ModeCost[run_mode.getMode()]):
                        self._credit_attachment.led_backpack.flashText("MORE", 1)
                        time.sleep(1)
                        return
                    self._rgb_button.displayColor(self._inprogress_color)
                    self.runModeCheck()
                    self._rgb_button.displayColor(self._mode_colors[self._run_mode.getMode()])
        else:
            self._rgb_button.displayColor(self._rgb_button.Color.WHITE)
            if self._rgb_button.isPushed():
                self._run_mode.wakeUp()
                self._shot_stepper.updateReleaseTimeout()
                self._rgb_button.displayColor(self._mode_colors[self._run_mode.getMode()])
                time.sleep(0.75)

    def runModeCheck(self):
        mode = run_mode.getMode()
        if mode == 0:
            runSingleMode()
        elif mode == 1:
            runFullMode()
        elif mode == 2:
            runPartyMode()
        
    def moveGlassesCheck(self):
    
        if self._motor_button.isPushedFor(2):
            self._credit_attachment.setFree()
            while self._motor_button.isPushed():
                self._shot_stepper.release()
                time.sleep(0.01)
            self._shot_stepper.unrelease()
        else:
            self._credit_attachment.setMoving()
            self._shot_stepper.moveToNextGlass()
            
    def runPriming(self):
        while self._prime_switch.isSwitched():
            self._credit_attachment.setPouring()
            self._pump_motor.pumpAt(self._pump_motor.max_speed)
            time.sleep(0.01)
        SELF._pump_motor.turnOff()
        time.sleep(0.25)
        
    def runSingleMode(self):
		
        self._credit_attachment.spendCredit()
        self._credit_attachment.setMoving()
        self._shot_stepper.moveToNextGlass()
        self._shot_stepper.moveToNextGlass()
        self._credit_attachment.setPouring()
        self._pump_motor.pumpVolume(44)
        time.sleep(0.5)
        self._credit_attachment.setMoving()
        self._shot_stepper.moveToNextGlass()
        self._shot_stepper.moveToNextGlass()
        self._credit_attachment.flashDone()
        
    def runFullMode(self):
        
        self._credit_attachment.spendCredit(4)
        for glass in range(self._shot_stepper.num_glasses):
            self._credit_attachment.setMoving()
            self._shot_stepper.moveToNextGlass()
            time.sleep(0.25)
            self._credit_attachment.setPouring()
            self._pump_motor.pumpVolume(44)
            time.sleep(0.25)
        self._credit_attachment.flashDone()
        time.sleep(0.5)

    def runPartyMode(self):
		
        self._credit_attachment.spendCredit(1)
        direction = 0
        for movement in range(5):
            self._credit_attachment.setMoving()
            self._shot_stepper.moveToRandomGlass(reverse_direction=direction)
            direction = (direction + 1) % 2
            time.sleep(1)
        for cycle_num in range(3):
            self._credit_attachment.flashDone()
            self._rgb_button.displayColor(self._rgb_button.Color.LIGHT_BLUE)
            time.sleep(0.5)
            self._rgb_button.displayColor(self._rgb_button.Color.AQUA)
            time.sleep(0.5)

    def run(self):
        while True:
            checkInputs()
            self._credit_attachment.led_backpack.checkFlashText()
            time.sleep(0.01)