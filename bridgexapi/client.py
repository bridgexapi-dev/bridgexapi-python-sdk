from typing import Iterable, Optional, Any

import requests

from .exceptions import (
    ApiRequestError,
    AuthenticationError,
    InsufficientBalanceError,
    InvalidRouteError,
    UnauthorizedRouteError,
    ValidationError,
    VendorSendError,
)
from .models import (
    SMSBatchResponse,
    EstimateResponse,
    BalanceResponse,
    DLRMessage,
    DLRListResponse,
    ActivitySummaryResponse,
    ActivityLogsResponse,
    ActivityUsageResponse,
    EndpointBreakdownResponse,
)
from .validators import (
    validate_route_id,
    validate_caller_id,
    validate_numbers,
    validate_message,
)


class BridgeXAPI:
    """
    Official sync client for the BridgeXAPI developer API.

    This client exposes the programmable routing surface:
    - send SMS
    - estimate cost
    - get balance
    - retrieve delivery reports
    - inspect developer activity
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = "https://hi.bridgexapi.io",
        timeout: float = 30.0,
        session: Optional[requests.Session] = None,
    ) -> None:
        if not api_key or not isinstance(api_key, str):
            raise AuthenticationError("api_key is required.")

        self.api_key = api_key.strip()
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = session or requests.Session()

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "X-API-KEY": self.api_key,
        }

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        response = self.session.request(
            method=method.upper(),
            url=f"{self.base_url}{path}",
            headers=self.headers,
            params=params,
            json=json,
            timeout=self.timeout,
        )

        data = self._decode_json(response)
        self._raise_for_error(response.status_code, data)
        return data

    def send_sms(
        self,
        *,
        route_id: int,
        caller_id: str,
        numbers: Iterable[str],
        message: str,
    ) -> SMSBatchResponse:
        payload = {
            "route_id": validate_route_id(route_id),
            "caller_id": validate_caller_id(caller_id),
            "numbers": validate_numbers(numbers),
            "message": validate_message(message),
        }

        data = self._request("POST", "/api/v1/send_sms", json=payload)
        return SMSBatchResponse.from_dict(data)

    def send_one(
        self,
        *,
        route_id: int,
        caller_id: str,
        number: str,
        message: str,
    ) -> SMSBatchResponse:
        return self.send_sms(
            route_id=route_id,
            caller_id=caller_id,
            numbers=[number],
            message=message,
        )

    def estimate(
        self,
        *,
        route_id: int,
        caller_id: str,
        numbers: Iterable[str],
        message: str,
    ) -> EstimateResponse:
        payload = {
            "route_id": validate_route_id(route_id),
            "caller_id": validate_caller_id(caller_id),
            "numbers": validate_numbers(numbers),
            "message": validate_message(message),
        }

        data = self._request("POST", "/api/v1/estimate", json=payload)
        return EstimateResponse.from_dict(data)

    def get_balance(self) -> BalanceResponse:
        data = self._request("GET", "/api/v1/balance")
        return BalanceResponse.from_dict(data)

    def list_dlr(
        self,
        *,
        limit: int = 50,
        skip: int = 0,
        status: Optional[str] = None,
        msisdn: Optional[str] = None,
        order_id: Optional[int] = None,
        route_id: Optional[int] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> DLRListResponse:
        params = {
            "limit": limit,
            "skip": skip,
            "status": status,
            "msisdn": msisdn,
            "order_id": order_id,
            "route_id": route_id,
            "from_date": from_date,
            "to_date": to_date,
        }
        params = {k: v for k, v in params.items() if v is not None}

        data = self._request("GET", "/api/v1/dlr", params=params)
        return DLRListResponse.from_dict(data)

    def get_dlr(self, bx_message_id: str) -> DLRMessage:
        if not bx_message_id or not isinstance(bx_message_id, str):
            raise ValidationError("bx_message_id is required.")

        data = self._request("GET", f"/api/v1/dlr/{bx_message_id.strip()}")
        return DLRMessage.from_dict(data)

    def get_order_dlr(
        self,
        order_id: int,
        *,
        limit: int = 500,
        skip: int = 0,
    ) -> DLRListResponse:
        if not isinstance(order_id, int) or order_id <= 0:
            raise ValidationError("order_id must be a positive integer.")

        data = self._request(
            "GET",
            f"/api/v1/orders/{order_id}/dlr",
            params={"limit": limit, "skip": skip},
        )
        return DLRListResponse.from_dict(data)

    def list_routes(self):
        data = self._request("GET", "/api/v1/routes")
        return data

    def get_route(self, route_id: int):
        route_id = validate_route_id(route_id)
        data = self._request("GET", f"/api/v1/routes/{route_id}")
        return data

    def get_route_pricing(self, route_id: int):
        route_id = validate_route_id(route_id)
        data = self._request("GET", f"/api/v1/routes/{route_id}/pricing")
        return data


    def get_activity_summary(self) -> ActivitySummaryResponse:
        data = self._request("GET", "/api/v1/activity/summary")
        return ActivitySummaryResponse.from_dict(data)

    def get_activity_logs(
        self,
        *,
        page: int = 1,
        limit: int = 20,
        endpoint: Optional[str] = None,
        method: Optional[str] = None,
        status_code: Optional[int] = None,
        route_id: Optional[str] = None,
    ) -> ActivityLogsResponse:
        params = {
            "page": page,
            "limit": limit,
            "endpoint": endpoint,
            "method": method,
            "status_code": status_code,
            "route_id": route_id,
        }
        params = {k: v for k, v in params.items() if v is not None}

        data = self._request("GET", "/api/v1/activity/logs", params=params)
        return ActivityLogsResponse.from_dict(data)

    def get_activity_usage(self, *, days: int = 7) -> ActivityUsageResponse:
        data = self._request("GET", "/api/v1/activity/usage", params={"days": days})
        return ActivityUsageResponse.from_dict(data)

    def get_activity_endpoints(self) -> EndpointBreakdownResponse:
        data = self._request("GET", "/api/v1/activity/endpoints")
        return EndpointBreakdownResponse.from_dict(data)

    def _decode_json(self, response: requests.Response) -> dict[str, Any]:
        try:
            return response.json()
        except ValueError as exc:
            raise ApiRequestError(
                f"BridgeXAPI returned a non-JSON response (status {response.status_code})."
            ) from exc

    def _raise_for_error(self, status_code: int, data: dict[str, Any]) -> None:
        if 200 <= status_code < 300:
            return

        detail = data.get("detail")

        if isinstance(detail, list):
            first = detail[0] if detail else {}
            msg = first.get("msg") or "Validation error."
            raise ValidationError(msg)

        if isinstance(detail, str):
            msg = detail.lower()

            if "missing api key" in msg or "invalid or inactive api key" in msg:
                raise AuthenticationError(detail)

            if "missing x-api-key header" in msg:
                raise AuthenticationError(detail)

            if "invalid route_id" in msg:
                raise InvalidRouteError(detail)

            if "you are not authorized for route" in msg:
                raise UnauthorizedRouteError(detail)

            if "not authorized for the casino route" in msg:
                raise UnauthorizedRouteError(detail)

            if "sender id not allowed for route 8" in msg:
                raise UnauthorizedRouteError(detail)

            if "insufficient balance" in msg:
                raise InsufficientBalanceError(detail)

            if "vendor send failed" in msg:
                raise VendorSendError(detail)

            if "pricing failed" in msg or "estimate failed" in msg:
                raise ValidationError(detail)

            if "dlr record not found" in msg:
                raise ApiRequestError(detail)

            raise ApiRequestError(detail)

        raise ApiRequestError(f"BridgeXAPI request failed with status {status_code}.")