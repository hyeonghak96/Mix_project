import rc_test
import camera_capture as camera 
import aws_file as aws 
import threading
import socket
import os
import time
from queue import Queue

#보낼 파일 이름 공간 확보
# file_name=[]
# path = '/home/pi/Desktop/picture'
#클라이언트 소켓 연결
# ip = '192.168.0.15'
# ip='13.48.157.80'
# port=9999


#rc카 전진 -> 사진 캡처 -> 파일이름 저장 후 전송 
def rc_repeat():
    rc_test.go_front()
    camera.imagefilesave()
    time.sleep(1)
    # aws.fileupload()

class RcSocket(threading.Thread):
    def __init__(self, ip, port, q):
        self.clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.clientSocket.connect((ip,port))
        self.q = q
        super().__init__()

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
            time.sleep(1)
            q.put(None)
            if decdata == "종료":
                break
        self.clientSocket.close()

    def run(self):
        self._clientsocket_send()
        self._receive_data(self.q)

#메인 스레드
class MainThread:
    def __init__(self, q):
        self.q = q

    def receiver(self):
        while True:
            data =self.q.get()
            print(f'receiver:{data}')
            print('receiver done')

            #수신값에 따른 모듈제어
            if data == "1":
                water_pump.motorforward(1)
                time.sleep(2)
                camera.removeAllFile()
                break

            if data == "2":
                water_pump.motor_two_forward(1)
                time.sleep(2)
                camera.removeAllFile()
                break

            if data == "healthy":
                time.sleep(1.5)
                camera.removeAllFile()
                break

def run():
    TASK_QUEUE = Queue()
    while True:
        rc_repeat()
        socket_instance = RcSocket('192.168.0.15', 9999, TASK_QUEUE)
        socket_instance.start()
        main_instance = MainThread(TASK_QUEUE)
        main_instance.receiver()

if __name__=='__main__':
    run()

