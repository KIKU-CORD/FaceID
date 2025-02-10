import time
import threading

def start(sec: int, func):
    timert = threading.Thread(target=timer, args=(sec, func))
    timert.start()
    print("Start Timer")
    print(sec)

def timer(sec: int, func):
    time.sleep(sec)
    print("Run Function")
    func()