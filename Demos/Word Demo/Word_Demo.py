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


import anki_vector as av
from anki_vector.events import Events
from anki_vector.util import degrees, Pose, distance_mm
from anki_vector.connection import ControlPriorityLevel
from anki_vector.messaging import behavior_pb2
from anki_vector.messaging.shared_pb2 import Event
from anki_vector.objects import CustomObjectMarkers, CustomObjectTypes

from vector_letter_recog_test import Load_Model, use_model, get_rois

from hardcoded_letter_recog import identify_letter

def rotate(robot,deg):
    speed = 30
    time360 = 9.66 # 9.5 
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
        time.sleep(3)
        robot.motors.set_wheel_motors(0,0)
        robot.behavior.set_lift_height(0)
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



class Letter_Bounding_box():
    def __init__(self):
        self.x1,self.y1,self.x2,self.y2 = 0,0,0,0
        self.pose = Pose(0,0,0,angle_z=degrees(0))
    def area(self):
        return (self.x2-self.x1)*(self.y2-self.y1)

class Cube():
    def __init__(self):
        self.x,self.y,self.z,self.angle = 0,0,0,0
        self.bbox_x1,self.bbox_y1,self.bbox_width,self.bbox_height = 0,0,0,0
        self.flag = False
        obj = None


def go_to_next_side(robot,mult):
    # found_cube = False
    # cube1 = None
    # while not found_cube:
    #     for obj in robot.world.visible_objects:
    #         s = str(obj)[1:10]
    #         if s == "LightCube":
    #             found_cube = True
    #             cube1 = obj
    # curr_angle = cube1.pose.rotation.angle_z.degrees
    # print("current angle = {}".format(curr_angle))
    # new_angle = abs(curr_angle)+90*mult
    # if new_angle > 180:
    #     new_angle = new_angle - 180
    # robot.behavior.dock_with_cube(cube1,approach_angle=degrees(new_angle))
    # time.sleep(1)
    # robot.motors.set_wheel_motors(-50,-50)
    # time.sleep(3)
    # robot.motors.set_wheel_motors(0,0)
    # robot.behavior.set_head_angle(degrees(10.0))
    rotate(robot,90)
    robot.motors.set_wheel_motors(50,50)
    time.sleep(4)
    robot.motors.set_wheel_motors(0,0)
    rotate(robot,-90)
    robot.motors.set_wheel_motors(50,50)
    time.sleep(4)
    robot.motors.set_wheel_motors(0,0)
    rotate(robot,-90)
    found_cube = False
    cube1 = None
    while not found_cube:
        for obj in robot.world.visible_objects:
            s = str(obj)[1:10]
            if s == "LightCube":
                found_cube = True
                cube1 = obj
    dock(robot,cube1)
    robot.motors.set_wheel_motors(-50,-50)
    time.sleep(3)
    robot.motors.set_wheel_motors(0,0)
    robot.behavior.set_head_angle(degrees(10.0))


def Handle_object_seen2(robot, event_type,event,Box,cube):
    obj_name = str(event.obj)[1:10]
    num = str(event.obj)[54:56]
    if obj_name == "LightCube":
        # Box.x1,Box.y1 = int(event.image_rect.x_top_left+event.image_rect.width/5),int(event.image_rect.y_top_left-event.image_rect.height/1.5-10)
        # Box.x2,Box.y2 = int(Box.x1+event.image_rect.width/1.25),int(event.image_rect.y_top_left+event.image_rect.height/3.5-10)
        Box.x1,Box.y1 = int(event.image_rect.x_top_left+15), int(event.image_rect.y_top_left-60)
        Box.x2,Box.y2 = int(Box.x1+event.image_rect.width-10), int(Box.y1+event.image_rect.height)
        cube.x, cube.y, cube.z, cube.angle = event.obj.pose.position.x,event.obj.pose.position.y,event.obj.pose.position.z,event.obj.pose.rotation.angle_z.degrees
        cube.bbox_x1, cube.bbox_y1, cube.bbox_width, cube.bbox_height = event.image_rect.x_top_left,event.image_rect.y_top_left,event.image_rect.width,event.image_rect.height
        cube.flag = True
        cube.obj = event.obj


