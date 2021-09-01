#!/usr/bin/env python3
from os import wait
from tensorflow.keras.models import load_model
from tensorflow.keras.models import model_from_json
import time

import cv2
import numpy as np
from matplotlib import pyplot as plt
import math


import anki_vector as av
from anki_vector.events import Events
from anki_vector.util import degrees, Pose
from anki_vector.connection import ControlPriorityLevel
from anki_vector.messaging import behavior_pb2
from anki_vector.messaging.shared_pb2 import Event

from vector_letter_recog_test import Load_Model, get_rois, use_model


class Letter_Bounding_box():
    def __init__(self):
        self.x1,self.y1,self.x2,self.y2 = 0,0,0,0

class Cube():
    def __innit__(self):
        self.x,self.y,self.z,self.angle = 0,0,0,0
        self.bbox_x1,self.bbox_y1,self.bbox_width,self.bbox_height = 0,0,0,0
        self.flag = False

def Handle_cube_seen(robot, event_type,event,Box,cube):
    Box.x1,Box.y1 = int(event.image_rect.x_top_left+event.image_rect.width/5),int(event.image_rect.y_top_left-event.image_rect.height/2)
    Box.x2,Box.y2 = int(Box.x1+event.image_rect.width/1.25),int(event.image_rect.y_top_left+event.image_rect.height/4)
    cube.x, cube.y, cube.z, cube.angle = event.obj.pose.position.x,event.obj.pose.position.y,event.obj.pose.position.z,event.obj.pose.rotation.angle_z.degrees
    cube.bbox_x1, cube.bbox_y1, cube.bbox_width, cube.bbox_height = event.image_rect.x_top_left,event.image_rect.y_top_left,event.image_rect.width,event.image_rect.height
    cube.flag = True

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
    # print("Vector is looking at side {}".format(side))
    return new_angle

def straighten(robot,cube):
    x,y,z,a = cube.x,cube.y,cube.z,Angle_Fix(cube.angle)
    yp = -1*(x*math.tan(a*math.pi/180))+y
    ap = a
    prev_pose = robot.pose
    new_pose = prev_pose.define_pose_relative_this(Pose(0,yp,0,angle_z=av.util.Angle(degrees=ap)))
    # print("Was at pose {}\n".format(prev_pose))
    # print("Going to pose {}\n".format(new_pose))
    # input("Because cube is at this: relative to me:\nx = {}, y = {}, a = {}".format(x,y,a))
    robot.behavior.go_to_pose(new_pose)

def go_to_next_face(robot,cube):
    x = cube.x
    d = x + 15
    curr_pose = robot.pose
    pose_1 = curr_pose.define_pose_relative_this(Pose(0,d,0,angle_z=av.util.Angle(degrees=0)))
    # print("Was at pose {}\n".format(curr_pose))
    # print("Going to pose {}\n".format(pose_1))
    robot.behavior.go_to_pose(pose_1)
    curr_pose = robot.pose
    pose_2 = curr_pose.define_pose_relative_this(Pose(d,0,0,angle_z=av.util.Angle(degrees=-90)))
    # print("Was at pose {}\n".format(curr_pose))
    # print("Going to pose {}\n".format(pose_2))
    robot.behavior.go_to_pose(pose_2)

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


    
def lift_and_drop(robot):
    robot.behavior.set_lift_height(1)
    time.sleep(5)
    robot.behavior.set_lift_height(0)

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
                if s == "LightCube":
                    found_cube = True
                    cube = obj
    return cube

def lift_and_put_on_other(robot):
    robot.behavior.set_lift_height(1)
    time.sleep(1)
    cube = rotate_and_search(robot)
    robot.behavior.dock_with_cube(cube)
    time.sleep(0.5)
    robot.behavior.set_lift_height(0.7)
    time.sleep(1)
    robot.motors.set_wheel_motors(-50,-50)
    time.sleep(1)
    robot.motors.set_wheel_motors(0,0)
    robot.behavior.set_lift_height(0)



def main(args = None):
    characters = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    model = Load_Model()
    # img = cv2.imread('A.jpg')

    BB = Letter_Bounding_box()
    C1 = Cube()
    robot = av.Robot("00804458",behavior_control_level=ControlPriorityLevel.OVERRIDE_BEHAVIORS_PRIORITY)
    robot.connect()
    robot.motors.stop_all_motors()
    robot.behavior.set_lift_height(0.0)
    robot.behavior.set_head_angle(degrees(0.0))
    robot.camera.init_camera_feed()
    robot.events.subscribe(Handle_cube_seen, Events.object_observed,BB,C1)

    time.sleep(3)
    Letter = input("\n\nWhich letter would you like to search for?\n")

    t0 = time.time()
    while time.time()-t0 < 10:
        if C1.flag:
            straighten(robot,C1)
            break


    letter_found = False
    same_letter_count = 0
    letter_temp = ""
    loop_count = 0
    while not letter_found:
        if same_letter_count == 4:
            print("Going to next face")
            same_letter_count = 0
            letter_temp = ""
            go_to_next_face(robot,C1)

        cv_image = cv2.cvtColor(np.array(robot.camera.latest_image.raw_image),cv2.COLOR_RGB2BGR)
        if BB.x2-BB.x1 > 0 and BB.y2-BB.y1 >0:
            roi = cv_image[BB.y1:BB.y2,BB.x1:BB.x2]
            if roi is not None:
                try:
                    rois, imgs = get_rois(roi)
                except Exception as ex:
                    print(ex)
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
    
    robot.motors.set_wheel_motors(-30,-30)
    time.sleep(1)
    robot.motors.set_wheel_motors(0,0)
    dock(robot,3)
    time.sleep(1)
    # lift_and_drop(robot)
    lift_and_put_on_other(robot)
    input("Done")

if __name__ == '__main__':
    main()