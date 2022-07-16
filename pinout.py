from micropython import const


class Pinout:
    DISPLAY_SDA = const(4)  # I2C0
    DISPLAY_SCL = const(5)

    ENCODER_A = const(16)
    ENCODER_B = const(17)
    ENCODER_BUTTON = const(18)

    LIGHT_SENSOR = const(22)
