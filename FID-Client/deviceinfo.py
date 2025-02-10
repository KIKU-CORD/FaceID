import requests
import time
import uuid
import hmac
import hashlib
import base64

# APIの基本設定
url = 'https://api.switch-bot.com'
token = '6111becc84886a39aadfa6eae686d19f206bf5194b1ffaea6cd12171d44dfdfc30f186371294cd55054c9887145b0bd1'  # SwitchBotのAPIトークン
secret = 'dd8eb53d57bdf10876f483fa5be71581'  # SwitchBotのクライアントシークレット

# SwitchBotに登録されているデバイスの一覧を取得する関数
def get_device_info():
    path = '/v1.1/devices'
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
    
    response = requests.get(url + path, headers=headers)
    
    print(f'Status Code: {response.status_code}')
    print(f'Response Text: {response.text}')
    
    if response.status_code == 200:
        response_json = response.json()
        print(f'Response JSON: {response_json}')
        return response_json
    else:
        print(f"Error: {response.status_code}, Message: {response.text}")
        return {}

if __name__ == "__main__":
    
    print("Getting Device List")
    devices = get_device_info()
    print(devices)