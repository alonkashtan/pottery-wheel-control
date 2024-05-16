from machine import Pin, PWM
from config import Config


class OnOffSwitch:
    """Control an on/off pin"""


    def __init__(self, pin) -> None:
        super().__init__()

        self._pin = Pin(pin, Pin.OUT)


    def switch_on(self):
        self._pin.value(1)


    def switch_off(self):
        self._pin.value(0)


class ServoOnOffSwitch(OnOffSwitch):
    """Control an on/off pin using a servo"""


    def __init__(self, pin) -> None:
        super().__init__(pin)
        self._pmw = PWM(self._pin)
        self._pmw.freq(50)


    def switch_on(self):
        self._pmw.duty_ns(Config.ON_OFF_SERVO_ON_VALUE)


    def switch_off(self):
        self._pmw.duty_ns(Config.ON_OFF_SERVO_OFF_VALUE)
