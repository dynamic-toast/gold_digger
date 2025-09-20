import requests
import secretz

CONTRACT_ID = secretz.CONTRACT_ID
BASE_URL=secretz.BASE_URL
ACCOUNT_ID = secretz.ACCOUNT_ID

def place_order(jwt, signal):

    side_map = {"BUY": 0, "SELL": 1}
    
    url = f"{BASE_URL}/api/Order/place"
    headers = {
        "Authorization": f"Bearer {jwt}",
        "Accept": "text/plain",
        "Content-Type": "application/json"
    }
    payload = {
        "accountId": ACCOUNT_ID,
        "contractId": CONTRACT_ID,
        "type": 1,
        "side": side_map[signal["side"]],
        "size": 5,
        "limitPrice": signal.get("price"),
    }

    try:
        response_buy = requests.post(url, json=payload, headers=headers, timeout=15)
        response_buy.raise_for_status()
        response_buy = response_buy.json() 
        return response_buy
    except Exception as e:
        return print("Error: ", e)