import time
import board
from adafruit_motorkit import MotorKit
# from adafruit_motor import stepper

class PumpMotor:

    max_speed = 100

    def __init__(self, stepper_number, tubing_bore=0.2):
        kit = MotorKit(i2c=board.I2C())
        if stepper_number == 1:
            self._motor = kit.motor1
        elif stepper_number == 2:
            self._motor = kit.motor2
        elif stepper_number == 3:
            self._motor = kit.motor3
        elif stepper_number == 4:
            self._motor = kit.motor4
        else:
            raise Exception("Invalid motor number for motor kit")
        self._motor.throttle = 0

    def pumpAt(self, flowrate):
        if (flowrate >= -100) and (flowrate <= 100):
            self._motor.throttle = flowrate/100
        else:
            raise Exception("Invalid flowrate for this pump")

    def pumpAtFor(self, flowrate, duration, rgb=None):
        self.pumpAt(flowrate)
        if rgb == None:
            time.sleep(duration)
        else:
            freq = 0.01
            pulses = duration/freq
            for pulse in range(pulses):
                rgb.toggleDisplayRainbow()
                time.sleep(freq)
        self.turnOff()

    def pumpVolume(self, volume_mL, rgb=None):
        pumpRate = 100
        timeToPump = volume_mL/(pumpRate/60)
        self.pumpAtFor(pumpRate, timeToPump, rgb=rgb)

    def turnOff(self):
        self.pumpAt(0)

    def release(self):
        self._motor.throttle = None

    def unrelease(self):
        self._motor.throttle = 0