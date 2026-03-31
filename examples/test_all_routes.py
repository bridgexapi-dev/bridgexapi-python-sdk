import os
import time
from bridgexapi import BridgeXAPI


def main() -> None:
    api_key = os.getenv("BRIDGEXAPI_API_KEY")
    if not api_key:
        raise RuntimeError("Set BRIDGEXAPI_API_KEY environment variable.")

    target_number = os.getenv("BRIDGEXAPI_TEST_NUMBER")
    if not target_number:
        raise RuntimeError("Set BRIDGEXAPI_TEST_NUMBER environment variable.")

    client = BridgeXAPI(api_key=api_key)
    routes_to_test = [1, 2, 3, 4]

    print("\nBridgeXAPI programmable routing test")
    print(f"Recipient: {target_number}\n")

    results = []

    for route_id in routes_to_test:
        handset_ref = f"R{route_id}"

        try:
            response = client.send_one(
                route_id=route_id,
                caller_id="BRIDGEXAPI",
                number=target_number,
                message=f"BridgeXAPI verification notice. Ref: {handset_ref}.",
            )

            msg = response.messages[0] if response.messages else None
            bx_message_id = msg.bx_message_id if msg else None

            print(f"[Route {route_id}] ACCEPTED")
            print(f"  order_id      : {response.order_id}")
            print(f"  bx_message_id : {bx_message_id}")
            print(f"  cost          : {response.cost} EUR")
            print(f"  handset_ref   : {handset_ref}")
            print()

            results.append(
                {
                    "route_id": route_id,
                    "status": "ACCEPTED",
                    "order_id": response.order_id,
                    "bx_message_id": bx_message_id,
                    "cost": response.cost,
                    "handset_ref": handset_ref,
                    "error": None,
                }
            )

        except Exception as e:
            print(f"[Route {route_id}] REJECTED")
            print(f"  reason        : {e}")
            print()

            results.append(
                {
                    "route_id": route_id,
                    "status": "REJECTED",
                    "order_id": None,
                    "bx_message_id": None,
                    "cost": None,
                    "handset_ref": handset_ref,
                    "error": str(e),
                }
            )

        time.sleep(1.0)

    print("SUMMARY")
    print("-" * 110)
    print(
        f"{'ROUTE':<8}"
        f"{'STATUS':<12}"
        f"{'ORDER_ID':<12}"
        f"{'BX_MESSAGE_ID':<28}"
        f"{'HANDSET_REF':<14}"
        f"{'COST':<10}"
    )
    print("-" * 110)

    for item in results:
        order_id = str(item["order_id"]) if item["order_id"] is not None else "-"
        bx_message_id = item["bx_message_id"] or "-"
        cost = f"{item['cost']:.3f}" if item["cost"] is not None else "-"

        print(
            f"{item['route_id']:<8}"
            f"{item['status']:<12}"
            f"{order_id:<12}"
            f"{bx_message_id:<28}"
            f"{item['handset_ref']:<14}"
            f"{cost:<10}"
        )

    print("-" * 110)
    print("\nCheck your phone to compare what lands per route.\n")


if __name__ == "__main__":
    main()