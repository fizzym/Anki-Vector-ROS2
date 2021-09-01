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


def Angle2Side(angle):
    side = ""
    if angle >= -45 and angle < 45:
        side = "Side 1"
    if angle >= 45 and angle < 135:
        side = "Side 2"
    if angle >= 135 or angle < -135:
        side = "Side 3"
    if angle >= -135 and angle < -45:
        side = "Side 4"
    # print("Vector is looking at side {}".format(side))
    return side


class Letter_Bounding_box():
    def __init__(self):
        self.x1,self.y1,self.x2,self.y2 = 0,0,0,0
        self.pose = Pose(0,0,0,angle_z=degrees(0))


class Cube():
    def __init__(self):
        self.x,self.y,self.z,self.angle = 0,0,0,0
        self.bbox_x1,self.bbox_y1,self.bbox_width,self.bbox_height = 0,0,0,0
        self.flag = False
        obj = None


def Angle_Fix(angle):
    new_angle = 0
    if angle >= -45 and angle < 45:
        new_angle = angle
    if angle >= 45 and angle < 135:
        new_angle = angle - 90
    if angle >= 135 or angle < -135:
        if angle < 0:
            new_angle = angle + 180
        else:
            new_angle = angle - 180
    if angle >= -135 and angle < -45:
        new_angle = angle + 90
    return new_angle


def dock(robot,num_retries):
    docked = False
    tried = False
    num_tries = 0
    while not docked:
        while not tried:
            for obj in robot.world.visible_objects:
                s = str(obj)[1:10]
                if s == "LightCube":
                    robot.behavior.dock_with_cube(obj,num_retries=2)
                    tried = True
                    num_tries += 1
                    docked = True


    robot.motors.set_wheel_motors(20,20)
    time.sleep(2)
    robot.motors.set_wheel_motors(0,0)


def rotate_and_search(robot):
    found_cube = False
    cube = None
    while not found_cube:
        robot.motors.set_wheel_motors(20,-20)
        time.sleep(1)
        robot.motors.set_wheel_motors(0,0)
        t0 = time.time()
        while time.time()-t0 < 1:
            for obj in robot.world.visible_objects:
                s = str(obj)[1:10]
                # print(s)
                if s == "LightCube":
                    found_cube = True
                    cube = obj
    return cube


def face_cube(robot,cube):
    robot.behavior.dock_with_cube(cube)
    robot.motors.set_wheel_motors(30,30)
    time.sleep(1)
    robot.motors.set_wheel_motors(-50,-50)
    time.sleep(3)
    robot.motors.set_wheel_motors(0,0)

def go_to_next_side(robot,mult):
    found_cube = False
    cube1 = None
    while not found_cube:
        for obj in robot.world.visible_objects:
            s = str(obj)[1:10]
            if s == "LightCube":
                found_cube = True
                cube1 = obj
    curr_angle = cube1.pose.rotation.angle_z.degrees
    print("current angle = {}".format(curr_angle))
    new_angle = abs(curr_angle)+90*mult
    if new_angle > 180:
        new_angle = new_angle - 180
    robot.behavior.dock_with_cube(cube1,approach_angle=degrees(new_angle))
    time.sleep(1)
    robot.motors.set_wheel_motors(-50,-50)
    time.sleep(3)
    robot.motors.set_wheel_motors(0,0)
    robot.behavior.set_head_angle(degrees(10.0))



