import flet as ft
import socket
import json
import ssl
import sys
import time
import threading

def main(page: ft.Page):

	page.window.minimizable = False
	page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
	page.window.width = 600
	page.window.height = 400
	page.update()
    
	def adjust():
		time.sleep(1)
		page.title = "FaceID - メール認証"
		page.update()

	threading.Thread(target=adjust).start()

	top = ft.Text("ようこそ " + username + "様", size=20, weight=ft.FontWeight.NORMAL, color=ft.colors.BLACK, selectable=True)
	t1 = ft.Text("登録いただいたメールアドレスに認証用のメールが送信されました。", size=15, weight=ft.FontWeight.NORMAL, color=ft.colors.GREEN, selectable=True)
	t2 = ft.Text("送信された値を入力して認証を行ってください。", size=15, weight=ft.FontWeight.NORMAL, color=ft.colors.GREEN, selectable=True)
	field = ft.TextField(label="値を入力", password=True, can_reveal_password=True)
	result = ft.Text(size=15, weight=ft.FontWeight.NORMAL, color=ft.colors.GREEN, selectable=True)

	def button_clicked(e):
		print("Press!")
		if field.value == password:
			print("Auth Done !")
			result.color = ft.colors.GREEN
			result.value = "認証に成功しました。"
			page.update()

			dict_data = {'status': 'gui', 'uuid': uuidstr, 'user': username, 'mail': mailadd}
			str_data = json.dumps(dict_data)
			byte_data = str_data.encode()

			client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
			context.load_verify_locations('keys/client.crt')
			context.check_hostname = False
			context.verify_mode = ssl.CERT_REQUIRED

			ssl_client_socket = context.wrap_socket(client_socket, server_hostname='192.168.1.1')
			ssl_client_socket.connect(('192.168.1.1', 8443))
			ssl_client_socket.send(byte_data)
			print("Send Data To Local")
			ssl_client_socket.close()
			page.window.destroy()
		else:
			result.color = ft.colors.RED
			result.value = "パスワードが誤っています。"
			page.update()

	b1 = ft.FilledTonalButton(text="クリックで認証", icon=ft.icons.RECOMMEND, on_click=button_clicked)
	page.add(top, t1, t2, field, b1, result)

def build():
    
    ft.app(target=main)

if __name__ == "__main__":
    
	global uuidstr, username, mailadd, password
	uuidstr = sys.argv[1]
	username = sys.argv[2]
	mailadd = sys.argv[3]
	password = sys.argv[4]

	build()
