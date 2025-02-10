import glob
import os
import threading
import face_recognition

import reciever
import data

import database

def user_and_face_list():

	datadir = os.getcwd() + '/datas/'

	users = database.getAllValue('23CC_Users')

	f = open('/var/www/radius/users', 'w')

	f.truncate(0) # キャッシュファイル内のデータを削除

	for userdata in users:
		uuid = userdata[0]
		name = userdata[1]
		mail = userdata[3]

		print(uuid, name, mail, sep=':', file=f) # : で区切ってファイルに書き込み

		# キャッシュファイル作成と同時に画像データも学習

		face = datadir + uuid + ".jpg"

		image = face_recognition.load_image_file(face)
		face_encoding = face_recognition.face_encodings(image)[0]
		data.known_face_encodings.append(face_encoding)

		data.known_face_uuid.append(uuid)

		user_data_format = {
			'uuid' : uuid,
			'user' : name,
			'mail' : mail
		}

		data.known_users_data.append(user_data_format)

		print("登録データ: " + name)

	print("Prepared Users Cache File")

def main():
	# スレッドを使用して各処理を分割
	# 顔認証データリスト準備
	data.init() # Setup Global Variable
	user_and_face_list() # Setup Users Cache File and Face
	recieve= threading.Thread(target=reciever.reciever)
	recieve.start()

if __name__ == "__main__":
	main()