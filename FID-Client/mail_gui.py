import flet as ft

import mail_sender

def main(page: ft.Page):
    
	global screen
     
	screen = page

	page.title = "FaceID - メール認証"

	screen.window.opacity = 0 # 初回起動は画面を表示しない
    
	page.window_minimizable = False # 最小化の防止
    #page.window_maximizable = False 最大化をするとサイズが変わるのでサイズを指定できなくなる
	#page.window_resizable = False 上と同じ理由
	page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

	page.window_width = 600
	page.window_height = 400

	page.update()

	global top

	top = ft.Text(
    	"ようこそ " + username + "様",
    	size=20,
    	weight=ft.FontWeight.NORMAL,
    	color=ft.colors.BLACK,
    	selectable=True,
	)

	t1 = ft.Text(
    	"登録いただいたメールアドレスに認証用のメールが送信されました。",
    	size=15,
    	weight=ft.FontWeight.NORMAL,
    	color=ft.colors.GREEN,
    	selectable=True,
	)

	t2 = ft.Text(
    	"送信された値を入力して認証を行ってください。",
    	size=15,
    	weight=ft.FontWeight.NORMAL,
    	color=ft.colors.GREEN,
    	selectable=True,
	)

	global field

	field = ft.TextField(
    	label = "値を入力",
    	password=True,
    	can_reveal_password=True,
	)

	result = ft.Text(
    	size=15,
    	weight=ft.FontWeight.NORMAL,
    	color=ft.colors.GREEN,
    	selectable=True,
	)

	def button_clicked(e):
		print("Press!")
		if field.value == password:
			print("Auth Done !")
			result.color=ft.colors.GREEN
			result.value = "認証に成功しました。"
			page.update()

			# Radius 認証開始
			mail_sender.senderRadius(uuidstr, username, mailadd)

			show(False)

		else:
			result.color=ft.colors.RED
			result.value = "パスワードが誤っています。"
			page.update()

	b1 = ft.FilledTonalButton(
    	text="クリックで認証",
    	icon=ft.icons.RECOMMEND,
    	on_click=button_clicked,
	)

	page.add(top, t1, t2, field, b1, result)

def register(uuid: str, user: str, mail: str, passwd: str):

	global uuidstr
	global username
	global mailadd
	global password

	uuidstr = uuid
	username = user
	mailadd = mail
	password = passwd

	top.value = "ようこそ " + username + "様"
	field.value = ""
	screen.update()
    
def show(show: bool):

	if show:

		screen.window.opacity = 1

	else:

		screen.window.opacity = 0

	screen.update()
    
def build():

	global uuidstr
	global username
	global mailadd
	global password

	username = 'unknown'

	ft.app(target=main, view=ft.AppView.FLET_APP_HIDDEN)
