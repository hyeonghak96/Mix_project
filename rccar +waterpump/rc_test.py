from gpiozero import Robot
import time
import camera_capture as camera

robot = Robot(left=(13,19,26), right=(20,16,21))

def go_front():
    robot.forward(speed=1)
    
def stop():
    robot.stop()
    
while True:
    go_front()
    time.sleep(1)
    robot.stop()
    camera.imagefilesave()
    
    


