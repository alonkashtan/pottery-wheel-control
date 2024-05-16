from display import Display
from pinout import Pinout
from rotary import Rotary
from speed_measure import Tachometer
from pedal_input import PedalInput
from servo_speed_control import ServoSpeedControl
from on_off_switch import OnOffSwitch, ServoOnOffSwitch
from pottery_wheel_manager import PotteryWheelManager

pedal_input = PedalInput(Pinout.PEDAL_POT)
main_switch = ServoOnOffSwitch(Pinout.MAIN_SWITCH)
speed_measure = Tachometer(Pinout.LIGHT_SENSOR)
speed_control = ServoSpeedControl(Pinout.SERVO)
display = Display(Pinout.DISPLAY_SDA, Pinout.DISPLAY_SCL)
rotary = Rotary(Pinout.ENCODER_A, Pinout.ENCODER_B, Pinout.ENCODER_BUTTON)
wheel_manager = PotteryWheelManager(pedal_input, main_switch, speed_measure, speed_control, display, rotary)

while True:
    wheel_manager.loop()

# val = 150
#
#
# def rotary_changed(change):
#     global val, servo
#     if change == Rotary.ROT_CW:
#         val = val + 1
#         print(val)
#     elif change == Rotary.ROT_CCW:
#         val = val - 1
#         print(val)
#     elif change == Rotary.SW_PRESS:
#         print('PRESS')
#     elif change == Rotary.SW_RELEASE:
#         print('RELEASE')
#
#     # val = max(Config.PEDAL_MIN_VALUE, min(Config.PEDAL_MAX_VALUE, val))
#     # percent = 100*(val - Config.PEDAL_MIN_VALUE) / (Config.PEDAL_MAX_VALUE - Config.PEDAL_MIN_VALUE)
#     # servo.set_speed(percent)
#
#
# rotary.add_handler(rotary_changed)

#
# while True:
#     pot_value = pedal_input.get_pot_value()
#     percentage = pedal_input.get_pedal_percentage()
#     # print(str(pot_value) + " - " + str(percentage))
#     servo.set_speed(percentage)
#     utime.sleep(0.1)
#     display.current_speed = round(speedMeasure.get_current_rpm())
#     display.requested_speed = percentage * Config.MAX_SUPPORTED_RPM / 100
#     display.max_speed = val
