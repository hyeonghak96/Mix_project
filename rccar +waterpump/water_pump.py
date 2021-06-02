from gpiozero import Motor
import time

#핀 수정 후 다시 테스트
motor = Motor(forward=19,backward=13,enable=26)

def motorforward(s):
    print('모터회전방향 :Forward')
    motor.forward(speed=s)
    time.sleep(1)
    motor.stop()

motorforward(1)
    