def search_for_letter(characters,model,BB,C1,robot,Letter):
    letter_found = False
    same_letter_count = 0
    letter_temp = ""
    try_count = 0
    num_to_not_consider = 5
    count_not_consider = 0
    while not letter_found:
        if same_letter_count == 4:
            count_not_consider = 0
            print("Going to next face")
            same_letter_count = 0
            letter_temp = ""
            try_count+=1
            go_to_next_side(robot,try_count)

        cv_image = cv2.cvtColor(np.array(robot.camera.latest_image.raw_image),cv2.COLOR_RGB2BGR)
        boxed = cv2.rectangle(cv_image,(BB.x1,BB.y1),(BB.x2,BB.y2),(255,0,0),2)
        cv2.imshow("bbox",boxed)
        cv2.waitKey(1)
        input("image")

        count_not_consider += 1
        roi = cv_image[BB.y1:BB.y2,BB.x1:BB.x2]
        if roi.shape[0] > 0 and count_not_consider > num_to_not_consider:

            rois, imgs = get_rois(roi)
            if rois is not None:
                for i in range(len(rois)):
                    processed_img = rois[i]
                    img = imgs[i]
                    pred = use_model(model,processed_img)
                    character_guess = characters[pred[0]]
                    print("Predicted character = {}".format(character_guess))
                    if character_guess == letter_temp or letter_temp == "":
                        same_letter_count += 1
                    if character_guess != letter_temp:
                        same_letter_count = 0

                    letter_temp = character_guess
                    if same_letter_count == 4:
                        if letter_temp == Letter:
                            letter_found = True
        time.sleep(0.25)



def pick_up_cube(robot):
    found_cube = False
    cube1 = None
    while not found_cube:
        for obj in robot.world.visible_objects:
            s = str(obj)[1:10]
            if s == "LightCube":
                found_cube = True
                cube1 = obj
    robot.behavior.dock_with_cube(cube1)
    robot.motors.set_wheel_motors(30,30)
    time.sleep(1)
    robot.motors.set_wheel_motors(0,0)
    robot.behavior.set_lift_height(1)



    

def Handle_object_seen2(robot, event_type,event,Boxs,Box,cube):
    obj_name = str(event.obj)[1:10]
    num = str(event.obj)[54:56]
    if obj_name == "CustomObj":
        if num == "00":
            Boxs[0].x1, Boxs[0].y1, Boxs[0].x2, Boxs[0].y2 = int(event.image_rect.x_top_left),int(event.image_rect.y_top_left),int(event.image_rect.x_top_left+event.image_rect.width),int(event.image_rect.y_top_left+event.image_rect.height)
            Boxs[0].pose = event.obj.pose
        if num == "01":
            Boxs[1].x1, Boxs[1].y1, Boxs[1].x2, Boxs[1].y2 = int(event.image_rect.x_top_left),int(event.image_rect.y_top_left),int(event.image_rect.x_top_left+event.image_rect.width),int(event.image_rect.y_top_left+event.image_rect.height)
            Boxs[1].pose = event.obj.pose
        if num == "02":
            Boxs[2].x1, Boxs[2].y1, Boxs[2].x2, Boxs[2].y2 = int(event.image_rect.x_top_left),int(event.image_rect.y_top_left),int(event.image_rect.x_top_left+event.image_rect.width),int(event.image_rect.y_top_left+event.image_rect.height)
            Boxs[2].pose = event.obj.pose
        if num == "03":
            Boxs[3].x1, Boxs[3].y1, Boxs[3].x2, Boxs[3].y2 = int(event.image_rect.x_top_left),int(event.image_rect.y_top_left),int(event.image_rect.x_top_left+event.image_rect.width),int(event.image_rect.y_top_left+event.image_rect.height)
            Boxs[3].pose = event.obj.pose
    else:
        if obj_name == "LightCube":
            Box.x1,Box.y1 = int(event.image_rect.x_top_left+event.image_rect.width/5),int(event.image_rect.y_top_left-event.image_rect.height/2)
            Box.x2,Box.y2 = int(Box.x1+event.image_rect.width/1.25),int(event.image_rect.y_top_left+event.image_rect.height/4)
            cube.x, cube.y, cube.z, cube.angle = event.obj.pose.position.x,event.obj.pose.position.y,event.obj.pose.position.z,event.obj.pose.rotation.angle_z.degrees
            cube.bbox_x1, cube.bbox_y1, cube.bbox_width, cube.bbox_height = event.image_rect.x_top_left,event.image_rect.y_top_left,event.image_rect.width,event.image_rect.height
            cube.flag = True
            cube.obj = event.obj



