import os
from bridgexapi import BridgeXAPI


def main():
    api_key = os.getenv("BRIDGEXAPI_API_KEY")
    if not api_key:
        raise RuntimeError("Set BRIDGEXAPI_API_KEY environment variable.")

    client = BridgeXAPI(api_key=api_key)

    print("=== ROUTES ===")
    routes = client.list_routes()
    print(routes)

    print("\n=== ROUTE 1 ===")
    route = client.get_route(1)
    print(route)

    print("\n=== PRICING ROUTE 1 ===")
    pricing = client.get_route_pricing(1)
    print(pricing)


if __name__ == "__main__":
    main()