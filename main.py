import machine
import utime
import ustruct
import sys

from display import Display
from pinout import Pinout
from rotary import Rotary
from speed_measure import Tachometer
from pedal_input import PedalInput
from servo_speed_control import ServoSpeedControl
from config import Config

rotary = Rotary(Pinout.ENCODER_A, Pinout.ENCODER_B, Pinout.ENCODER_BUTTON)
val = Config.PEDAL_MIN_VALUE


def rotary_changed(change):
    global val, servo
    if change == Rotary.ROT_CW:
        val = val + 500
        print(val)
    elif change == Rotary.ROT_CCW:
        val = val - 500
        print(val)
    elif change == Rotary.SW_PRESS:
        print('PRESS')
    elif change == Rotary.SW_RELEASE:
        print('RELEASE')

    val = max(Config.PEDAL_MIN_VALUE, min(Config.PEDAL_MAX_VALUE, val))
    percent = 100*(val - Config.PEDAL_MIN_VALUE) / (Config.PEDAL_MAX_VALUE - Config.PEDAL_MIN_VALUE)
    servo.set_speed(percent)


rotary.add_handler(rotary_changed)
# display = Display(Pinout.DISPLAY_SDA, Pinout.DISPLAY_SCL)
# speedMeasure = Tachometer(Pinout.LIGHT_SENSOR)
pedal_input = PedalInput(Pinout.PEDAL_POT)
servo = ServoSpeedControl(Pinout.SERVO)

while True:
    # pot_value = pedal_input.get_pot_value()
    # percentage = pedal_input.get_pedal_percentage()
    # print(str(pot_value) + " - " + str(percentage))
    # servo.set_speed(percentage)
    utime.sleep(0.1)
    # display.current_speed = round(speedMeasure.get_current_rpm())
