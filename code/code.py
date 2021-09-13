import time
import board
from SimpleButton import SimpleButton
from RGBButton import RGBButton
from ShotStepper import ShotStepper
from PumpMotor import PumpMotor
from SimpleSwitch import SimpleSwitch
from AttachmentManager import AttachmentManager
from RunMode import RunMode

enable = True

if not enable:
    while True:
        print("Code is disabled, please set 'enable' to True to run")
        time.sleep(60)


def switchMode():
    try:
        run_mode.advanceMode()
    except:
        rgb_button.displayColor(rgb_button.Color.ORANGE)
        quit
    rgb_button.displayColor(mode_colors[run_mode.getMode()])
    credit_attachment.led_backpack.flashText(RunMode.ModeNames[run_mode.getMode()]) if attach_manager.hasAttachment(coin_op_type)

def checkInputs():
    if not run_mode.isAsleep():
        rgb_button.displayColor(mode_colors[run_mode.getMode()])
        credit_attachment.setCreditsInserted() if attach_manager.hasAttachment(coin_op_type)
        if shot_stepper.isPastReleaseTimeout():
            run_mode.setToSleepMode()
            shot_stepper.release()
            if attach_manager.hasAttachment(coin_op_type):
                credit_attachment.setSleep()
                credit_attachment.setLEDBrightness(0.5)
        if motor_button.isPushed():
            moveGlassesCheck()
        elif prime_switch.isSwitched():
            runPriming()
        elif rgb_button.isPushed():
            if rgb_button.isPushedFor(2):
                switchMode()
                time.sleep(0.75)
                return
            else:
                rgb_button.displayColor(inprogress_color)
                runModeCheck()
                rgb_button.displayColor(mode_colors[run_mode.getMode()])
    else:
        rgb_button.displayColor(rgb_button.Color.WHITE)
        if rgb_button.isPushed():
            run_mode.wakeUp()
            shot_stepper.updateReleaseTimeout()
            rgb_button.displayColor(mode_colors[run_mode.getMode()])
            time.sleep(0.75)
        
    if 

def runModeCheck():
    mode = run_mode.getMode()
    if mode == 0:
        runSingleMode()
    elif mode == 1:
        runFullMode()
    elif mode == 2:
        runPartyMode()

def moveGlassesCheck():
    if motor_button.isPushedFor(2):
        credit_attachment.setFree() if attach_manager.hasAttachment(coin_op_type)
        while motor_button.isPushed():
            shot_stepper.release()
            time.sleep(0.01)
        shot_stepper.unrelease()
    else:
        credit_attachment.setMoving() if attach_manager.hasAttachment(coin_op_type)
        shot_stepper.moveToNextGlass()

def runPriming():
    while prime_switch.isSwitched():
        credit_attachment.setPouring() if attach_manager.hasAttachment(coin_op_type)
        pump_motor.pumpAt(pump_motor.max_speed)
        time.sleep(0.01)
    pump_motor.turnOff()
    time.sleep(0.25)

def runSingleMode():
    credit_attachment.setMoving() if attach_manager.hasAttachment(coin_op_type)
    shot_stepper.moveToNextGlass()
    shot_stepper.moveToNextGlass()
    credit_attachment.setPouring() if attach_manager.hasAttachment(coin_op_type)
    pump_motor.pumpVolume(44)
    time.sleep(0.5)
    credit_attachment.setMoving() if attach_manager.hasAttachment(coin_op_type)
    shot_stepper.moveToNextGlass()
    shot_stepper.moveToNextGlass()
    credit_attachment.flashDone() if attach_manager.hasAttachment(coin_op_type)

def runFullMode():
    for glass in range(shot_stepper.num_glasses):
        credit_attachment.setMoving() if attach_manager.hasAttachment(coin_op_type)
        shot_stepper.moveToNextGlass()
        time.sleep(0.25)
        credit_attachment.setPouring() if attach_manager.hasAttachment(coin_op_type)
        pump_motor.pumpVolume(44)
        time.sleep(0.25)
    credit_attachment.flashDone() if attach_manager.hasAttachment(coin_op_type)
    time.sleep(0.5)


def runPartyMode():
    direction = 0
    for movement in range(5):
        credit_attachment.setMoving() if attach_manager.hasAttachment(coin_op_type)
        shot_stepper.moveToRandomGlass(reverse_direction=direction)
        direction = (direction + 1) % 2
        time.sleep(1)
    for cycle_num in range(3):
        credit_attachment.flashDone() if attach_manager.hasAttachment(coin_op_type)
        rgb_button.displayColor(rgb_button.Color.LIGHT_BLUE)
        time.sleep(0.5)
        rgb_button.displayColor(rgb_button.Color.AQUA)
        time.sleep(0.5)

rgb_button = RGBButton(board.A1, board.D9, board.D10, board.D11)
motor_button = SimpleButton(board.A2)
prime_switch = SimpleSwitch(board.D6)
shot_stepper = ShotStepper(2)
pump_motor = PumpMotor(2)
attach_manager = AttachmentManager()
coin_op_type = AttachmentManager.Types["COIN_OP"]
if attach_manager.hasAttachment(coin_op_type):
    credit_attachment = CreditAttachment()
run_mode = RunMode(0)
red = rgb_button.Color.RED
green = rgb_button.Color.GREEN
blue = rgb_button.Color.BLUE
mode_colors = [red, green, blue]
inprogress_color = rgb_button.Color.PURPLE

credit_attachment.led_backpack.marqueeShotBotName() if AttachmentManager.hasAttachment(coin_op_type)

while True:
    checkInputs()
    credit_attachment.led_backpack.checkFlashText()
    time.sleep(0.01)