def go_to_spot(robot,spot,BB):
    # sx,sy,sz,sa = spot.pose.position.x,spot.pose.position.y,spot.pose.position.z,spot.pose.rotation.angle_z.degrees
    # rx,ry,rz,ra = robot.pose.position.x,robot.pose.position.y,robot.pose.position.z,robot.pose.rotation.angle_z.degrees
    # x,y,z,a = rx-sx,ry-sy,rz-sz,ra-sa

    done = False
    robot.motors.set_wheel_motors(30,30)
    while not done:
        prox = robot.proximity.last_sensor_reading.distance.distance_mm
        if prox <=40:
            done = True
    time.sleep(1)
    robot.motors.set_wheel_motors(0,0)
    time.sleep(1)
    robot.motors.set_wheel_motors(-30,-30)
    time.sleep(2)
    robot.motors.set_wheel_motors(0,0)


def rotate(robot,deg):
    speed = 30
    time360 = 9.66
    with_block_multiplier = 1/1.75
    t = abs(deg)*time360/360*with_block_multiplier
    sign = deg/abs(deg)
    robot.motors.set_wheel_motors(-sign*speed,1*sign*speed)
    time.sleep(t)
    robot.motors.set_wheel_motors(0,0)

def drive_straight(robot,dist):
    speed = 30
    with_block_multiplier = 1.31
    t = abs(dist)/speed*with_block_multiplier
    sign = dist/abs(dist)
    robot.motors.set_wheel_motors(sign*speed,sign*speed)
    time.sleep(t)
    robot.motors.set_wheel_motors(0,0)

def go_to_pose(robot,pose,dist_from = 0,is_abs=False,no_x = False):
    # coord system = 
    #      x
    #      ^
    # y <--|--> -y
    #      v
    #     -x
    # positive angle is ccw
    
    x,y,z,a = pose.position.x,pose.position.y,pose.position.z,pose.rotation.angle_z.degrees
    if not is_abs:
        rx,ry,rz,ra = robot.pose.position.x,robot.pose.position.y,robot.pose.position.z,robot.pose.rotation.angle_z.degrees
        x,y,z,a = rx-x,ry-y,rz-z,a-ra
    x = x-dist_from
    # input("I am at pose\n {}\n\n and symbol is at pose\n {}\n\n".format(robot.pose,pose))
    # rotate(robot,ra)
    # input("Now I am at pose\n {}\n\n ".format(robot.pose))

    if a != 0:
        rotate(robot,a)
        time.sleep(0.5)
    if y != 0:
        sign = y/abs(y)
        rotate(robot,sign*90)
        time.sleep(0.5)
        drive_straight(robot,abs(y))
        time.sleep(0.5)
        rotate(robot,-1*sign*90)
        time.sleep(0.5)
    if x != 0 and not no_x:
        drive_straight(robot,x)
        time.sleep(0.5)
    

def which_custom_vis(robot):
    vis = []
    for obj in robot.world.visible_custom_objects:
        vis.append(int(str(obj)[54:56]))
    return vis



def face_stalls(robot):
    found = False
    charger = None
    while not found:
        robot.motors.set_wheel_motors(20,-20)
        time.sleep(1)
        robot.motors.set_wheel_motors(0,0)
        t0 = time.time()
        while time.time()-t0 < 1:
            try:
                for obj in robot.world.visible_objects:
                    s = str(obj)[1:8]
                    # print(s)
                    if s == "Charger":
                        found = True
                        charger = obj
            except Exception as ex:
                print(ex)
                robot.motors.set_wheel_motors(0,0)
    pose = charger.pose
    go_to_pose(robot,pose,dist_from=50)
    # input("done")

