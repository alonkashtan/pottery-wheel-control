import time
from micropython import const
from libs.lcd1602 import LCD1602
from machine import I2C, Pin

I2C_ADDR = const(0X3E)
I2C_NUM_ROWS = const(2)
I2C_NUM_COLS = const(16)


class Display:
    """Display speed data on a Seeedstudio 16X2 display"""
    def __init__(self, sda_pin, scl_pin, initial_max_speed=0, initial_curr_speed=0, initial_requested_speed=0) -> None:
        super().__init__()
        sda = Pin(sda_pin)
        scl = Pin(scl_pin)
        # i2c = machine.I2C(0, sda=sda, scl=scl, freq=400000)

        i2c = I2C(0, scl=scl, sda=sda, freq=400000)
        self._display = LCD1602(i2c, 2, 16)
        self._display.clear()
        self._maxSpeed = initial_max_speed
        self._currentSpeed = initial_curr_speed
        self._requestedSpeed = initial_requested_speed
        self._refresh_text()

    def _refresh_text(self):
        self._display.home()
        self._display.print("Max ")
        self._display.print("{:>3}".format(str(self.max_speed)))
        self._display.print("  Set ")
        self._display.print("{:>3}".format(str(self.requested_speed)))
        self._display.setCursor(0, 1)
        self._display.print("Current ")
        self._display.print("{:>3}".format(str(self.current_speed)))

    @staticmethod
    def _validate_speed(value):
        if value < 0 or value > 999:
            raise Exception("Speed must be in [0-999] (" + str(value) + " given)")

    @property
    def max_speed(self):
        return self._maxSpeed

    @max_speed.setter
    def max_speed(self, value):
        self._validate_speed(value)
        self._maxSpeed = value
        self._refresh_text()

    @property
    def current_speed(self):
        return self._currentSpeed

    @current_speed.setter
    def current_speed(self, value):
        # self._validate_speed(value)
        self._currentSpeed = value
        self._refresh_text()

    @property
    def requested_speed(self):
        return self._requestedSpeed

    @requested_speed.setter
    def requested_speed(self, value):
        self._validate_speed(value)
        self._requestedSpeed = value
        self._refresh_text()

    def set_is_on(self, is_on: bool):
        if is_on:
            self._display.display()
        else:
            self._display.no_display()
