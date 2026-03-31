# BridgeXAPI Python SDK

Python SMS API SDK for sending SMS, bulk messaging and OTP delivery.

BridgeXAPI provides programmable routing, pricing visibility and delivery tracking.

A developer-first alternative to traditional SMS APIs like Twilio.

BridgeXAPI exposes SMS delivery as programmable infrastructure.

Most SMS APIs abstract routing behind a single endpoint.

BridgeXAPI does not.

You explicitly choose the route (`route_id`) for every message:
- control delivery paths
- control pricing per destination
- observe delivery using BridgeX message identifiers

This SDK provides a direct interface to that system.

---

## Installation

```bash
pip install bridgexapi
```

---

## Quick Start

```python
from bridgexapi import BridgeXAPI, Route

client = BridgeXAPI(api_key="YOUR_API_KEY")

response = client.send_one(
    route_id=Route.ROUTE_2,
    caller_id="BRIDGEXAPI",
    number="31612345678",
    message="Your verification code is 483921",
)

print(response.to_dict())
```

---

## Core Concept

BridgeXAPI makes routing explicit.

Messaging becomes part of your backend logic, not a black box.
