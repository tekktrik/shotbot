import time
import board
import os
import sys
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

class ShotStepper:

    num_glasses = 4
    total_steps = 200
    steps_per_glass = total_steps/num_glasses
    timeout_min = 5

    def __init__(self, stepper_number, release=False):
        kit = MotorKit(i2c=board.I2C())
        if stepper_number == 1:
            self._stepper = kit.stepper1
        elif stepper_number == 2:
            self._stepper = kit.stepper2
        else:
            raise Exception("Invalid stepper number for motor kit")
        self._release_timeout = None
        self.updateReleaseTimeout()
        if release:
            self.release()

    def moveSteps(self, num_steps, reverse_direction=False):
        for step in range(num_steps):
            if not reverse_direction:
                self._stepper.onestep()
            else:
                self._stepper.onestep(direction=stepper.BACKWARD)
            time.sleep(0.02)

    def release(self):
        self._stepper.release()

    def unrelease(self):
        self.moveSteps(1, reverse_direction=True)
        self.moveSteps(1)

    def moveToNextGlass(self, reverse_direction=False):
        steps = self.steps_per_glass
        self.moveSteps(steps, reverse_direction=reverse_direction)

    def moveToRandomGlass(self, reverse_direction=False):
        random_glass = (int.from_bytes(os.urandom(1), sys.byteorder) % 4) + 1
        for movement in range(random_glass):
            self.moveToNextGlass(reverse_direction=reverse_direction)

    def updateReleaseTimeout(self, auto_unrelease=True):
        self._release_timeout = time.time()
        if auto_unrelease:
            self.unrelease()

    def isPastReleaseTimeout(self, auto_release=False):
        currentTime = time.time()
        timeoutTime = self._release_timeout + (self.timeout_min*60)
        if currentTime >= timeoutTime:
            if auto_release:
                self.release()
            return True
        else:
            return False