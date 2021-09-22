import time
from base.simple_button import SimpleButton
from base.rgb_Button import RGBButton
from base.shot_stepper import ShotStepper
from base.pump_motor import PumpMotor
from base.simple_switch import SimpleSwitch
from base.run_mode import RunMode
from attachments.attachment_manager import AttachmentManager

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
        if attach_manager.hasAttachment(coin_op_type):
            credit_attachment.setLEDBrightness(1)
            credit_attachment.setCreditsInserted()
            credit_attachment.checkCoinInserted()
        if shot_stepper.isPastReleaseTimeout():
            run_mode.setToSleepMode()
            shot_stepper.release()
            if attach_manager.hasAttachment(coin_op_type):
                credit_attachment.setSleep()
                credit_attachment.setLEDBrightness(0.5)
        elif motor_button.isPushed():
            moveGlassesCheck()
        elif prime_switch.isSwitched():
            runPriming()
        elif rgb_button.isPushed():
            if rgb_button.isPushedFor(2):
                switchMode()
                time.sleep(0.75)
                return
            else:
                if attach_manager.hasAttachment(coin_op_type):
                    if not credit_attachment.hasEnoughCredits(CreditAttachment.ModeCost[run_mode.getMode()]):
                        credit_attachment.led_backpack.flashText("MORE", 1)
                        time.sleep(1)
                        return
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
    if attach_manager.hasAttachment(coin_op_type):
        credit_attachment.spendCredit()
        credit_attachment.setMoving()
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
    credit_attachment.spendCredit(4) if attach_manager.hasAttachment(coin_op_type)
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
    credit_attachment.spendCredit(1) if attach_manager.hasAttachment(coin_op_type)
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

def runShotBot():
    while True:
        checkInputs(device_map)
        credit_attachment.led_backpack.checkFlashText() if attach_manager.hasAttachment(coin_op_type)
        time.sleep(0.01)