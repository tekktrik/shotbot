class RunMode:

    def __init__(self, startup_mode):
        self._mode = startup_mode
        self._sleeping = False

    def setToMode(self, new_mode_num):
        self._mode = new_mode_num

    def advanceMode(self):
        if self._mode == 0:
            self._mode = 1
        elif self._mode == 1:
            self._mode = 2
        elif self._mode == 2:
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