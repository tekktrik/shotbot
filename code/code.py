import time
import board
from base.simple_button import SimpleButton
from base.rgb_Button import RGBButton
from base.shot_stepper import ShotStepper
from base.pump_motor import PumpMotor
from base.simple_switch import SimpleSwitch
from base.run_mode import RunMode
from attachments.attachment_manager import AttachmentManager
from base.device_map import DeviceMap

device_map = DeviceMap()

device_map.addDevice("rgb_button", RGBButton(board.A1, board.D9, board.D10, board.D11))
device_map.addDevice("motor_button", SimpleButton(board.A2))
device_map.addDevice("prime_switch", SimpleSwitch(board.D6))
device_map.addDevice("shot_stepper", ShotStepper(2))
device_map.addDevice("pump_motor", PumpMotor(2))

device_map.addAttachmentManager(attach_manager)

device_map.addRunMode(RunMode(0))
device_map.addModeColors([rgb_button.Color.RED, rgb_button.Color.GREEN, rgb_button.Color.BLUE])
device_map.addInProgressColor(rgb_button.Color.PURPLE)

attach_manager = AttachmentManager()
if attach_manager.hasAttachment(AttachmentManager.Types["COIN_OP"]):
    from credit_attachment import CreditAttachment
    device_map.addDevice("credit_attachment", CreditAttachment())
elif attach_manager.hasAttachment(AttachmentManager.Types["TWITCH_BOT"]):
    # initialize twitch-bot type
    pass
else:
    from base_sequence import ShotBotSequence
    
device_map.getDevice("credit_attachment").led_backpack.marqueeShotBotName() if attach_manager.hasAttachment(coin_op_type)

seq = ShotBotSequence(device_map)
seq.run()