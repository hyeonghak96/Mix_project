import rc_test
import camera_capture as camera 
import aws_file as aws 
import threading
import socket
import os
import time
import water_pump
from queue import Queue

#보낼 파일 이름 공간,경로 확보
file_name=[]
path = '/home/pi/Desktop/picture'
#클라이언트 소켓 연결
ip='13.48.157.80'
port=9999

#메인스레드 첫번째 클라이언트 연결

class MetaSingleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Settings(MetaSingleton):
    def __init__(self):
        self.path = '/home/pi/Desktop/picture'


#rc카 전진 -> 사진 캡처 -> 파일이름 저장 후 전송 
def rc_repeat():
    rc_test.go_front()
    # camera.imagefilesave()
    time.sleep(1)
    aws.file_upload()

class RcSocket():
    def __init__(self, ip, port, q):
        self.clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.clientSocket.connect((ip,port))
        self.q = q
        

    def _clientsocket_send(self):
        file_name = os.listdir('/home/pi/Desktop/picture')
        sendingfile = file_name[0].encode()
        self.clientSocket.send(sendingfile)

    def _receive_data(self, q):
        while True:
            data = self.clientSocket.recv(1024)
            decdata = data.decode("utf-8")
            time.sleep(1)
            print("받은 데이터 ", decdata)

            # 데이터 메인스레드로 전송
            q.put(decdata)
            # time.sleep(1)
            q.put(None)
            if decdata is not None:
                break
        self.clientSocket.close()

    def run(self):
        self._clientsocket_send()
        self._receive_data(self.q)

#메인 스레드
def receiver(q):
    while True:
        data =q.get()
        print(f'receiver:{data}')
        print('receiver done')
        
        #수신값에 따른 모듈제어
        if data == '1' or data == '7':
            water_pump.motorforward(1)
            time.sleep(2)
            # camera.removeAllFile(path)
            break

        if data == '8':
            water_pump.motor_two_forward(1)
            time.sleep(2)
            # camera.removeAllFile(path)
            break

        if data == '2':
            time.sleep(1.5)
            # camera.removeAllFile(path)
            break

def run():
    TASK_QUEUE = Queue()
    # while True:
    # 소켓 연결 유지 
    rc_repeat()
    time.sleep(1)
    socket_instance = RcSocket('13.48.157.80', 9999, TASK_QUEUE)
    socket_instance.run()
    receiver(TASK_QUEUE)
    while True:
        rc_repeat()
        socket_instance = RcSocket('13.48.157.80', 9999, TASK_QUEUE)
        socket_instance.run()
        receiver(TASK_QUEUE)

if __name__=='__main__':
    run()

