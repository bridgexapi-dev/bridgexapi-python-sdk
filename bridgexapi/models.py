from dataclasses import dataclass, asdict
from typing import Optional, List, Any


@dataclass(slots=True)
class SMSMessageStatus:
    bx_message_id: Optional[str]
    msisdn: str
    status: str

    @classmethod
    def from_dict(cls, data: dict) -> "SMSMessageStatus":
        return cls(
            bx_message_id=data.get("bx_message_id"),
            msisdn=str(data.get("msisdn", "")),
            status=str(data.get("status", "")),
        )

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(slots=True)
class SMSBatchResponse:
    status: str
    message: str
    order_id: Optional[int]
    route_id: int
    count: int
    messages: List[SMSMessageStatus]
    cost: Optional[float]
    balance_after: Optional[float]
    raw: dict[str, Any]

    @classmethod
    def from_dict(cls, data: dict) -> "SMSBatchResponse":
        return cls(
            status=str(data.get("status", "")),
            message=str(data.get("message", "")),
            order_id=data.get("order_id"),
            route_id=int(data.get("route_id", 0)),
            count=int(data.get("count", 0)),
            messages=[SMSMessageStatus.from_dict(x) for x in data.get("messages", [])],
            cost=float(data["cost"]) if data.get("cost") is not None else None,
            balance_after=float(data["balance_after"]) if data.get("balance_after") is not None else None,
            raw=data,
        )

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "message": self.message,
            "order_id": self.order_id,
            "route_id": self.route_id,
            "count": self.count,
            "messages": [m.to_dict() for m in self.messages],
            "cost": self.cost,
            "balance_after": self.balance_after,
            "raw": self.raw,
        }


@dataclass(slots=True)
class EstimateResponse:
    status: str
    message: str
    route_id: int
    count: int
    estimated_cost: float
    currency: str
    balance: float
    sufficient_balance: bool
    sandbox: bool
    raw: dict[str, Any]

    @classmethod
    def from_dict(cls, data: dict) -> "EstimateResponse":
        return cls(
            status=str(data.get("status", "")),
            message=str(data.get("message", "")),
            route_id=int(data.get("route_id", 0)),
            count=int(data.get("count", 0)),
            estimated_cost=float(data.get("estimated_cost", 0.0)),
            currency=str(data.get("currency", "")),
            balance=float(data.get("balance", 0.0)),
            sufficient_balance=bool(data.get("sufficient_balance", False)),
            sandbox=bool(data.get("sandbox", False)),
            raw=data,
        )

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(slots=True)
class BalanceResponse:
    status: str
    balance: float
    currency: str
    sandbox: bool
    username: str
    raw: dict[str, Any]

    @classmethod
    def from_dict(cls, data: dict) -> "BalanceResponse":
        return cls(
            status=str(data.get("status", "")),
            balance=float(data.get("balance", 0.0)),
            currency=str(data.get("currency", "")),
            sandbox=bool(data.get("sandbox", False)),
            username=str(data.get("username", "")),
            raw=data,
        )

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(slots=True)
class DLRMessage:
    bx_message_id: str
    msisdn: str
    status: str
    route_id: Optional[int]
    sms_order_id: int
    created_at: str
    error: Optional[str]
    raw: dict[str, Any]

    @classmethod
    def from_dict(cls, data: dict) -> "DLRMessage":
        return cls(
            bx_message_id=str(data.get("bx_message_id", "")),
            msisdn=str(data.get("msisdn", "")),
            status=str(data.get("status", "")),
            route_id=int(data["route_id"]) if data.get("route_id") is not None else None,
            sms_order_id=int(data.get("sms_order_id", 0)),
            created_at=str(data.get("created_at", "")),
            error=data.get("error"),
            raw=data,
        )

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(slots=True)
class DLRListResponse:
    total: int
    skip: int
    limit: int
    messages: List[DLRMessage]
    raw: dict[str, Any]

    @classmethod
    def from_dict(cls, data: dict) -> "DLRListResponse":
        return cls(
            total=int(data.get("total", 0)),
            skip=int(data.get("skip", 0)),
            limit=int(data.get("limit", 0)),
            messages=[DLRMessage.from_dict(x) for x in data.get("messages", [])],
            raw=data,
        )

    def to_dict(self) -> dict:
        return {
            "total": self.total,
            "skip": self.skip,
            "limit": self.limit,
            "messages": [m.to_dict() for m in self.messages],
            "raw": self.raw,
        }


