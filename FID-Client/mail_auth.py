import string
import random

# import mail_gui
import mail_sender

import subprocess

import threading

import data

def passwd_gen() -> str:
	
    chars = string.ascii_letters + string.digits
    randomStr = ''.join([random.choice(chars) for i in range(5)])
	
    print(randomStr)
	
    return randomStr

def setup_passwd(uuid: str, user: str, mail: str):
    
    passwd = passwd_gen()

    mail_sender.sender(user, mail, passwd)

    # gui = threading.Thread(target=runMailGUI, args=(uuid, user, mail, passwd))
    # gui.start()

    runMailGUI(uuid, user, mail, passwd)

    # mail_gui.register(uuid, user, mail, passwd)

    # mail_gui.show(True)

def runMailGUI(uuid: str, user: str, mail: str, passwd: str):

    try:
        # 実行したいPythonプログラムのファイルパス
        # program_path = 'mail_gui_sub.py'

        # サンプル引数
        # sample_args = [uuid, user, mail, passwd]

        # subprocess.runを使ってプログラムを実行
        # subprocess.run(['python3', program_path] + sample_args)
        subprocess.Popen(["python3", "mail_gui_sub.py", uuid, user, mail, passwd])
        # subprocess.run('echo ' + uuid + ' ' + user + ' ' + ' ' + mail + ' ' + passwd + ' | python3 mail_gui_sub.py', shell=True)

    except Exception as e:

        print(f"エラーが発生しました: {e}")