def search_for_letter(characters,model,BB,C1,robot,Letter):
    letter_found = False
    letter_temp = ""
    try_count = 0
    num_to_not_consider = 15
    num_need_to_pass = 5
    guessed = []
    reset = False
    while not letter_found:

        if reset:
            letter_temp = ""
            guessed = []
            reset = False
            try_count += 1
            go_to_next_side(robot,try_count)

        cv_image = cv2.cvtColor(np.array(robot.camera.latest_image.raw_image),cv2.COLOR_RGB2BGR)
        boxed = cv2.rectangle(cv_image,(BB.x1,BB.y1),(BB.x2,BB.y2),(255,0,0),2)

        roi = cv_image[BB.y1:BB.y2,BB.x1:BB.x2]

        print("area of BB = {}".format(BB.area()))
        
        try:
            cv2.imshow("roi raw",roi)
            gray = cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(gray,220,255,cv2.THRESH_BINARY)
            cv2.imshow("thresh",thresh)
            cntrs,hier = cv2.findContours(thresh,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
            extr, hier = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            blank = np.zeros_like(thresh)
            cntrs = cv2.drawContours(np.copy(blank),cntrs,-1,255,3)
            extr_cntrs = cv2.drawContours(np.copy(blank),extr,-1,255,3)
            cv2.imshow("contour",cntrs)
            cv2.imshow("external contours", extr_cntrs)
            subtracted = cntrs-extr_cntrs
            cv2.imshow("subtracted contours", subtracted)
        
            cnt, hier = cv2.findContours(subtracted,cv2.RETR_EXTERNAL ,cv2.CHAIN_APPROX_SIMPLE)
            filled = cv2.drawContours(np.copy(blank),cnt,-1,255,3)
            cv2.imshow("floodfill", filled)
            small = 0
            contour = cnt[0]
            for cont in cnt:
                area = cv2.contourArea(cont)
                if area > small:
                    small = area
                    contour = cont
            x,y,w,h = cv2.boundingRect(contour)
            region = thresh[y:y+h,x:x+w]
            cv2.imshow("Region",region)

            roi = cv2.resize(region, dsize=(28,28), interpolation=cv2.INTER_CUBIC)
            roi = np.array(roi)
            t = np.copy(roi)
            t = t / 255.0
            t = 1-t
            t = t.reshape(1,784)
            pred = use_model(model,t)
            character_guess = characters[pred[0]]
            print("Predicted character = {}".format(character_guess))
            cv2.waitKey(1)

            guessed.append(character_guess)
            if len(guessed) >= num_to_not_consider+num_need_to_pass:
                to_check = guessed[-1*num_need_to_pass:-1]
                print("\nTo check = {}\n".format(to_check))
                if len(set(to_check)) == 1:
                    letter_temp = guessed[-1]
            if letter_temp != "":
                if letter_temp == Letter:
                    letter_found = True
                else:
                    reset = True

                    
        except Exception as ex:
            print(ex)
        # input("Next")
        


def main():
    robot = av.Robot("00804458",behavior_control_level=ControlPriorityLevel.OVERRIDE_BEHAVIORS_PRIORITY,enable_custom_object_detection=True)
    robot.connect()
    robot.motors.stop_all_motors()
    robot.behavior.set_lift_height(0)
    robot.behavior.set_head_angle(degrees(10.0))
    robot.camera.init_camera_feed()

    characters = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    model = Load_Model()
    BB = Letter_Bounding_box()
    C1 = Cube()
    robot.events.subscribe(Handle_object_seen2, Events.object_observed,BB,C1)

    

    available_letters = ["A","B","C","D","A","B","C","D","A","B","C","D",]
    word = input("please input a 3 letter word from the available letters\n{}\n".format(available_letters)).upper()

    index = 2

    done_everything = False

    while not done_everything:
        robot.behavior.set_lift_height(0)
        robot.behavior.set_head_angle(degrees(10.0))
        Letter = word[index]
        found_cube = False
        rotation_count = 3
        while not found_cube:
            if rotation_count >= 0 and rotation_count <= 7:
                rotate(robot,-30)
            if rotation_count < 0 and rotation_count >= -7:
                rotate(robot,30)
            rotation_count -= 1
            if rotation_count == -8:
                rotation_count = 7

            t0 = time.time()
            while time.time()-t0 < 1:
                try:
                    for obj in robot.world.visible_objects:
                        if str(obj)[1:8] == "Charger":
                            found_cube = False
                            break
                        if str(obj)[1:10] == "LightCube":
                            found_cube = True
                        # dock_and_pick_up(robot,obj)
                        dock(robot,obj)
                except Exception as ex:
                    print(ex)
                    rotate(robot,-30)
            
    
        robot.motors.set_wheel_motors(-50,-50)
        time.sleep(3)
        robot.motors.set_wheel_motors(0,0)

        robot.behavior.set_head_angle(degrees(10.0))

        cyclce_count = 0
        while BB.area() >= 10000:
            print("area of BB = {}".format(BB.area()))
            time.sleep(2)
            if cyclce_count == 5:
                robot.motors.set_wheel_motors(-30,-30)
                time.sleep(1)
                robot.motors.set_wheel_motors(0,0)
                robot.motors.set_wheel_motors(30,30)
                time.sleep(1)
                robot.motors.set_wheel_motors(0,0)
                cyclce_count = 0
            cyclce_count += 1

            
        search_for_letter(characters, model, BB, C1, robot, Letter)

        ready_to_dock = False
        while not ready_to_dock:
            t0 = time.time()
            while time.time()-t0 < 1:
                try:
                    for obj in robot.world.visible_objects:
                        if str(obj)[1:8] == "Charger":
                            ready_to_dock = False
                            break
                        if str(obj)[1:10] == "LightCube":
                            ready_to_dock = True
                        dock_and_pick_up(robot,obj)
                except Exception as ex:
                    print(ex)
                    
        
        robot.behavior.set_lift_height(1)
        robot.behavior.set_head_angle(degrees(0.0))
        in_position = False
        while not in_position:
            robot.behavior.set_lift_height(1)
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

                if cube_in and charger_in:
                    dock(robot,cube)
                    robot.motors.set_wheel_motors(-20,-20)
                    time.sleep(7)
                    robot.motors.set_wheel_motors(0,0)
                    rotate(robot,-91)
                    time.sleep(0.5)
                    robot.motors.set_wheel_motors(-20,-20)
                    time.sleep(4.5)
                    robot.motors.set_wheel_motors(0,0)
                    in_position = True

        robot.behavior.set_lift_height(1)

        robot.behavior.set_lift_height(1)

        time.sleep(2)
        num = index + 1
        index -= 1
        robot.behavior.set_head_angle(degrees(-22))
        lines_passed = 0
        robot.motors.set_wheel_motors(10,10)
        while lines_passed < num:
            white = False
            black = False
            while not white:
                cv_image = cv2.cvtColor(np.array(robot.camera.latest_image.raw_image),cv2.COLOR_RGB2BGR)
                img = cv2.cvtColor(cv_image,cv2.COLOR_BGR2GRAY)
                ret,img = cv2.threshold(img,80,255,cv2.THRESH_BINARY)
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

        robot.behavior.set_lift_height(1)
        robot.behavior.set_head_angle(degrees(-22))

        in_spot = False
        while not in_spot:
            cv_image = cv2.cvtColor(np.array(robot.camera.latest_image.raw_image),cv2.COLOR_RGB2BGR)
            img = cv2.cvtColor(cv_image,cv2.COLOR_BGR2GRAY)
            ret,img = cv2.threshold(img,50,255,cv2.THRESH_BINARY)
            cv2.imshow("camera feed",img)
            h,w = img.shape
            h_low, h_high = 100,300
            w_low, w_high = int(w/4),int(w*3/4)
            region = img[h_low:h_high,w_low:w_high]
            cv2.imshow("region",region)
            cv2.waitKey(1)
            follow_line(robot)
            in_spot = True

        rotate(robot,90)
        robot.motors.set_wheel_motors(30,30)
        time.sleep((index+1)*3)
        robot.motors.set_wheel_motors(0,0)
        rotate(robot,90)
        if index == -1:
            done_everything = True
        

if __name__ == '__main__':
    main()