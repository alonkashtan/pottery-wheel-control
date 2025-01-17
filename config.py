from micropython import const


class Config:
    SERVO_MIN_VALUE = const(400000)
    SERVO_MAX_VALUE = const(1330000)

    PEDAL_MIN_VALUE = const(4000)
    PEDAL_MAX_VALUE = const(42000)

    ON_OFF_SERVO_ON_VALUE = const(1935000)
    ON_OFF_SERVO_OFF_VALUE = const(1010000)

    MAX_SUPPORTED_RPM = const(300)
    DEFAULT_MAX_RPM = const(150)
    SUPPORTED_RPM_STATE = [1, 50, 100, 150, 200, 250, MAX_SUPPORTED_RPM]
