import requests
import time
import uuid
import hmac
import hashlib
import base64

# APIの基本設定
url = 'https://api.switch-bot.com'
token = '???'  # SwitchBotのトークン
secret = '???'  # SwitchBotのクライアントシークレット

def control_device(deviceId, command):
    
    path = f'/v1.1/devices/{deviceId}/commands'
    nonce = str(uuid.uuid4())
    timestamp = str(int(time.time() * 1000))

    string_to_sign = token + timestamp + nonce
    sign = base64.b64encode(
        hmac.new(secret.encode('utf-8'), string_to_sign.encode('utf-8'), digestmod=hashlib.sha256).digest()
    )

    headers = {
        'Authorization': token,
        'sign': sign.decode('utf-8'),
        't': timestamp,
        'nonce': nonce
    }
    
    body = {
        "command": command,
        "parameter": "default",
        "commandType": "command"
    }

    print(f"Headers: {headers}")
    print(f"Body: {body}")

    response = requests.post(url + path, headers=headers, json=body)
    print(f'Status Code: {response.status_code}')
    print(f'Response Text: {response.text}')
    
    if response.status_code == 200:
        response_json = response.json()
        print(f'Response JSON: {response_json}')
        return response_json
    else:
        print(f"Error: {response.status_code}, Message: {response.text}")
        return {}

def controll(query: str): # lock or unlock

    deviceId = 'DED6F81C0C36'  # 取得したスマートロックのデバイスID

    print(f"Sending command '{query}' to device '{deviceId}'")
    response = control_device(deviceId, query)
    print(response)
