class RunMode:

    ModeNames = {
        0: "SING",
        1: "ALL",
        2: "RAND"
    }

    def __init__(self, startup_mode):
        self._mode = startup_mode
        self._sleeping = False
        self._num_modes = len(self.ModeNames.keys())

    def setToMode(self, new_mode_num):
        self._mode = new_mode_num

    def advanceMode(self):
        highest_mode = self._num_modes-1
        if self._mode < highest_mode:
            self._mode += 1
        elif self._mode == highest_mode:
            self._mode = 0
        else:
            raise Exception("Invalid mode assignment")

    def getMode(self):
        return self._mode

    def setToSleepMode(self):
        self._sleeping = True

    def wakeUp(self):
        self._sleeping = False

    def isAsleep(self):
        return self._sleeping