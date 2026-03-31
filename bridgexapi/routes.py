from enum import IntEnum


class Route(IntEnum):
    """
    BridgeXAPI route identifiers.

    Public:
    - ROUTE_1 .. ROUTE_4

    Restricted:
    - CASINO = 5
    - ENTERPRISE_IGAMING = 7
    - ENTERPRISE_OTP = 8
    """

    ROUTE_1 = 1
    ROUTE_2 = 2
    ROUTE_3 = 3
    ROUTE_4 = 4
    CASINO = 5
    ENTERPRISE_IGAMING = 7
    ENTERPRISE_OTP = 8