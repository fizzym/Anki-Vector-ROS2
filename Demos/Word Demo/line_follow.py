#!/usr/bin/env python3
from os import wait
from PIL.Image import new
from tensorflow.keras.models import load_model
from tensorflow.keras.models import model_from_json
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

from vector_letter_recog_test import Load_Model, use_model, get_rois


def img_processing(img_raw):
    gray = cv2.cvtColor(img_raw,cv2.COLOR_BGR2GRAY)
    # cv2.imshow("Grayscale", gray)
    # cv2.waitKey(1)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    # cv2.imshow("blurred", blur)
    # cv2.waitKey(1)
    ret,thresh = cv2.threshold(blur,127,255,cv2.THRESH_BINARY_INV)
    # cv2.imshow("Threshold", thresh)
    # cv2.waitKey(1)
    h,w = thresh.shape[0],thresh.shape[1]
    # region = np.copy(thresh)
    # region[0:int(h/2),0:w] = 0
    # region[0:h,0:int(w/4)] = 0
    # region[0:h,int(3*(w/4)):w] = 0
    # region = cv2.rectangle(region,(int(w/4),int(h/2.25)),(int(3*(w/4)),h),0,2)
    # cv2.imshow("Region", region)
    # cv2.waitKey(1)


    low_h,high_h,low_w,high_w = int(h/3),int(2*h/3),int(w/4),int(3*w/4)


    region = np.copy(thresh)
    region[0:low_h,0:w] = 0
    region[0:h,0:low_w] = 0
    region[0:h,high_w:w] = 0
    region[high_h:h,0:w] = 0
    cv2.imshow("Region", region)
    cv2.waitKey(1)

    cntrs,hier = cv2.findContours(region,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    m = 0
    if len(cntrs) > 0:
        cntr = cntrs[0]
        for i in cntrs:
            if len(i) > m:
                m = len(i)
                cntr = i
    else:
        cx = int(w/2)
        cy = int(h/2)
    # contoured = cv2.drawContours(img_raw,[cntr],0,255,2)
    # cv2.imshow("Contoured", contoured)
    # cv2.waitKey(1)

    try:
        M = cv2.moments(cntr)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
    except:
        cx = int(w/2)
        cy = int(h/2)
        print("Error calculating moments and center")
    
    center = cv2.circle(img_raw,(cx,cy),3,255,-1,cv2.LINE_AA)
    cv2.imshow("Center", center)
    cv2.waitKey(1)
    return [float(cx),float(cy)]




def main(args=None):
    # characters = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    # model = Load_Model()
    # # img = cv2.imread('A.jpg')
    # BB = Letter_Bounding_box()
    # C1 = Cube()
    robot = av.Robot("00804458",behavior_control_level=ControlPriorityLevel.OVERRIDE_BEHAVIORS_PRIORITY,enable_custom_object_detection=True)
    robot.connect()
    robot.motors.stop_all_motors()
    robot.behavior.set_lift_height(1.0)
    robot.behavior.set_head_angle(degrees(-22.0))
    robot.camera.init_camera_feed()
    # robot.events.subscribe(Handle_object_seen, Events.object_observed,BB,C1)

    while True:
        cv_image = cv2.cvtColor(np.array(robot.camera.latest_image.raw_image),cv2.COLOR_RGB2BGR)
        center = img_processing(cv_image)
        # img = cv2.circle(cv_image,(int(center[0]),int(center[1])),5,(255,0,0))
        # cv2.imshow("camera feed",img)
        # cv2.waitKey(1)


if __name__ == '__main__':
    main()