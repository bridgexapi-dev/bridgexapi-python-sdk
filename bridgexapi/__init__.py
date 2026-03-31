from .client import BridgeXAPI
from .version import __version__
from .routes import Route

# Core models
from .models import (
    SMSBatchResponse,
    SMSMessageStatus,
    EstimateResponse,
    BalanceResponse,
    DLRMessage,
    DLRListResponse,
    ActivitySummary,
    ActivitySummaryResponse,
    ActivityLogEntry,
    ActivityLogsResponse,
    ActivityUsageDay,
    ActivityUsageResponse,
    EndpointBreakdownEntry,
    EndpointBreakdownResponse,
)

# Exceptions
from .exceptions import (
    BridgeXAPIError,
    ApiRequestError,
    AuthenticationError,
    ValidationError,
    InvalidRouteError,
    UnauthorizedRouteError,
    InsufficientBalanceError,
    VendorSendError,
    InvalidNumberError,
    MixedCountryBatchError,
    MessageTooLongError,
    UnicodeNotAllowedError,
    InvalidCallerIDError,
)

__all__ = [
    # client
    "BridgeXAPI",
    "__version__",

    # routing
    "Route",

    # core models
    "SMSBatchResponse",
    "SMSMessageStatus",

    # new models
    "EstimateResponse",
    "BalanceResponse",
    "DLRMessage",
    "DLRListResponse",

    # activity models
    "ActivitySummary",
    "ActivitySummaryResponse",
    "ActivityLogEntry",
    "ActivityLogsResponse",
    "ActivityUsageDay",
    "ActivityUsageResponse",
    "EndpointBreakdownEntry",
    "EndpointBreakdownResponse",

    # exceptions
    "BridgeXAPIError",
    "ApiRequestError",
    "AuthenticationError",
    "ValidationError",
    "InvalidRouteError",
    "UnauthorizedRouteError",
    "InsufficientBalanceError",
    "VendorSendError",
    "InvalidNumberError",
    "MixedCountryBatchError",
    "MessageTooLongError",
    "UnicodeNotAllowedError",
    "InvalidCallerIDError",
]