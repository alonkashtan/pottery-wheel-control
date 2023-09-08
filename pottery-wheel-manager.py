from micropython import const
from machine import Pin

from libs.PID import PID

from config import Config
from display import Display
from on_off_switch import OnOffSwitch
from pedal_input import PedalInput
from rotary import Rotary
from speed_measure import Tachometer
from speed_control import SpeedControl


class PotteryWheelManager:
    STOPPED_HOLD_STATE = const("STOPPED_HOLD")  # when first stopping, we stop motor and wait for safety conditions
    STOPPED_WAIT_STATE = const("STOPPED_WAIT")  # once safety conditions are met we wait for indication to start running
    RUNNING_STATE = const("RUNNING")

    def __init__(self, pedal_input: PedalInput, main_switch: OnOffSwitch, tachometer: Tachometer,
                 speed_control: SpeedControl, display: Display, rotary: Rotary) -> None:
        super().__init__()

        self.pedal_input = pedal_input
        self.main_switch = main_switch
        self.tachometer = tachometer
        self.speed_control = speed_control
        self.display = display
        self.rotary = rotary
        self.rotary.add_handler(self.create_rotary_event_handler())

        self._state = self.STOPPED_HOLD_STATE
        self._maxRpm = Config.DEFAULT_MAX_RPM

    def create_rotary_event_handler(self):
        """create a callback with no "self" parameter, so it can be passed as a handler"""
        def event_handler(event_type):
            if event_type == Rotary.ROT_CW:
                self._maxRpm = min(self._maxRpm + 1, Config.MAX_SUPPORTED_RPM)
            elif event_type == Rotary.ROT_CCW:
                self._maxRpm = min(self._maxRpm - 1, Config.MAX_SUPPORTED_RPM)
            elif event_type == Rotary.SW_PRESS:
                print('PRESS')
            elif event_type == Rotary.SW_RELEASE:
                print('RELEASE')

        return event_handler

    def loop(self):
        percentage = self.pedal_input.get_pedal_percentage()
        current_speed = self.tachometer.get_current_rpm()

        if self._state == self.STOPPED_HOLD_STATE:
            # make sure we are switched off
            self.main_switch.switch_off()
            self.speed_control.set_speed(0)
            if percentage == 0:
                self._state = self.STOPPED_WAIT_STATE

        elif self._state == self.STOPPED_WAIT_STATE:
            # if we made it here, we are already giving stop signals

            if percentage > 0:  # This indicates we need to start running
                self._state = self._state = self.RUNNING_STATE

        elif self._state == self.RUNNING_STATE:
            self.main_switch.switch_on()
