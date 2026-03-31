import os
from bridgexapi import BridgeXAPI


def main():
    api_key = os.getenv("BRIDGEXAPI_API_KEY")
    if not api_key:
        raise RuntimeError("Set BRIDGEXAPI_API_KEY environment variable.")

    client = BridgeXAPI(api_key=api_key)

    dlr_list = client.list_dlr(limit=1)

    if not dlr_list.messages:
        raise RuntimeError("No delivery reports found.")

    bx_message_id = dlr_list.messages[0].bx_message_id
    response = client.get_dlr(bx_message_id)

    print(response.to_dict())


if __name__ == "__main__":
    main()