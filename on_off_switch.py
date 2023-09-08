from machine import Pin


class OnOffSwitch:
    """Control an on/off pin"""

    def __init__(self, pin) -> None:
        super().__init__()

        self._pin = Pin(pin, Pin.IN)

    def switch_on(self):
        self._pin.value(1)

    def switch_off(self):
        self._pin.value(0)

