import socket
import json
import ssl
# import uuid

def buffer(encode: bytes):

    encode_str = encode.decode()

    # picid = uuid.uuid4() # Random UUID

    dict_data = {
        'data' : encode_str
    }

	#辞書を文字列(JSON形式)に変換する
    str_data = json.dumps(dict_data)

    # 文字列をバイトデータに変換する
    data = str_data.encode()

    print("Start Sending Buffer Data")

    while True:
        packet = bytes(data[:1024])
        if not packet:
            break
        sender(packet)
        data = data[1024:]

    end_sign = "end"

    end = end_sign.encode()

    sender(end)

def sender(data: bytes):

    # 通常のソケットを作成
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# SSLコンテキストを作成
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations('server-key/server.crt')
    context.check_hostname = False
    context.verify_mode = ssl.CERT_REQUIRED

    # 172.20.0.1 = Auth Server

	# サーバーに接続
    ssl_client_socket = context.wrap_socket(client_socket, server_hostname='172.20.0.1')
    ssl_client_socket.connect(('172.20.0.1', 8443))

	# バイトデータを送信する
    ssl_client_socket.send(data)

    print("Send Data To Server")

	# データを送信
	# ssl_client_socket.send(b"Hello, server!")

	# ソケットを閉じる
    ssl_client_socket.close()
