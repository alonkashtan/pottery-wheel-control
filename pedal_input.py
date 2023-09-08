from machine import Pin, ADC
from config import Config


class PedalInput:
    def __init__(self, pin) -> None:
        super().__init__()
        self._adc = ADC(Pin(pin))

    def get_pedal_percentage(self) -> float:
        pot_value = self.get_pot_value()
        if pot_value < Config.PEDAL_MIN_VALUE:
            pot_value = Config.PEDAL_MIN_VALUE
        if pot_value > Config.PEDAL_MAX_VALUE:
            pot_value = Config.PEDAL_MAX_VALUE
        return 100 * (pot_value - Config.PEDAL_MIN_VALUE) / (Config.PEDAL_MAX_VALUE - Config.PEDAL_MIN_VALUE)

    def get_pot_value(self):
        return self._adc.read_u16()
