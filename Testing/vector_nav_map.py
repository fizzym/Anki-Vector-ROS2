#!/usr/bin/env python3
from os import wait
from PIL.Image import new
from numpy.core.numeric import allclose
from numpy.lib.function_base import angle
# from tensorflow.keras.models import load_model
# from tensorflow.keras.models import model_from_json
import time, sys

import cv2
import numpy as np
from matplotlib import pyplot as plt
import math
from collections import Counter


import anki_vector as av
from anki_vector.events import Events
from anki_vector.util import degrees, Pose, distance_mm
from anki_vector.connection import ControlPriorityLevel
from anki_vector.messaging import behavior_pb2
from anki_vector.messaging.shared_pb2 import Event
from anki_vector.objects import CustomObjectMarkers, CustomObjectTypes

def main():
    t0 = time.time()
    robot = av.Robot("00804458",behavior_control_level=ControlPriorityLevel.OVERRIDE_BEHAVIORS_PRIORITY,enable_nav_map_feed=True,show_viewer=True,show_3d_viewer=True)
    robot.connect()
    # robot.behavior.drive_off_charger()
    robot.behavior.set_lift_height(0)
    # robot.motors.set_wheel_motors(-100,100)
    while True:
        latest_nav_map = robot.nav_map.latest_nav_map
        # print(latest_nav_map)
        # if time.time()-t0 > 30:
        #     break
    robot.motors.set_wheel_motors(0,0)
    
if __name__ == '__main__':
    main()