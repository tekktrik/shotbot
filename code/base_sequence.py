import time

class ShotBotSequence:
    
    def __init__(self, device_map):
        self._device_map = device_map
        self._run_mode = device_map.getRunMode()
        self._mode_colors = device_map.getModeColors()
        self._inprogress_color = device_map.getInProgressColor()
		self._devices = device_map.getDevices()

    def switchMode(self):
		rgb_button = self._devices["rgb_button"]
		
        try:
            self._run_mode.advanceMode()
        except:
            rgb_button.displayColor(rgb_button.Color.ORANGE)
            quit
        rgb_button.displayColor(self._mode_colors[self._run_mode.getMode()])

    def checkInputs(self):
        rgb_button = self._devices["rgb_button"]
        shot_stepper = self._devices["shot_stepper"]
        
        if not self._run_mode.isAsleep():
            rgb_button.displayColor(self._mode_colors[self._run_mode.getMode()])
            if shot_stepper.isPastReleaseTimeout():
                self._run_mode.setToSleepMode()
                shot_stepper.release()
            elif self._devices["motor_button"].isPushed():
                self.moveGlassesCheck()
            elif self._devices["prime_switch"].isSwitched():
                self.runPriming()
            elif rgb_button.isPushed():
                if rgb_button.isPushedFor(2):
                    self.switchMode()
                    time.sleep(0.75)
                    return
                else:
                    rgb_button.displayColor(self._inprogress_color)
                    self.runModeCheck()
                    rgb_button.displayColor(self._mode_colors[self._run_mode.getMode()])
        else:
            rgb_button.displayColor(rgb_button.Color.WHITE)
            if rgb_button.isPushed():
                self._run_mode.wakeUp()
                shot_stepper.updateReleaseTimeout()
                rgb_button.displayColor(self._mode_colors[self._run_mode.getMode()])
                time.sleep(0.75)

    def runModeCheck(self):
        mode = self._run_mode.getMode()
        if mode == 0:
            self.runSingleMode()
        elif mode == 1:
            self.runFullMode()
        elif mode == 2:
            self.runPartyMode()

    def moveGlassesCheck(self):
        motor_button = self._devices["motor_button"]
        shot_stepper = self._devices["shot_stepper"]
    
        if motor_button.isPushedFor(2):
            while motor_button.isPushed():
                shot_stepper.release()
                time.sleep(0.01)
            shot_stepper.unrelease()
        else:
            shot_stepper.moveToNextGlass()

    def runPriming(self):
        pump_motor = self._devices["pump_motor"]
        
        while self._devices["prime_switch"].isSwitched():
            pump_motor.pumpAt(pump_motor.max_speed)
            time.sleep(0.01)
        pump_motor.turnOff()
        time.sleep(0.25)

    def runSingleMode(self):
		shot_stepper = self._devices["shot_stepper"]
		
        shot_stepper.moveToNextGlass()
        shot_stepper.moveToNextGlass()
        self._devices["pump_motor"].pumpVolume(44)
        time.sleep(0.5)
        shot_stepper.moveToNextGlass()
        shot_stepper.moveToNextGlass()

    def runFullMode(self):
        shot_stepper = self._devices["shot_stepper"]
        
        for glass in range(shot_stepper.num_glasses):
            shot_stepper.moveToNextGlass()
            time.sleep(0.25)
            self._devices["pump_motor"].pumpVolume(44)
            time.sleep(0.25)
        time.sleep(0.5)


    def runPartyMode(self):
		rgb_button = self._devices["rgb_button"]
		
        direction = 0
        for movement in range(5):
            self._devices["shot_stepper"].moveToRandomGlass(reverse_direction=direction)
            direction = (direction + 1) % 2
            time.sleep(1)
        for cycle_num in range(3):
            rgb_button.displayColor(rgb_button.Color.LIGHT_BLUE)
            time.sleep(0.5)
            rgb_button.displayColor(rgb_button.Color.AQUA)
            time.sleep(0.5)

    def run(self):
        while True:
            self.checkInputs()
            time.sleep(0.01)