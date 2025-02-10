import face_recognition
import cv2
import numpy
import base64
import sys
from PIL import ImageFont, ImageDraw, Image

import sender
import reciever

import timer

# import mail_gui

import threading # スレッド実装

import data

video_capture = cv2.VideoCapture(0)

def putText_japanese(img, text, point, size, color):

	fontpath ='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
	font = ImageFont.truetype(fontpath, size) # フォントサイズが32

	img_pil = Image.fromarray(img) # 配列の各値を8bit(1byte)整数型(0～255)をPIL Imageに変換。

	draw = ImageDraw.Draw(img_pil) # drawインスタンスを生成

	draw.text(point, text, font = font , fill = color) # drawにテキストを記載 fill:色 BGRA (RGB)

	img = numpy.array(img_pil, copy=True)

	#PILからndarrayに変換して返す
	return img

def capture():

	global face_amoaunt_detect

	# Webカメラの1フレームを取得、顔を検出し顔の特徴値を取得する
	ok, frame = video_capture.read()

	if frame is None: return
	if ok is False: return

	rectangle_color = (10, 10, 10)
	alpha = 0.5
	overlay = frame.copy()
	cv2.rectangle(overlay, (20, 20), (620, 80), rectangle_color, -1) # オーバーレイを画像にブレンド
	cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

	if data.keep_capture:

		rgb_frame = numpy.asarray( frame[:,:] )
		face_locations = face_recognition.face_locations(img=rgb_frame, number_of_times_to_upsample=1, model="hog")
		amount = len(face_locations) # 検出した顔の数

		if amount > 1:
			frame = putText_japanese(frame, "１人ずつ顔認証をお願いします", (30, 25), 32, (255, 255, 255))
			face_amoaunt_detect = 0
		elif amount == 0:
			frame = putText_japanese(frame, "画面に顔を映してください", (30, 25), 32, (255, 255, 255))
			face_amoaunt_detect = 0
		elif face_amoaunt_detect >= 50: # 5秒顔があったら実行
			data.keep_capture = False
			en_ok, buffer = cv2.imencode('.jpg', rgb_frame)
			if en_ok is True:
				encode = base64.b64encode(buffer)
				proccess = threading.Thread(target=sender.buffer(encode))
				proccess.start()
				face_amoaunt_detect = 0
				print("Face Sended")
			else:
				data.keep_capture = True
		else:
			frame = putText_japanese(frame, "顔検出中... 顔を動かさないでください", (30, 25), 32, (255, 255, 255))
			face_amoaunt_detect = face_amoaunt_detect + 1
			print(face_amoaunt_detect)
			print("Face Detected")

	else:

		frame = putText_japanese(frame, "顔認証を処理中です", (30, 25), 32, (255, 255, 255))

	cv2.imshow('WebCam', frame)

def start_capture():
	global face_amoaunt_detect
	face_amoaunt_detect = 0
	video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
	cv2.namedWindow('WebCam', cv2.WINDOW_NORMAL)
	cv2.setWindowProperty('WebCam', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
	while True:
		capture()
		if cv2.waitKey(1) & 0xFF == ord('q'):
			data.keep_capture = False
			stop_capture()
			break

def stop_capture():
	video_capture.release()
	cv2.destroyAllWindows()
	sys.exit()

def main():
	# スレッドを使用して各処理を分割
	data.init()
	capture = threading.Thread(target=start_capture)
	recieve = threading.Thread(target=reciever.reciever)
	capture.start()
	recieve.start()
	def start_app():
		data.keep_capture = True
	timer.start(10, start_app)

if __name__ == "__main__":
	main()