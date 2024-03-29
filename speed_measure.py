from micropython import const
from machine import Pin, Timer
import time


# Useful calculators for working with Tachometer code:
#   - https://www.sensorsone.com/period-to-frequency-calculator/
#   - https://www.sensorsone.com/frequency-to-period-calculator/

class Tachometer:
    """
    Measure RPM via a logical (1/0) sensor.
    Any type of logical sensor will do.
    """

    RESOLUTION: int = const(1000)
    """sampling time. Max RPS is half of this"""
    TOO_SLOW_SECONDS: int = const(20)
    """after this number of seconds with no hits, the RPM will be considered 0"""

    def __init__(self, pin) -> None:
        """
        :param pin: pin number of sensor input
        """
        super().__init__()
        self.pin = Pin(pin, Pin.IN)

        self.hitsSinceLastHigh = 0
        self.cycleTime = 0.0
        """in seconds"""
        self.lastReading = 0
        timer = Timer()
        timer.init(freq=Tachometer.RESOLUTION, mode=Timer.PERIODIC, callback=self.calcRPM)

    def calcRPM(self, timer):
        current_value = self.pin.value()
        if current_value != self.lastReading and current_value == 1:
            self.cycleTime = self.hitsSinceLastHigh / Tachometer.RESOLUTION
            self.hitsSinceLastHigh = 0
        else:
            self.hitsSinceLastHigh += 1

        if self.hitsSinceLastHigh > Tachometer.TOO_SLOW_SECONDS * Tachometer.RESOLUTION:
            self.cycleTime = 0
        self.lastReading = current_value

    def get_current_rpm(self):
        return 60 / self.cycleTime if self.cycleTime != 0 else 0

    def get_current_cycle_time(self):
        """
        :returns: cycle time, or zero if too long (e.g. measured object is stopped) or unknown
        """
        return self.cycleTime
