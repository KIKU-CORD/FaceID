import socket
import json
import ssl

import auth
import database

one_connection = True
recieve_cancel = False
recieved_data = ""

def reciever():

	global one_connection
	global recieve_cancel
	global recieved_data

	print("Start Server Side Server")

	# 172.20.0.1 = Auth Server (localhost)
	# 通常のソケットを作成
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind(('172.20.0.1', 8443))
	server_socket.listen(5)

	# SSLコンテキストを作成
	context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
	context.load_cert_chain(certfile="keys/server.crt", keyfile="keys/server.key")

	while True:

		if recieve_cancel: break

		# クライアント接続を受け入れる
		client_socket, addr = server_socket.accept()
		print(f"Connection from {addr}")

		# クライアントソケットをSSLでラップ
		ssl_client_socket = context.wrap_socket(client_socket, server_side=True)

		# クライアントからのデータを受信
		byte_data = ssl_client_socket.recv(1024)

		# バイトデータを文字列に変換する
		str_data = byte_data.decode()

		if "open" in str_data:
			# Change Database Status
			recieved_data = str_data
			status = encode_to_json()
			code = status["auth"]
			uuid = status["uuid"]
			if code == "open":
				# Update Door Status to Open
				database.updateValue("23CC_Users", "status", '1', "id", uuid)
				database.updateValue("23CC_Users", "last_action_time", "current_timestamp", "id", uuid)
				print("データベースのドア状態を更新")
			recieved_data = ""
			continue

		elif "close" in str_data:
			# Change Database Status
			recieved_data = str_data
			status = encode_to_json()
			code = status["auth"]
			if code == "close":
				uuid = status["uuid"]
				# Update Door Status to Close
				database.updateValue("23CC_Users", "status", '0', "id", uuid)
				database.updateValue("23CC_Users", "last_action_time", "current_timestamp", "id", uuid)
				print("データベースのドア状態を更新")
			recieved_data = ""
			continue

		if str_data == "end" and one_connection == False:
			# End Buffer Connection
			print("End Buffer Recieve")
			one_connection = True
			json = encode_to_json()
			auth.face_auth(json)
			recieved_data = ""
			continue

		if(one_connection == True):
			print("Start Buffer Recieve")
			one_connection = False

		if(one_connection == False):
        	# Buffer
			recieved_data += str_data

	server_socket.close()

def encode_to_json() -> dict[str, any]:

	print("Encode")
    
	dict_data = json.loads(recieved_data)

	return dict_data
