import requests

def long_order(jwt, account_id):

    url ="https://api.topstepx.com/api/Order/place"
    headers = {
        "Authorization": f"Bearer {jwt}",
        "Accept": "text/plain",
        "Content-Type": "application/json"
    }
    payload = {
        "accountId": account_id,
        "contractId": "CON.F.US.GCE.Z25",
        "type": 2,
        "side": 0,
        "size": 1,
        "stopLossBracket": {
        "ticks": -50,
        "type": 4
        },
        "takeProfitBracket": {
        "ticks": 90,
        "type": 1
        }
    }


    try:
        response_order = requests.post(url, json=payload, headers=headers, timeout=15)
        response_order.raise_for_status()
        response_order = response_order.json() 
        return response_order
    except Exception as e:
        return print("Error: ", e)
    
def short_order(jwt, account_id):
    url ="https://api.topstepx.com/api/Order/place"
    headers = {
        "Authorization": f"Bearer {jwt}",
        "Accept": "text/plain",
        "Content-Type": "application/json"
    }
    payload = {
        "accountId": account_id,
        "contractId": "CON.F.US.GCE.Z25",
        "type": 2,
        "side": 1,
        "size": 1,
        "stopLossBracket": {
        "ticks": 50,
        "type": 4
        },
        "takeProfitBracket": {
        "ticks": -90,
        "type": 1
        }
    }

    try:
        response_order = requests.post(url, json=payload, headers=headers, timeout=15)
        response_order.raise_for_status()
        response_order = response_order.json() 
        return response_order
    except Exception as e:
        return print("Error: ", e)
    

def buy_market(jwt, account_id):
    url ="https://api.topstepx.com/api/Order/place"
    headers = {
        "Authorization": f"Bearer {jwt}",
        "Accept": "text/plain",
        "Content-Type": "application/json"
    }
    payload = {
        "accountId": account_id,
        "contractId": "CON.F.US.GCE.Z25",
        "type": 2,
        "side": 0,
        "size": 1,

        "stopLossBracket": {
        "ticks": -50,
        "type": 4
        },
        "takeProfitBracket": {
        "ticks": 90,
        "type": 1
        }
    }

    try:
        response_order = requests.post(url, json=payload, headers=headers, timeout=15)
        response_order.raise_for_status()
        response_order = response_order.json() 
        print("LOG: ORDER FILLED ------- 1 buy market filled")
        return response_order
    except Exception as e:
        return print("Error: ", e)

def sell_market(jwt, account_id):
    url ="https://api.topstepx.com/api/Order/place"
    headers = {
        "Authorization": f"Bearer {jwt}",
        "Accept": "text/plain",
        "Content-Type": "application/json"
    }
    payload = {
        "accountId": account_id,
        "contractId": "CON.F.US.GCE.Z25",
        "type": 2,
        "side": 1,
        "size": 1,

        "stopLossBracket": {
        "ticks": 50,
        "type": 4
        },
        "takeProfitBracket": {
        "ticks": -90,
        "type": 1
        }
    }

    try:
        response_order = requests.post(url, json=payload, headers=headers, timeout=15)
        response_order.raise_for_status()
        response_order = response_order.json() 
        print("LOG: ORDER FILLED ------- 1 sell market filled", response_order)
        return response_order
    except Exception as e:
        return print("Error: ", e)
    
def flatten(jwt, account_id):

    url = "https://api.topstepx.com/api/Position/closeContract"
    headers = {
        "Authorization": f"Bearer {jwt}",
        "Accept": "text/plain",
        "Content-Type": "application/json"
    }

    payload = {
        "accountId": account_id,
        "contractId": "CON.F.US.GCE.Z25"
    }

    response_order = requests.post(url, headers=headers, json=payload)
    response_order.raise_for_status()
    response_order = response_order.json()
    print("LOG: CLOSING POSITIONS ------- ", response_order)
    return response_order
