import time
import board
from base.simple_button import SimpleButton
from base.rgb_Button import RGBButton
from base.shot_stepper import ShotStepper
from base.pump_motor import PumpMotor
from base.simple_switch import SimpleSwitch
from base.run_mode import RunMode
from attachments.attachment_manager import AttachmentManager

rgb_button = RGBButton(board.A1, board.D9, board.D10, board.D11)
motor_button = SimpleButton(board.A2)
prime_switch = SimpleSwitch(board.D6)
shot_stepper = ShotStepper(2)
pump_motor = PumpMotor(2)
attach_manager = AttachmentManager()
coin_op_type = AttachmentManager.Types["COIN_OP"]
twitch_bot_type = AttachmentManager.Types["TWITCH_BOT"]
if attach_manager.hasAttachment(coin_op_type):
    from credit_attachment import CreditAttachment
    credit_attachment = CreditAttachment()
elif attach_manager.hasAttachment(twitch_bot_type):
    # initialize twitch-bot type
    pass
run_mode = RunMode(0)
red = rgb_button.Color.RED
green = rgb_button.Color.GREEN
blue = rgb_button.Color.BLUE
mode_colors = [red, green, blue]
inprogress_color = rgb_button.Color.PURPLE

credit_attachment.led_backpack.marqueeShotBotName() if attach_manager.hasAttachment(coin_op_type)