def make_all_stalls_visible(robot, want_vis,spot_bbs):
    visible = which_custom_vis(robot)
    # print(visible)
    all_vis = False
    if len(visible) == want_vis:
        all_vis = True
    while not all_vis:
        try:
            visible = which_custom_vis(robot)
            length = len(visible)
            lrgst = max(visible)
            smlst = min(visible)
            if length == want_vis:
                all_vis = True
                break
            if length <= want_vis-2:
                if lrgst == 3:
                    pose = Pose(-5,30,0,angle_z=degrees(0))
                else:
                    if smlst == 0:
                        pose = Pose(-5,-30,0,angle_z=degrees(0))
            else:
                if lrgst == 3:
                    pose = Pose(0,30,0,angle_z=degrees(0))
                else:
                    if smlst == 0:
                        pose = Pose(0,-30,0,angle_z=degrees(0))
            go_to_pose(robot,pose,is_abs=True)
        except Exception as ex:
            print(ex)
    

def make_want_stall_vis(robot,stall_num):
    print("in make want stall visible")
    visible = which_custom_vis(robot)
    print(visible)
    is_vis = False
    if stall_num in visible:
        is_vis = True
    while not is_vis:
        try:
            visible = which_custom_vis(robot)
            print(visible)
            if stall_num in visible:
                is_vis = True
                break
            lrgst = max(visible)
            smlst = min(visible)
            if stall_num < smlst:
                pose = Pose(-5,30,0,angle_z=degrees(0))
                go_to_pose(robot,pose,is_abs=True)
            else:
                if stall_num > lrgst:
                    pose = Pose(-5,-30,0,angle_z=degrees(0))
                    go_to_pose(robot,pose,is_abs=True)
        except Exception as ex:
            print(ex)
    print("leaving make want stall vis")



def find_stall(robot,stall_num,spot_bbs):
    colours = [(255,0,0),(0,255,0),(0,0,255),(0,255,255)]

    found = False
    while not found:
        try:
            cv_image = cv2.cvtColor(np.array(robot.camera.latest_image.raw_image),cv2.COLOR_RGB2BGR)
            drawn = np.copy(cv_image)
            visible = which_custom_vis(robot)
            # print(visible)
            # for j in range(len(spot_bbs)):
            for j in visible:
                BB = spot_bbs[j]
                col = colours[j]
                drawn = cv2.rectangle(drawn,(BB.x1,BB.y1),(BB.x2,BB.y2),col,5)
            cv2.imshow("spot",drawn)
            cv2.waitKey(1)
        except Exception as ex:
            print(ex)





    




