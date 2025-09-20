import json
import requests
import secretz

EMAIL = secretz.EMAIL
API_KEY = secretz.API_KEY
BASE_URL = secretz.BASE_URL

#LOGIN REQUEST
def login():

    #Auth key login
    url = f"{BASE_URL}/api/Auth/loginKey"
    headers = {
        "Accept": "text/plain",
        "Content-Type": "application/json"
    }
    payload = {
        "userName": EMAIL,
        "apiKey": API_KEY
    }

    try:
        response_login = requests.post(url, json=payload, headers=headers, timeout=15)
        response_login.raise_for_status()
        response_login = response_login.json() 
        token = response_login['token'] 
        save_json = {
            "token": token,
        }

        with open("token_data.json", "w") as f:
            json.dump(save_json, f)
            
        return token
        

    except Exception:
        print("Error: ", Exception)