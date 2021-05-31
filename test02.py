import rc_test
import camera_capture as camera 
import aws_file as aws 
import threading
import socket
import os
import time
from queue import Queue

#보낼 파일 이름 공간 확보
file_name=[]
path = '/home/pi/Desktop/picture'
# send_file_name = file_name[0]
#클라이언트 소켓 연결
ip = '192.168.0.15'
# ip='13.48.157.80'
# ip = '172.30.1.95'
port=9999

#메인스레드 첫번째 클라이언트 연결
mainSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
mainSocket.connect((ip,port))
print("첫번째 클라이언트가 연결되었습니다.")



#rc카 전진 -> 사진 캡처 -> 파일이름 저장 후 전송 
def rc_repeat():
    rc_test.go_front()
    camera.imagefilesave()
    time.sleep(1)
    file_name= os.listdir(path)
    sendingfile =file_name[0].encode()
    mainSocket.send(sendingfile)
    # aws.fileupload()

#클라이언트 소켓 연결 -> 메인스레드 데이터 전송
def socket_thread():
    clientSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    clientSocket.connect((ip,port))
    print("두번째 클라이언트가 연결되었습니다.")
    #데이터 지속적으로 수신
    while True:
        data = clientSocket.recv(1024)
        decdata=data.decode("utf-8")
        time.sleep(1)
        print("받은 데이터 ",decdata)
        
        #데이터 메인스레드로 전송
        q.put(decdata)
        time.sleep(1)
        q.put(None)
        if decdata == "종료":
            break         
    clientSocket.close()

#메인 스레드
def receiver(q):
    while True:
        data =q.get()
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
    while True:
        rc_repeat()
        receiver(q)


# 소켓 스레드와 스레드에 필요한 큐 선언 
q= Queue()
sthread = threading.Thread(target= socket_thread,args=())


if __name__=='__main__':
    sthread.start()
    run()



