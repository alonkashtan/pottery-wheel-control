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
        """
        :param pedal_input: input class for getting information about the pedal position
        :param main_switch: switch that turn off the main power to the motor
        :param tachometer: get the current rotation speed (of the wheel head)
        :param speed_control: a controller for controlling the motor speed
        :param display: text LCD display
        :param rotary: input device (rotary switch) for the user to interact with the system
        """
        super().__init__()

        self.pedal_input = pedal_input
        self.main_switch = main_switch
        self.tachometer = tachometer
        self.speed_control = speed_control
        self.display = display
        self.rotary = rotary
        self.rotary.add_handler(self.create_rotary_event_handler())

        self._lastState = ""
        self._state = self.STOPPED_HOLD_STATE
        self._maxRpm = Config.DEFAULT_MAX_RPM


    def create_rotary_event_handler(self):
        """create a callback with no "self" parameter, so it can be passed as a handler"""

        def find_next_supported_rpm():
            for i in Config.SUPPORTED_RPM_STATE:
                if i > self._maxRpm:
                    return i
            return Config.SUPPORTED_RPM_STATE[0]

        def event_handler(event_type):
            if event_type == Rotary.ROT_CW:
                self._maxRpm = min(self._maxRpm + 1, Config.MAX_SUPPORTED_RPM)
            elif event_type == Rotary.ROT_CCW:
                self._maxRpm = max(self._maxRpm - 1, 0)
            elif event_type == Rotary.SW_PRESS:
                print('PRESS')
            elif event_type == Rotary.SW_RELEASE:
                print('RELEASE')
                self._maxRpm = find_next_supported_rpm()

        return event_handler


    def loop(self):
        """A single loop. For running this you probably want to call this method repeatedly"""
        try:
            if self._state != self._lastState:
                print("State: " + self._state)
                self._lastState = self._state

            percentage = self.pedal_input.get_pedal_percentage()
            current_speed = self.tachometer.get_current_rpm()
            requested_rpm = 0

            if self._state == self.STOPPED_HOLD_STATE:
                # make sure we are switched off
                self.main_switch.switch_off()
                self.speed_control.set_speed(0)
                if percentage == 0:
                    # we exit this state only when the user moved the pedal to 0
                    # this will prevent accidents on startup or restarts
                    self._state = self.STOPPED_WAIT_STATE

            elif self._state == self.STOPPED_WAIT_STATE:
                # if we made it here, we are already giving stop signals. So all we need to do is wait for user

                if percentage > 0:  # This indicates we need to start running
                    self._state = self._state = self.RUNNING_STATE

            elif self._state == self.RUNNING_STATE:
                self.main_switch.switch_on()

                pedal_percentage = self.pedal_input.get_pedal_percentage()
                requested_rpm = pedal_percentage * self._maxRpm / 100
                requested_percentage = 100 * requested_rpm / Config.MAX_SUPPORTED_RPM
                self.speed_control.set_speed(requested_percentage)
                if pedal_percentage == 0:
                    self._state = self.STOPPED_HOLD_STATE

            self.display.current_speed = current_speed
            self.display.max_speed = self._maxRpm
            self.display.requested_speed = requested_rpm
        except Exception as e:
            self._state = self.STOPPED_HOLD_STATE
            print('Failure on main loop: ' + str(e))
