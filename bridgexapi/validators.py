import re
from typing import Iterable, List

from .exceptions import (
    InvalidCallerIDError,
    InvalidNumberError,
    InvalidRouteError,
    MessageTooLongError,
    MixedCountryBatchError,
    UnicodeNotAllowedError,
)

VALID_ROUTES = {1, 2, 3, 4, 5, 7, 8}
NUMBER_RE = re.compile(r"^\d{10,15}$")


def normalize_number(number: str) -> str:
    """
    Normalize user input into BridgeXAPI format.
    Removes spaces, dashes, parentheses and other non-digits.
    """
    if not isinstance(number, str):
        raise InvalidNumberError("Phone number must be a string.")
    return re.sub(r"\D", "", number.strip())


def validate_route_id(route_id: int) -> int:
    if route_id not in VALID_ROUTES:
        raise InvalidRouteError("route_id must be one of: 1, 2, 3, 4, 5, 7, 8.")
    return route_id


def validate_caller_id(caller_id: str) -> str:
    if not isinstance(caller_id, str):
        raise InvalidCallerIDError("caller_id must be a string.")

    caller_id = caller_id.strip()

    if not (3 <= len(caller_id) <= 11):
        raise InvalidCallerIDError("caller_id must be between 3 and 11 characters.")

    return caller_id


def validate_message(message: str) -> str:
    if not isinstance(message, str):
        raise MessageTooLongError("message must be a string.")

    if len(message) > 158:
        raise MessageTooLongError("Message must contain at most 158 characters.")

    if not message.isascii():
        raise UnicodeNotAllowedError("Message must contain only ASCII characters.")

    return message


def validate_numbers(numbers: Iterable[str]) -> List[str]:
    numbers = list(numbers)

    if not numbers:
        raise InvalidNumberError("numbers must contain at least one phone number.")

    normalized = []

    for raw in numbers:
        if not isinstance(raw, str):
            raise InvalidNumberError("Each number must be a string.")

        if raw.strip().startswith("+"):
            raise InvalidNumberError("Number must not start with '+'.")

        cleaned = normalize_number(raw)

        if not NUMBER_RE.fullmatch(cleaned):
            raise InvalidNumberError("Each number must be 10 to 15 digits, digits only.")

        normalized.append(cleaned)

    validate_same_country(normalized)
    return normalized


def validate_same_country(numbers: List[str]) -> None:
    """
    BridgeXAPI business rule:
    all numbers in one request must belong to the same country.

    Current SDK heuristic:
    compare first 3, 2 or 1 digits against the first number.
    """
    if len(numbers) <= 1:
        return

    ref3, ref2, ref1 = numbers[0][:3], numbers[0][:2], numbers[0][:1]

    for number in numbers[1:]:
        cur3, cur2, cur1 = number[:3], number[:2], number[:1]
        if not (cur3 == ref3 or cur2 == ref2 or cur1 == ref1):
            raise MixedCountryBatchError(
                "All numbers in one request must belong to the same country."
            )