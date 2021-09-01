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
from anki_vector.util import degrees, Pose, distance_mm
import time
import math
import logging,threading
from anki_vector.objects import CustomObjectMarkers, CustomObjectTypes

def rotate(robot,deg):
    speed = 30
    time360 = 9.5 #9.66
    with_block_multiplier = 1
    t = abs(deg)*time360/360*with_block_multiplier
    sign = deg/abs(deg)
    robot.motors.set_wheel_motors(-sign*speed,1*sign*speed)
    time.sleep(t)
    robot.motors.set_wheel_motors(0,0)

def get_centroid(region,shift_x,shift_y):
    h,w = 640,360
    cntrs,hier = cv2.findContours(region,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    total = 0
    x,y = 0,0
    for cntr in cntrs:
        for kp in cntr:
            x = x+kp[0][0]
            y = y+kp[0][1]
            total += 1
    cx,cy = int(x/total)+shift_x,int(y/total)+shift_y
    return cx,cy


def follow_line(robot,para=False, perp=False):
    at_spot = False
    while not at_spot:
        cv_image = cv2.cvtColor(np.array(robot.camera.latest_image.raw_image),cv2.COLOR_RGB2BGR)
        img = cv2.cvtColor(cv_image,cv2.COLOR_BGR2GRAY)
        ret,img = cv2.threshold(img,80,255,cv2.THRESH_BINARY)
        h,w = img.shape
        h_low, h_high = 200,300
        w_low, w_high = int(w/4),int(w*3/4)
        region = img[h_low:h_high,w_low:w_high]
        cx,cy = get_centroid(region,w_low,h_low)
        print("cx = {}".format(cx))

        cv2.imshow("region",region)
        img = cv2.circle(cv_image,(cx,cy),10,(255,0,0),-1,cv2.LINE_AA)
        cv2.imshow("camera feed",img)
        cv2.waitKey(1)

        k = (cx-w/2)/(w/2)
        speed = 10
        L = (k*10)+10
        R = (-1*(k)*10)+10
        robot.motors.set_wheel_motors(L,R)
        prox = robot.proximity.last_sensor_reading.distance.distance_mm
        if prox <= 70:
            robot.motors.set_wheel_motors(0,0)
            at_spot = True
            break
    robot.motors.set_wheel_motors(-20,-20)
    time.sleep(3)
    robot.motors.set_wheel_motors(0,0)
    # input("now would drop")
    robot.behavior.set_lift_height(0)
    robot.motors.set_wheel_motors(-30,-30)
    time.sleep(3)
    robot.motors.set_wheel_motors(0,0)
    input("done")

def dock_and_pick_up(robot,cube):
    robot.behavior.dock_with_cube(cube)
    robot.motors.set_lift_motor(0.4)
    time.sleep(2.5)
    robot.motors.set_lift_motor(0.0)
    up = False
    proxes = []
    t0 = time.time()
    while not up:
        prox = robot.proximity.last_sensor_reading.distance.distance_mm
        proxes.append(prox)
        if len(proxes) >= 5:
            if proxes[-1] >= 70 and proxes [-2] >= 70 and proxes [-3] >= 70:
                up = True
        t1 = time.time()
        if t1 - t0 > 5:
            break
    if not up:
        robot.motors.set_wheel_motors(-30,-30)
        time.sleep(1.5)
        robot.motors.set_wheel_motors(0,0)
        dock_and_pick_up(robot,cube)

def dock(robot,cube):
    robot.behavior.dock_with_cube(cube)
    docked = False
    proxes = []
    t0 = time.time()
    while not docked:
        prox = robot.proximity.last_sensor_reading.distance.distance_mm
        proxes.append(prox)
        if len(proxes) >= 5:
            if proxes[-1] <= 50 and proxes [-2] <= 50 and proxes [-3] <= 50:
                docked = True
        t1 = time.time()
        if t1 - t0 > 5:
            break
    if not docked:
        robot.motors.set_wheel_motors(-30,-30)
        time.sleep(1.5)
        robot.motors.set_wheel_motors(0,0)
        dock(robot,cube)

def dock_no_check(robot,cube):
    robot.behavior.dock_with_cube(cube)
    


def main():
    robot = av.Robot("00804458",behavior_control_level=ControlPriorityLevel.OVERRIDE_BEHAVIORS_PRIORITY,enable_custom_object_detection=True)
    robot.connect()
    robot.motors.stop_all_motors()
    robot.behavior.set_lift_height(0)
    robot.behavior.set_head_angle(degrees(0.0))
    robot.camera.init_camera_feed()


    done_everything = "n"

    while done_everything != "y":
        found_cube = False
        while not found_cube:
            t0 = time.time()
            while time.time()-t0 < 1:
                try:
                    for obj in robot.world.visible_objects:
                        if str(obj)[1:8] == "Charger":
                            found_cube = False
                            break
                        if str(obj)[1:10] == "LightCube":
                            found_cube = True
                        dock_and_pick_up(robot,obj)
                except Exception as ex:
                    print(ex)
                    rotate(robot,-30)
            rotate(robot,-30)
        
        # input("Next?")
        robot.behavior.set_lift_height(1)
        robot.behavior.set_head_angle(degrees(0.0))
        in_position = False
        while not in_position:
            robot.behavior.set_lift_height(1)
            # robot.motors.set_wheel_motors(20,-20)
            # time.sleep(2)
            # robot.motors.set_wheel_motors(0,0)
            rotate(robot,-30)
            cube_in = False
            charger_in = False
            cube = None
            t0 = time.time()
            while time.time()-t0 < 1:
                try:
                    for obj in robot.world.visible_objects:
                        print(str(obj)[1:10])
                        if str(obj)[1:10] == "LightCube":
                            cube_in = True
                            cube = obj
                        if str(obj)[1:8] == "Charger":
                            charger_in = True
                except Exception as ex:
                    print(ex)
                # print("cube_in = {}, charger_in = {}".format(cube_in,charger_in))
                if cube_in and charger_in:
                    # robot.behavior.dock_with_cube(cube)
                    dock(robot,cube)
                    robot.motors.set_wheel_motors(-20,-20)
                    time.sleep(7)
                    robot.motors.set_wheel_motors(0,0)
                    rotate(robot,-90)
                    in_position = True

        robot.behavior.set_lift_height(1)
        # input("Next?")
        robot.behavior.set_lift_height(1)

        num = int(input("spot num?"))
        robot.behavior.set_head_angle(degrees(-22))
        lines_passed = 0
        robot.motors.set_wheel_motors(10,10)
        while lines_passed < num:
            white = False
            black = False
            while not white:
                cv_image = cv2.cvtColor(np.array(robot.camera.latest_image.raw_image),cv2.COLOR_RGB2BGR)
                img = cv2.cvtColor(cv_image,cv2.COLOR_BGR2GRAY)
                ret,img = cv2.threshold(img,50,255,cv2.THRESH_BINARY)
                cv2.imshow("camera feed",img)
                cv2.waitKey(1)
                h,w = img.shape
                h_low, h_high = 265,275
                w_low, w_high = int(w/4),int(w*3/4)
                section = img[h_low:h_high,w_low:w_high]
                sum = np.sum(section)
                total = (h_high-h_low)*(w_high-w_low)*255
                print("sum = {}\n% = {}\n".format(sum,sum/total))
                if sum/total <= 0.1:
                    black = True
                if black and sum/total >= 0.9:
                    white = True
                print("lines_passed = {}\n".format(lines_passed))
            lines_passed += 1
            
        robot.motors.set_wheel_motors(0,0)
        robot.motors.set_wheel_motors(30,30)
        time.sleep(1)
        robot.motors.set_wheel_motors(0,0)
        rotate(robot,90)
        # input("Next?")
        robot.behavior.set_lift_height(1)
        robot.behavior.set_head_angle(degrees(-22))

        in_spot = False
        while not in_spot:
            cv_image = cv2.cvtColor(np.array(robot.camera.latest_image.raw_image),cv2.COLOR_RGB2BGR)
            img = cv2.cvtColor(cv_image,cv2.COLOR_BGR2GRAY)
            ret,img = cv2.threshold(img,50,255,cv2.THRESH_BINARY)
            cv2.imshow("camera feed",img)
            # cv2.waitKey(1)
            h,w = img.shape
            h_low, h_high = 100,300
            w_low, w_high = int(w/4),int(w*3/4)
            region = img[h_low:h_high,w_low:w_high]
            cv2.imshow("region",region)
            cv2.waitKey(1)
            # input("Try straighten")
            follow_line(robot)
            in_spot = True

        rotate(robot,180)
        done_everything = input(" done everything?")


def Ramp_Demo():
    robot = av.Robot("00804458",behavior_control_level=ControlPriorityLevel.OVERRIDE_BEHAVIORS_PRIORITY,enable_custom_object_detection=True)
    robot.connect()
    robot.motors.stop_all_motors()
    robot.behavior.set_lift_height(0)
    robot.behavior.set_head_angle(degrees(0.0))
    robot.camera.init_camera_feed()

    input("\n\nReady?\n\n")

    found_cube = False
    while not found_cube:
        rotate(robot,-30)
        t0 = time.time()
        while time.time()-t0 < 1:
            try:
                for obj in robot.world.visible_objects:
                    if str(obj)[1:10] == "LightCube":
                        found_cube = True
                        dock_and_pick_up(robot,obj)
            except Exception as ex:
                print(ex)
                rotate(robot,-30)
        
    

    robot.motors.set_wheel_motors(-60,-60)
    time.sleep(2)
    rotate(robot,-120)
    time.sleep(0.5)
    robot.motors.set_lift_motor(-0.5)
    time.sleep(3)
    robot.motors.set_lift_motor(0)
    time.sleep(0.5)
    robot.behavior.set_lift_height(0)
    robot.motors.set_wheel_motors(-60,-60)
    time.sleep(2)
    robot.motors.set_wheel_motors(0,0)

    rotate(robot,-75)
    found_cube = False
    while not found_cube:
        rotate(robot,-5)
        t0 = time.time()
        while time.time()-t0 < 1:
            try:
                for obj in robot.world.visible_objects:
                    if str(obj)[1:10] == "LightCube":
                        found_cube = True
                        robot.behavior.set_lift_height(1)
                        dock(robot,obj)
            except Exception as ex:
                print(ex)
                rotate(robot,-5)
    
    robot.behavior.set_lift_height(0)
    time.sleep(0.5)
    rotate(robot,90)
    time.sleep(0.5)

    robot.motors.set_wheel_motors(30,30)
    time.sleep(6)
    robot.motors.set_wheel_motors(0,0)
    time.sleep(0.5)
    rotate(robot,75)

    found_cube = False
    while not found_cube:
        rotate(robot,3)
        t0 = time.time()
        while time.time()-t0 < 1:
            try:
                for obj in robot.world.visible_objects:
                    if str(obj)[1:10] == "LightCube":
                        found_cube = True
                        robot.behavior.set_lift_height(1)
                        time.sleep(1)
                        dock_no_check(robot,obj)
            except Exception as ex:
                print(ex)
                rotate(robot,3)

    time.sleep(3)


    robot.motors.set_wheel_motors(30,30)
    time.sleep(4)
    robot.motors.set_wheel_motors(0,0)
    time.sleep(0.5)

    input("done")

    

    
        
if __name__ == '__main__':
    Ramp_Demo()