def main(args = None):
    characters = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    model = Load_Model()
    # img = cv2.imread('A.jpg')
    BB = Letter_Bounding_box()
    C1 = Cube()
    num_spots = 4
    spot_bbs = []
    for i in range(num_spots):
        spot_bbs.append(Letter_Bounding_box())
    robot = av.Robot("00804458",behavior_control_level=ControlPriorityLevel.OVERRIDE_BEHAVIORS_PRIORITY,enable_custom_object_detection=True)
    robot.connect()
    robot.motors.stop_all_motors()
    robot.behavior.set_lift_height(0.0)
    robot.behavior.set_head_angle(degrees(10.0))
    robot.camera.init_camera_feed()
    robot.events.subscribe(Handle_object_seen2, Events.object_observed,spot_bbs,BB,C1)

    robot.world.define_custom_cube(custom_object_type=CustomObjectTypes.CustomType00,marker=CustomObjectMarkers.Circles2,size_mm = 76.2, marker_width_mm=76.2,marker_height_mm=76.2)
    robot.world.define_custom_cube(custom_object_type=CustomObjectTypes.CustomType01,marker=CustomObjectMarkers.Circles3,size_mm = 76.2, marker_width_mm=76.2,marker_height_mm=76.2)
    robot.world.define_custom_cube(custom_object_type=CustomObjectTypes.CustomType02,marker=CustomObjectMarkers.Circles4,size_mm = 76.2, marker_width_mm=76.2,marker_height_mm=76.2)
    robot.world.define_custom_cube(custom_object_type=CustomObjectTypes.CustomType03,marker=CustomObjectMarkers.Circles5,size_mm = 76.2, marker_width_mm=76.2,marker_height_mm=76.2)
    
    

    # time.sleep(3)
    Letter = input("\n\nWhich letter would you like to search for?\n")
    # Number = input("\nWhich parking spot would you like to place the letter?\n")


    

    cube = rotate_and_search(robot)
    face_cube(robot,cube)
    robot.behavior.set_head_angle(degrees(10.0))
    time.sleep(1)

    search_for_letter(characters,model,BB,C1,robot,Letter)
    pick_up_cube(robot)

    robot.behavior.set_head_angle(degrees(-5.0))
    
    while True:
        try:
            num = int(input("Which stall number would you like to drop cube off at?\n"))
            if num >= 0 and num <= 3:
                visible = which_custom_vis(robot)
                if len(visible) == 0 or num not in visible:
                    face_stalls(robot)
                    time.sleep(0.5)
                    t0 = time.time()
                    while time.time() - t0 < 10:
                        colours = [(255,0,0),(0,255,0),(0,0,255),(0,255,255)]
                        try:
                            cv_image = cv2.cvtColor(np.array(robot.camera.latest_image.raw_image),cv2.COLOR_RGB2BGR)
                            drawn = np.copy(cv_image)
                            visible = which_custom_vis(robot)
                            for j in visible:
                                BB = spot_bbs[j]
                                col = colours[j]
                                drawn = cv2.rectangle(drawn,(BB.x1,BB.y1),(BB.x2,BB.y2),col,5)
                            cv2.imshow("spot",drawn)
                            cv2.waitKey(1)
                        except Exception as ex:
                            print(ex)
                #     make_want_stall_vis(robot,1)
                #     time.sleep(0.5)
                BB = spot_bbs[num]
                pose = BB.pose
                go_to_pose(robot,pose,dist_from=210,no_x=True)
                time.sleep(0.5)
                robot.behavior.set_lift_height(0)
                time.sleep(0.5)
                robot.motors.set_wheel_motors(-50,-50)
                time.sleep(1)
                robot.motors.set_wheel_motors(0,0)
        except Exception as ex:
            print(ex)
    
    # at_spot = False
    # H,W = 360,640
    # robot.motors.set_wheel_motors(10,10)
    # t0 = time.time()
    # while not at_spot:
    #     if len(spot_bbs) > 0:
    #         BB = spot_bbs[0]
    #         angle = BB.pose.rotation.angle_z.degrees
    #         xc,yc = int((BB.x1+BB.x2)/2),int((BB.y1+BB.y2)/2)
    #         dx,dy = (W/2)-xc,(H/2)-yc
    #         print("\ndx = {}, dy = {}\nangle = {}\n".format(dx,dy,angle))
    #         try:
    #             cv_image = cv2.cvtColor(np.array(robot.camera.latest_image.raw_image),cv2.COLOR_RGB2BGR)
    #             drawn = np.copy(cv_image)
    #             visible = which_custom_vis(robot)
    #             for j in visible:
    #                 BB = spot_bbs[j]
    #                 drawn = cv2.rectangle(drawn,(BB.x1,BB.y1),(BB.x2,BB.y2),(255,0,0),5)
    #             cv2.imshow("spots",drawn)
    #             cv2.waitKey(1)
    #         except Exception as ex:
    #             print(ex)
    #         # input("\nNext iteration\n")
    #     if time.time()-t0 > 30:
    #         break
    # robot.motors.set_wheel_motors(0,0)

if __name__ == '__main__':
    main()