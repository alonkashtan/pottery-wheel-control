from micropython import const


class Config:
    SERVO_MIN_VALUE = const(400000)  # TODO
    SERVO_MAX_VALUE = const(2400000)  # TODO

    PEDAL_MIN_VALUE = const(1000)  # TODO
    PEDAL_MAX_VALUE = const(60535)  # TODO

    MAX_SUPPORTED_RPM = const(250)
    DEFAULT_MAX_RPM = const(150)
    SUPPORTED_RPM_STATE = const([1, 50, 100, 150, 200, MAX_SUPPORTED_RPM])