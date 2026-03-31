import os
from bridgexapi import BridgeXAPI, Route


def main() -> None:
    api_key = os.getenv("BRIDGEXAPI_API_KEY")
    if not api_key:
        raise RuntimeError("Set BRIDGEXAPI_API_KEY environment variable.")

    client = BridgeXAPI(api_key=api_key)

    response = client.send_sms(
        route_id=Route.ROUTE_2,
        caller_id="BRIDGEXAPI",
        numbers=[
            "34699108839",
            "34676784008",
            "34683466361",
        ],
        message="Your verification code is 483921",
    )

    print(response.to_dict())


if __name__ == "__main__":
    main()