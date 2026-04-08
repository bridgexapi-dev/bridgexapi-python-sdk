# BridgeXAPI Python SDK

Programmable routing for messaging infrastructure.

BridgeXAPI exposes the routing layer behind SMS delivery.

This SDK is a direct interface to that system.

Not a messaging abstraction.

---

## What this is

Most SMS APIs expose messaging.

You send a request.  
The system decides routing.  
You get a result.

BridgeXAPI does the opposite.

You control:

- route selection (`route_id`)
- pricing before execution
- delivery behavior
- message-level tracking (`bx_message_id`)

Messaging becomes input.  
Routing becomes execution.

---

## Installation

```bash
pip install bridgexapi
````

---

## Quick start

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

## Deterministic flow

Instead of:

send → hope → delivered

You get:

estimate → send → track

### 1. Estimate

Resolve pricing per route before sending.

### 2. Send

Execution is explicit.

You choose the route.
No hidden routing.
No fallback logic.

### 3. Track

Each execution returns route-aware metadata and message-level tracking.

**Example response:**

```json
{
  "status": "success",
  "message": "SMS batch accepted via route 5",
  "order_id": 22953,
  "route_id": 2,
  "count": 1,
  "messages": [
    {
      "bx_message_id": "BX-22953-c5f4f53431ed22c2",
      "msisdn": "31612345678",
      "status": "QUEUED"
    }
  ],
  "cost": 0.087,
  "balance_after": 158.46
}
```

Used to:

* track delivery lifecycle
* debug failures
* compare route behavior
* audit execution

---

## Core concepts

### Routing is the system

A message is not “sent”.

It is routed through:

* carrier connections
* pricing agreements
* filtering rules
* latency profiles

Different routes produce different outcomes.

---

### A route is a contract

A `route_id` defines:

* delivery path
* pricing model
* latency characteristics
* traffic policy

Changing route = changing infrastructure.

---

### No black box

BridgeXAPI does not:

* auto-switch routes
* hide delivery decisions
* abstract execution paths

What you select is what gets executed.

---

## Why this exists

Traditional SMS APIs (Twilio-style):

* hide routing
* apply pricing after execution
* make delivery behavior unpredictable

BridgeXAPI exposes that layer.

So you can:

* control delivery
* predict cost
* debug behavior
* build reliable OTP systems

---

## Notes

* routing is explicit (`route_id`)
* pricing is route-dependent
* delivery is tracked per message (`bx_message_id`)
* execution behavior is deterministic

---

BridgeXAPI

Programmable routing for messaging infrastructure.

Docs: [https://docs.bridgexapi.io](https://docs.bridgexapi.io)
Main: [https://bridgexapi.io](https://bridgexapi.io)

