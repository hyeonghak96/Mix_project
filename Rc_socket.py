import rc_test
import camera_capture as camera
import aws_file as aws
import threading
import socket
import os
import time
import water_pump
from queue import Queue

# 보낼 파일 이름 공간,경로 확보
file_name = []
path = '/home/pi/Desktop/picture'
# 클라이언트 소켓 연결
ip = '13.48.157.80'
port = 9999


# 메인스레드 첫번째 클라이언트 연결

class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Settings(MetaSingleton):
    def __init__(self):
        self.path = '/home/pi/Desktop/picture'


# rc카 전진 -> 사진 캡처 -> 파일이름 저장 후 전송
def rc_repeat():
    rc_test.go_front()
    # camera.imagefilesave()
    time.sleep(1)
    aws.file_upload()


class RcSocket(threading.Thread):
    """
    서버와 소켓 통신을 위한 클래스. 런타임동안 종료하지 않는다.

    Attrubutes:
        file_queue: 서버로부터 받은 값을 저장하는 큐, Queue 객체
        status_queue: 차량 제어를 위한 큐, Queue 객체
    """
    def __init__(self, ip, port, file_queue, status_queue):
        super().__init__()
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((ip, port))
        self.file_queue = file_queue
        self.status_queue = status_queue

    def _clientsocket_send(self):
        """
        라즈베리파이에 저장된 사진을 모두 연결된 서버로 전송함
        """
        file_name = os.listdir('/home/pi/Desktop/picture')
        sendingfile = file_name[0].encode()
        self.clientSocket.send(sendingfile)
        # camera.removeAllFile(path)

    def _receive_data(self, file_queue):
        """
        서버로부터의 응답을 큐에 저장하는 메서드

        Args:
            file_queue: 서버로부터의 응답을 저장하는 큐, Queue 객체
        """
        data = self.clientSocket.recv(1024)
        decdata = data.decode("utf-8")
        time.sleep(1)
        print("받은 데이터 ", decdata)

        # 데이터 메인스레드로 전송
        file_queue.put(decdata)
        # time.sleep(1)

    def run(self):
        """
        스레드 실행을 위한 메서드
        차량 상태에 따라 실행이 제어된다.
        """
        while True:
            if self.status_queue.qsize() == 0:
                continue
            self._clientsocket_send()
            self._receive_data(self.file_queue)
            self.status_queue.get()
            

# 메인 스레드
class MainThread(threading.Thread):
    """
    서버로부터 받은 값에 따라 차량을 제어하기 위한 클래스

    Attrubutes:
        file_queue: 서버로부터 받은 값을 저장하는 큐, Queue 객체
        status_queue: 차량 제어를 위한 큐, Queue 객체
    """
    def __init__(self, file_queue, status_queue):
        super().__init__()
        self.file_queue = file_queue
        self.status_queue = status_queue

    def receiver(self, file_queue, status_queue):
        """
        서버로부터 받은 값에 따라 차량을 제어하고 차량의 현재 상태를 업데이트 한 뒤 저장한다.
        서버로부터 받은 값이 있을때만 값을 차량을 제어한다.

        Args:
            file_queue: 서버로부터 받은 값을 저장하는 큐, Queue 객체
            status_queue: 차량 제어를 위한 큐, Queue 객체
        """
        while True:
            if self.file_queue.qsize() == 0:
                continue
            data = file_queue.get()
            print(f'receiver:{data}')
            print('receiver done')

            # 수신값에 따른 모듈제어
            if data == '1' or data == '7':
                water_pump.motorforward(1)
                time.sleep(2)

            if data == '8':
                water_pump.motor_two_forward(1)
                time.sleep(2)

            if data == '2':
                time.sleep(1.5)

            rc_repeat()
            status_queue.put(1)

    def run(self):
        """
        스레드 실행을 위한 메서드
        """
        self.receiver(self.file_queue,self.status_queue)


def run():
    """
    전체 통신을 위한 함수
    """
    file_queue = Queue()
    status_queue = Queue()

    socket_instance = RcSocket('13.48.157.80', 9999, file_queue, status_queue)
    socket_instance.start()
    main_instance = MainThread(file_queue, status_queue)
    main_instance.start()

    rc_repeat()
    status_queue.put(1)

if __name__ == '__main__':
    run()