import requests
import pandas as pd
from strategy import GoldDigger


#LOGIN REQUEST
def login(email, api_key):

    #Auth key login
    url = "https://api.topstepx.com/api/Auth/loginKey"
    headers = {
        "Accept": "text/plain",
        "Content-Type": "application/json"
    }
    payload = {
        "userName": email,
        "apiKey": api_key
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        response = response.json() 
        jwt = response['token']

        print(f"LOG: Login success ------- ",{jwt[:12]},"...")

        return jwt
        
    except Exception:
        print("Error: ", Exception)

def get_accounts(jwt):
    url = "https://api.topstepx.com/api/Account/search"
    headers = {
        "Authorization": f"Bearer {jwt}",
        "Accept": "text/plain",
        "Content-Type": "application/json"
    }
    account_data = requests.post(url, headers=headers, json={})
    account_data.raise_for_status()
    account_data = account_data.json()

    accounts = account_data.get("accounts", [])

    return accounts

def load_bars():
    try:
        df = pd.read_csv("bars.csv", parse_dates=["timestamp"])
        df = df.tail(500)
    
        return df
    except Exception:
        return pd.DataFrame()
    
def search_positions(jwt, account_id):
    url = "https://api.topstepx.com/api/Position/searchOpen"
    headers = {
        "Authorization": f"Bearer {jwt}",
        "Accept": "text/plain",
        "Content-Type": "application/json"
    }

    payload = {
        "accountId": account_id
    }

    positions = requests.post(url, headers=headers, json=payload)
    positions.raise_for_status()
    return positions.json().get("positions", [])

def compute_openpnl(positions, last_price):    
    if not positions or len(positions) == 0:
        return 0.0
    
    print(positions)
    
    pos = positions[0]
    
    entry = pos.get("averagePrice")
    size = pos.get("size")
    type = pos.get("type")

    if size == 0 or type is None:
        return 0.0
    
    close = last_price
    
    if type == 1:  # LONG
        pnl = (close - entry) * 100 * size
        open_pnl = round(pnl, 2)
        return open_pnl
    elif type == 2:  # SHORT
        pnl = (entry - close) * 100 * size
        open_pnl = round(pnl, 2)
        return open_pnl
    else:
        return 0.0

def activate_bot():
    strategy = GoldDigger()
    signal_response = strategy.signal()

    return signal_response

def get_tick_price():
    data = pd.read_csv("ticks.csv")
    if data.empty:
        return None
    
    last_price = data["price"].iloc[-1]

    return float(last_price)
