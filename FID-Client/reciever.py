import socket
import json
import ssl

import data
import mail_auth
import mail_sender
import switchbot

import time
import timer

import sender

import threading

import logger

recieve_cancel = False

def reciever():

    global recieve_cancel

    print("Start Client Side Server")

	# 通常のソケットを作成
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('192.168.1.1', 8443))
    server_socket.listen(5)
	# SSLコンテキストを作成
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="keys/client.crt", keyfile="keys/client.key")

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

        dict_data = json.loads(str_data)

        load_type(dict_data["status"], dict_data)

    server_socket.close()

def load_type(status: str, userdata: any):

    if 'uuid' not in userdata:

        print("顔を判別できませんでした。")

        data.keep_capture = True

        return

    uuid = userdata['uuid']
    user = userdata['user']
    mail = userdata['mail']

    if(status == "auth"):

        # すでに入室していたら 
        if uuid in data.in_users:
            
            print("すでに入室しています。")

        else:

            print("顔認証完了: " + user)

            if data.interval > 0:

                data.keep_capture = False

                switchbot.controll("unlock")

                def reset_capture():
                    data.keep_capture = True

                timer.start(10, reset_capture)
                
                data.interval = 0
                print("*** 複数人入室 ***")

                data.later.append(uuid)

                def timerg(cuuid: str):
                    time.sleep(120)
                    if cuuid in data.later:
                        print("[!] 認証違反 " + uuid)
                        logger.sendSyslog("[!!! ALERT !!! RADIUS NOT DONE] " + uuid + " , " + user + " , " + mail)

                timerf = threading.Thread(target=timerg, args=(uuid,))
                timerf.start()

                change_status = {

                    'auth': 'open',
                    'uuid': uuid
                    
                }

                str_data = json.dumps(change_status)
                byte_data = str_data.encode()

                sender.sender(byte_data)

                data.in_users.append(uuid)

                mail_sender.senderRadiusHarry(uuid, user, mail)

                logger.sendSyslog("[Face Auth Comp **DOUBLE RADIUS SKIP**] " + uuid + " , " + user + " , " + mail)

            else:

                mail_auth.setup_passwd(uuid, user, mail)

                logger.sendSyslog("[Face Auth Comp] " + uuid + " , " + user + " , " + mail)

    elif(status == "gui"):

        print("メール認証完了")

        mail_sender.senderRadius(uuid, user, mail)

        logger.sendSyslog("[Mail Auth Comp] " + uuid + " , " + user + " , " + mail)

    elif(status == "comp"):

        door = userdata['door']

        print("すべての認証完了" + uuid)

        logger.sendSyslog("[All Auth Comp] " + uuid + " , " + user + " , " + mail)

        if(door == "in"):

            print("入室")

            if uuid in data.later:

                print("複数人入室の認証が完了しました。" + user)

                data.later.remove(uuid)

                mail_sender.senderOut(uuid, user, mail)

                logger.sendSyslog("[Double Auth Comp] " + uuid + " , " + user + " , " + mail)

            elif uuid in data.in_users:
            
                print("すでに入室しています。")

            else:

                data.keep_capture = False

                switchbot.controll("unlock")

                def reset_capture():
                    data.keep_capture = True

                timer.start(10, reset_capture)

                change_status = {

                    'auth': 'open',
                    'uuid': uuid
                
                }

                str_data = json.dumps(change_status)
                byte_data = str_data.encode()

                sender.sender(byte_data)

                mail_sender.senderOut(uuid, user, mail)

                data.in_users.append(uuid)

                logger.sendSyslog("[Open Door] " + uuid + " , " + user + " , " + mail)

                if data.interval == 0:

                    data.interval = 20

                    print("* 普通入室 *")

                    def timerh():
                        while data.interval > 0:
                            time.sleep(1)
                            data.interval = data.interval - 1
                            print("複数人入室を受付中...")
                            print(data.interval)

                    timers = threading.Thread(target=timerh)
                    timers.start()

        elif(door == "mid-in"):

            print("再入室")

            if uuid not in data.in_users:
            
                print("まだ入室していません。")

            else:

                data.keep_capture = False

                switchbot.controll("unlock")

                def reset_capture():
                    data.keep_capture = True

                timer.start(10, reset_capture)

                logger.sendSyslog("[Mid In] " + uuid + " , " + user + " , " + mail)

        elif(door == "out"):

            print("退出")

            if uuid not in data.in_users:
            
                print("まだ入室していません。")

            else:

                data.in_users.remove(uuid)

                data.keep_capture = False

                switchbot.controll("unlock")

                def reset_capture():
                    data.keep_capture = True

                timer.start(10, reset_capture)

                change_status = {

                    'auth': 'close',
                    'uuid': uuid
                
                }

                str_data = json.dumps(change_status)
                byte_data = str_data.encode()

                sender.sender(byte_data)

                logger.sendSyslog("[Out] " + uuid + " , " + user + " , " + mail)

        

        
