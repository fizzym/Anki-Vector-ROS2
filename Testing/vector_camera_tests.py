import anki_vector as av
import numpy as np
import cv2
from PIL import Image
import threading

def on_new_raw_camera_image(robot,event_type,event,done):
    cv_image = cv2.cvtColor(np.array(event.image),cv2.COLOR_RGB2BGR)
    print("Image dimensions = {}".format(cv_image.shape))
    cv2.imshow("camera feed",cv_image)
    cv2.waitKey(1)
    done.set()

def on_new_camera_image(robot,event_type,event,done):
    cv_image = cv2.cvtColor(np.array(event.image.annotate_image()),cv2.COLOR_RGB2BGR)
    print("Image dimensions = {}".format(cv_image.shape))
    cv2.imshow("camera feed",cv_image)
    cv2.waitKey(1)
    done.set()

def Test_1(robot):
    while True:
        cv_image = cv2.cvtColor(np.array(robot.camera.latest_image.raw_image),cv2.COLOR_RGB2BGR)
        print("Image dimensions = {}".format(cv_image.shape))
        cv2.imshow("camera feed",cv_image)
        cv2.waitKey(1)

def Test_2(robot):
    while True:
        done = threading.Event()
        robot.events.subscribe(on_new_raw_camera_image, av.events.Events.new_raw_camera_image,done)

def Test_3(robot):
    while True:
        done = threading.Event()
        robot.events.subscribe(on_new_camera_image, av.events.Events.new_camera_image,done)

def main(test_num):
    robot = av.Robot(serial="00804458")
    robot.connect()
    robot.camera.init_camera_feed()
    if test_num == 1:
        print("Running test 1")
        Test_1(robot)
    if test_num == 2:
        print("Running test 2")
        Test_2(robot)
    if test_num == 3:
        print("Running test 3")
        Test_3(robot)
    
    
    
if __name__ == '__main__':
    main(3)

