import socket
import json
import ssl
# import uuid

def sender(dict_data: dict[str, any]):

	# 通常のソケットを作成
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# SSLコンテキストを作成
	context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
	context.load_verify_locations('client-keys/client.crt')

	context.check_hostname = False
	context.verify_mode = ssl.CERT_REQUIRED

	# サーバーに接続
	ssl_client_socket = context.wrap_socket(client_socket, server_hostname='192.168.1.1')
	ssl_client_socket.connect(('192.168.1.1', 8443))

	#辞書を文字列(JSON形式)に変換する
	str_data = json.dumps(dict_data)

	# 文字列をバイトデータに変換する
	byte_data = str_data.encode()

	# バイトデータを送信する
	ssl_client_socket.send(byte_data)

	print("Send Data To Client")

	# データを送信
	# ssl_client_socket.send(b"Hello, server!")

	# ソケットを閉じる
	ssl_client_socket.close()
