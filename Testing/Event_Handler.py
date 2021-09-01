#!/usr/bin/env python3
from PIL.Image import new
from anki_vector.connection import ControlPriorityLevel
from anki_vector.messaging import behavior_pb2
from anki_vector.messaging.shared_pb2 import Event
import numpy as np
import cv2
from matplotlib import pyplot as plt, rc
import glob

import anki_vector as av
from anki_vector.events import Events
from anki_vector.util import degrees, Pose, distance_mm, speed_mmps
import time
import math
import logging,threading
import sys

global f

class Flags():
    def __init__(self):
        self.see_object = False


def to_do():
    print(time.time())

async def Handle(robot, event_type,event):
    # global f
    print("See Object!")
    to_do()
    # try:
    #     await robot.motors.stop_all_motors()
    # except:
    #     print("Failed to stop")
    # f = True

    # done.set()
    # task = await robot.motors.set_wheel_motors(0,0)


def main():
    global f
    f = False
    flags = Flags()
    robot = av.AsyncRobot("00804458",behavior_control_level=ControlPriorityLevel.OVERRIDE_BEHAVIORS_PRIORITY)
    robot.connect()
    robot.motors.stop_all_motors()
    robot.behavior.set_lift_height(0.0)
    robot.behavior.set_head_angle(degrees(10.0))
    robot.events.subscribe(Handle, Events.robot_observed_object)

    # robot.behavior.drive_off_charger()
    # time.sleep(1)

    # robot.camera.init_camera_feed()
    drive_future = robot.behavior.drive_straight(distance_mm(300), speed_mmps(30))
    time.sleep(9.0)
    drive_future.cancel()
    # time.sleep(10)
    # while True:
    #     cv_image = cv2.cvtColor(np.array(robot.camera.latest_image.raw_image),cv2.COLOR_RGB2BGR)
    #     cv2.imshow("Image",cv_image)
    #     cv2.waitKey(1)

if __name__ == '__main__':
    main()

# import anki_vector
# from anki_vector.util import distance_mm, speed_mmps
# import time

# def main():
#     robot = anki_vector.AsyncRobot("00804458")
#     robot.connect()
#     drive_future = robot.behavior.drive_straight(distance_mm(300), speed_mmps(50))
#     time.sleep(2.0)
#     drive_future.cancel()

# if __name__ == '__main__':
#     main()