import os
from bridgexapi import BridgeXAPI


def main() -> None:
    api_key = os.getenv("BRIDGEXAPI_API_KEY")
    if not api_key:
        raise RuntimeError("Set BRIDGEXAPI_API_KEY environment variable.")

    client = BridgeXAPI(api_key=api_key)

    response = client.list_dlr(limit=10)
    print(response.to_dict())


if __name__ == "__main__":
    main()