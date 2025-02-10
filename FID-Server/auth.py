import face_recognition
import numpy
import base64
import cv2

import sender
import data

def face_auth(dict_data: dict[str, any]):

	base64_str = dict_data["data"]

	binary = base64.b64decode(base64_str)
	frame = numpy.frombuffer(binary, dtype=numpy.uint8) # jpg

	rgb_frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

	face_locations = face_recognition.face_locations(rgb_frame)
	face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

	# 1フレームで検出した顔分ループする
	for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
    	# 認識したい顔の特徴値と検出した顔の特徴値を比較する
		matches = face_recognition.compare_faces(data.known_face_encodings, face_encoding)
		uuid = "Unknown"
		face_distances = face_recognition.face_distance(data.known_face_encodings, face_encoding)
		best_match_index = numpy.argmin(face_distances)
		if matches[best_match_index]:
			
			uuid = data.known_face_uuid[best_match_index]

			print("顔認証に成功しました。")
			print("判別ユーザー: " + uuid)

			user_data = data.known_users_data[best_match_index]

			user = user_data['user']
			mail = user_data['mail']

			dict_data = {

				'status' : 'auth',
				'uuid' : uuid,
				'user' : user,
				'mail' : mail

			}

			sender.sender(dict_data)

			return

	dict_data = {

		'status' : 'auth',
		'user' : 'none',
		'mail' : 'none'

	}

	sender.sender(dict_data)


        	