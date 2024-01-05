from machine import Pin, PWM

from speed_control import SpeedControl
from config import Config


class ServoSpeedControl(SpeedControl):
    def __init__(self, pin) -> None:
        super().__init__()
        self._pmw = PWM(Pin(pin))
        self._pmw.freq(50)

    def set_speed(self, percent):
        required_value = round(percent * (Config.SERVO_MAX_VALUE - Config.SERVO_MIN_VALUE) / 100) + \
                         Config.SERVO_MIN_VALUE
        self.set_servo_value(required_value)

    def set_servo_value(self, required_value):
        self._pmw.duty_ns(required_value)