@dataclass(slots=True)
class ActivitySummary:
    total_requests: int
    requests_today: int
    success_requests: int
    error_requests: int
    success_rate: float
    average_latency_ms: int
    active_api_keys: int
    recent_errors_24h: int

    @classmethod
    def from_dict(cls, data: dict) -> "ActivitySummary":
        return cls(
            total_requests=int(data.get("total_requests", 0)),
            requests_today=int(data.get("requests_today", 0)),
            success_requests=int(data.get("success_requests", 0)),
            error_requests=int(data.get("error_requests", 0)),
            success_rate=float(data.get("success_rate", 0.0)),
            average_latency_ms=int(data.get("average_latency_ms", 0)),
            active_api_keys=int(data.get("active_api_keys", 0)),
            recent_errors_24h=int(data.get("recent_errors_24h", 0)),
        )

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(slots=True)
class ActivitySummaryResponse:
    status: str
    summary: ActivitySummary
    raw: dict[str, Any]

    @classmethod
    def from_dict(cls, data: dict) -> "ActivitySummaryResponse":
        return cls(
            status=str(data.get("status", "")),
            summary=ActivitySummary.from_dict(data.get("summary", {})),
            raw=data,
        )

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "summary": self.summary.to_dict(),
            "raw": self.raw,
        }


@dataclass(slots=True)
class ActivityLogEntry:
    id: int
    timestamp: str
    endpoint: str
    method: str
    status_code: int
    latency_ms: Optional[int]
    ip_address: Optional[str]
    route_id: Optional[str]

    @classmethod
    def from_dict(cls, data: dict) -> "ActivityLogEntry":
        return cls(
            id=int(data.get("id", 0)),
            timestamp=str(data.get("timestamp", "")),
            endpoint=str(data.get("endpoint", "")),
            method=str(data.get("method", "")),
            status_code=int(data.get("status_code", 0)),
            latency_ms=int(data["latency_ms"]) if data.get("latency_ms") is not None else None,
            ip_address=data.get("ip_address"),
            route_id=data.get("route_id"),
        )

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(slots=True)
class ActivityLogsResponse:
    status: str
    page: int
    limit: int
    total: int
    logs: List[ActivityLogEntry]
    raw: dict[str, Any]

    @classmethod
    def from_dict(cls, data: dict) -> "ActivityLogsResponse":
        return cls(
            status=str(data.get("status", "")),
            page=int(data.get("page", 0)),
            limit=int(data.get("limit", 0)),
            total=int(data.get("total", 0)),
            logs=[ActivityLogEntry.from_dict(x) for x in data.get("logs", [])],
            raw=data,
        )

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "page": self.page,
            "limit": self.limit,
            "total": self.total,
            "logs": [x.to_dict() for x in self.logs],
            "raw": self.raw,
        }


@dataclass(slots=True)
class ActivityUsageDay:
    date: str
    total: int
    success: int
    errors: int
    average_latency_ms: int

    @classmethod
    def from_dict(cls, data: dict) -> "ActivityUsageDay":
        return cls(
            date=str(data.get("date", "")),
            total=int(data.get("total", 0)),
            success=int(data.get("success", 0)),
            errors=int(data.get("errors", 0)),
            average_latency_ms=int(data.get("average_latency_ms", 0)),
        )

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(slots=True)
class ActivityUsageResponse:
    status: str
    usage: List[ActivityUsageDay]
    raw: dict[str, Any]

    @classmethod
    def from_dict(cls, data: dict) -> "ActivityUsageResponse":
        return cls(
            status=str(data.get("status", "")),
            usage=[ActivityUsageDay.from_dict(x) for x in data.get("usage", [])],
            raw=data,
        )

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "usage": [x.to_dict() for x in self.usage],
            "raw": self.raw,
        }


@dataclass(slots=True)
class EndpointBreakdownEntry:
    endpoint: str
    method: str
    requests: int
    success_requests: int
    error_requests: int
    average_latency_ms: int

    @classmethod
    def from_dict(cls, data: dict) -> "EndpointBreakdownEntry":
        return cls(
            endpoint=str(data.get("endpoint", "")),
            method=str(data.get("method", "")),
            requests=int(data.get("requests", 0)),
            success_requests=int(data.get("success_requests", 0)),
            error_requests=int(data.get("error_requests", 0)),
            average_latency_ms=int(data.get("average_latency_ms", 0)),
        )

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(slots=True)
class EndpointBreakdownResponse:
    status: str
    endpoints: List[EndpointBreakdownEntry]
    raw: dict[str, Any]

    @classmethod
    def from_dict(cls, data: dict) -> "EndpointBreakdownResponse":
        return cls(
            status=str(data.get("status", "")),
            endpoints=[EndpointBreakdownEntry.from_dict(x) for x in data.get("endpoints", [])],
            raw=data,
        )

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "endpoints": [x.to_dict() for x in self.endpoints],
            "raw": self.raw,
        }