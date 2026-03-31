class BridgeXAPIError(Exception):
    """Base exception for all BridgeXAPI SDK errors."""


class ApiRequestError(BridgeXAPIError):
    """Generic API request error."""


class AuthenticationError(ApiRequestError):
    """Missing, invalid, or inactive API key."""


class ValidationError(ApiRequestError):
    """Payload validation failed."""


class InvalidRouteError(ValidationError):
    """Invalid route_id supplied."""


class UnauthorizedRouteError(ApiRequestError):
    """User is not allowed to use the selected route."""


class InsufficientBalanceError(ApiRequestError):
    """User balance is too low for this request."""


class VendorSendError(ApiRequestError):
    """Vendor gateway failed to accept the SMS request."""


class InvalidNumberError(ValidationError):
    """Phone number format is invalid."""


class MixedCountryBatchError(ValidationError):
    """Numbers from multiple countries were provided in one request."""


class MessageTooLongError(ValidationError):
    """Message exceeds the maximum allowed length."""


class UnicodeNotAllowedError(ValidationError):
    """Message contains non-ASCII characters."""


class InvalidCallerIDError(ValidationError):
    """Caller ID is invalid."""