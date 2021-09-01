#!/usr/bin/env python3
from PIL.Image import new
from anki_vector.connection import ControlPriorityLevel
from anki_vector.messaging import behavior_pb2
from anki_vector.messaging.shared_pb2 import Event
import numpy as np
import cv2
from matplotlib import pyplot as plt
import glob

import anki_vector as av
from anki_vector.events import Events
from anki_vector.util import degrees, Pose
import time
import math

rcp = [0,0,0,0,""] # relative cube position
cube_seen = False
bounding_rect = [0,0,0,0]
observed_obj = None
original_pose  = None

def angle_to_side_conversion(ra):
    side = "Unknown"
    if ra >= -45 and ra < 45:
        side = "A"
    if ra >= 45 and ra < 135:
        side = "B"
    if ra >= 135 or ra < -135:
        side = "C"
    if ra >= -135 and ra < -45:
        side = "D"
    # print("Vector is looking at side {}".format(side))
    return side

def handle_object_disappeared(robot,event_type,event):
    global cube_seen
    cube_seen = False

def handle_object_observed(robot, event_type, event):
    global rcp, cube_seen, bounding_rect, observed_obj
    observed_obj = event.obj
    robot_pose = robot.pose
    obj_pose = event.obj.pose
    relative_x = obj_pose.position.x - robot_pose.position.x - 30 # the 30 is to adjust to cube face distance nt cube center
    relative_y = obj_pose.position.y - robot_pose.position.y
    relative_z = obj_pose.position.z - robot_pose.position.z
    relative_angle = obj_pose.rotation.angle_z.degrees - robot_pose.rotation.angle_z.degrees
    side = angle_to_side_conversion(relative_angle)

    rcp[0], rcp[1], rcp[2], rcp[3], rcp[4] = relative_x, relative_y, relative_z, relative_angle, side
    cube_seen = True
    x1,y1 = event.image_rect.x_top_left,event.image_rect.y_top_left
    x2,y2 = x1+event.image_rect.width,y1+event.image_rect.height
    # print("Object y = {}\nrobot y = {}\n".format(obj_pose.position.y,robot_pose.position.y))
    # print("Event sees cube at x = {}, y = {}\n".format(obj_pose.position.x,obj_pose.position.y))
    # print("Object is located at:\nX = {}\nY = {}\nZ = {}\nA = {}\n\n".format(obj_pose.position.x,obj_pose.position.y,obj_pose.position.z,obj_pose.rotation.angle_z.degrees))

    # cv_image = cv2.cvtColor(np.array(robot.camera.latest_image.raw_image),cv2.COLOR_RGB2BGR)
    # cv2.rectangle(cv_image,(int(x1),int(y1)),(int(x2),int(y2)),0,2,cv2.LINE_8)
    # cv2.imshow("camera feed",cv_image)
    # cv2.waitKey(1)
    bounding_rect[0],bounding_rect[1],bounding_rect[2],bounding_rect[3]= x1,y1,x2,y2
    # print(bounding_rect)


def straighten(robot,cube_pos):
    global observed_obj, original_pose
    obj_pose = observed_obj.pose
    x,y,z,a = obj_pose.position.x,obj_pose.position.y,obj_pose.position.z,obj_pose.rotation.angle_z.degrees
    curr_face = angle_to_side_conversion(obj_pose.rotation.angle_z.degrees)
    face_angle_adjust = {"A":0,"B":90,"C":180,"D":-90}
    print("Current face = {}".format(curr_face))
    a = a-face_angle_adjust[curr_face]
    if a > 360:
        a = a-360
    if a <-360:
        a = a+360
    yp = -1*(x*math.tan(a*math.pi/180))+y
    ap = -a
    prev_pose = robot.pose
    new_pose = prev_pose.define_pose_relative_this(Pose(0,yp,0,angle_z=av.util.Angle(degrees=-1*(ap))))
    print("Was at pose {}\n".format(prev_pose))
    print("Going to pose {}\n".format(new_pose))
    input("Because cube is at this: relative to me:\nx = {}, y = {}, a = {}".format(x,y,a))
    robot.behavior.go_to_pose(new_pose)
    # print("At Pose:\n{}\n".format(robot.pose))
 
    
def align_with_face(robot,face):
    global rcp
    rel_x,rel_y,rel_z,rel_a,curr_face = rcp[0],rcp[1],rcp[2],rcp[3],rcp[4]
    curr_pose = robot.pose
    if curr_face == face:
        # straighten(robot,rcp)
        print("Already looking at face {}".format(face))
        return
    face_vals = {"A":0,"B":1,"C":2,"D":3}
    df = face_vals[curr_face] - face_vals[face]
    if df == 3:
        df = -1
    if df == -3:
        df = 1

    d = rel_x + 15
    if df == -1:
        print("was at pose {}".format(curr_pose))
        pose_1 = curr_pose.define_pose_relative_this(Pose(0,d,0,angle_z=av.util.Angle(degrees=0)))
        # pose_1 = Pose(curr_pose.position.x,curr_pose.position.y+d,curr_pose.position.z,curr_pose.position.z,angle_z=av.util.Angle(degrees=curr_pose.rotation.angle_z.degrees))
        print("going to pose {}".format(pose_1))
        robot.behavior.go_to_pose(pose_1)
        curr_pose = robot.pose
        pose_2 = curr_pose.define_pose_relative_this(Pose(d,0,0,angle_z=av.util.Angle(degrees=-90)))
        # pose_2 = Pose(curr_pose.position.x+d,curr_pose.position.y,curr_pose.position.z,curr_pose.position.z,angle_z=av.util.Angle(degrees=curr_pose.rotation.angle_z.degrees-90))
        print("going to pose {}".format(pose_2))
        robot.behavior.go_to_pose(pose_2)

    if df == 1:
        print("was at pose {}".format(curr_pose))
        pose_1 = curr_pose.define_pose_relative_this(Pose(0,-d,0,angle_z=av.util.Angle(degrees=0)))
        # pose_1 = Pose(curr_pose.position.x,curr_pose.position.y-d,curr_pose.position.z,curr_pose.position.z,angle_z=av.util.Angle(degrees=curr_pose.rotation.angle_z.degrees))
        print("going to pose {}".format(pose_1))
        robot.behavior.go_to_pose(pose_1)
        curr_pose = robot.pose
        pose_2 = curr_pose.define_pose_relative_this(Pose(d,0,0,angle_z=av.util.Angle(degrees=90)))
        # pose_2 = Pose(curr_pose.position.x+d,curr_pose.position.y,curr_pose.position.z,curr_pose.position.z,angle_z=av.util.Angle(degrees=curr_pose.rotation.angle_z.degrees+90))
        print("going to pose {}".format(pose_2))
        robot.behavior.go_to_pose(pose_2)

    if df == -2 or df == 2:
        print("was at pose {}".format(curr_pose))
        pose_1 = curr_pose.define_pose_relative_this(Pose(0,d,0,angle_z=av.util.Angle(degrees=0)))
        # pose_1 = Pose(curr_pose.position.x,curr_pose.position.y+d,curr_pose.position.z,curr_pose.position.z,angle_z=av.util.Angle(degrees=curr_pose.rotation.angle_z.degrees))
        print("going to pose {}".format(pose_1))
        robot.behavior.go_to_pose(pose_1)
        curr_pose = robot.pose
        pose_2 = curr_pose.define_pose_relative_this(Pose(2*d,0,0,angle_z=av.util.Angle(degrees=0)))
        # pose_2 = Pose(curr_pose.position.x+(2*d),curr_pose.position.y,curr_pose.position.z,curr_pose.position.z,angle_z=av.util.Angle(degrees=curr_pose.rotation.angle_z.degrees))
        print("going to pose {}".format(pose_2))
        robot.behavior.go_to_pose(pose_2)
        curr_pose = robot.pose
        pose_3 = curr_pose.define_pose_relative_this(Pose(0,-d,0,angle_z=av.util.Angle(degrees=-180)))
        # pose_3 = Pose(curr_pose.position.x,curr_pose.position.y-d,curr_pose.position.z,curr_pose.position.z,angle_z=av.util.Angle(degrees=curr_pose.rotation.angle_z.degrees-180))
        print("going to pose {}".format(pose_3))
        robot.behavior.go_to_pose(pose_3)

    # reverse to get better view
    robot.motors.set_wheel_motors(-50,-50)
    time.sleep(1)
    robot.motors.set_wheel_motors(0,0)
       


def set_pose_test(robot,test,test_val):
    prev_pose = robot.pose
    if test == "x":
        new_pose = Pose(prev_pose.position.x+test_val,prev_pose.position.y,prev_pose.position.z,angle_z=av.util.Angle(degrees=prev_pose.rotation.angle_z.degrees))
    else:
        if test == "y":
            new_pose = Pose(prev_pose.position.x,prev_pose.position.y+test_val,prev_pose.position.z,angle_z=av.util.Angle(degrees=prev_pose.rotation.angle_z.degrees))
    robot.behavior.go_to_pose(new_pose)

def adjust_and_dock(robot):
    global bounding_rect, observed_obj
    H,W = 360,640
    base_speed = 30
    kp = 0.9
    docked = False
    while not docked:
        xc = (bounding_rect[0]+bounding_rect[2])/2
        # print("xc = {}".format(xc))
        dx = int(xc - W/2)
        print("dx = {}".format(dx))
        k = 1-abs(dx/(W/2))

        k = k*kp
        if dx > 0:
            # input("would set to ({},{})".format(base_speed,base_speed*k))
            robot.motors.set_wheel_motors(base_speed,base_speed*k)
        else:
            if dx < 0:
                # input("would set to ({},{})".format(base_speed*k,base_speed))
                robot.motors.set_wheel_motors(base_speed*k,base_speed)
            else:
                if dx == 0:
                    # input("would set to ({},{})".format(base_speed,base_speed))
                    robot.motors.set_wheel_motors(base_speed,base_speed)
        
        # print(observed_obj.pose)
        # print(bounding_rect)
        prox = robot.proximity.last_sensor_reading.distance.distance_mm
        if prox <= 30:
            docked = True
            robot.motors.set_wheel_motors(0,0)
    # sometimes sensor goes off slightly too early
    robot.motors.set_wheel_motors(20,20)
    time.sleep(1.5)
    robot.motors.set_wheel_motors(0,0)

def pick_up(robot):
    robot.motors.set_lift_motor(0.5)
    time.sleep(3)
    robot.motors.set_lift_motor(0)

def put_down(robot):
    robot.motors.set_lift_motor(-0.5)
    time.sleep(3)
    robot.motors.set_lift_motor(0)

def main(args = None):
    global rcp, cube_seen, bounding_rect, original_pose

    robot = av.Robot("00804458",behavior_control_level=ControlPriorityLevel.OVERRIDE_BEHAVIORS_PRIORITY)
    robot.connect()
    original_pose = robot.pose
    robot.events.subscribe(handle_object_observed, Events.object_observed)
    # robot.events.subscribe(handle_object_disappeared,Events.object_disappeared)
    # If necessary, move Vector's Head and Lift down
    robot.behavior.set_lift_height(0.0)
    robot.behavior.set_head_angle(degrees(10.0))
    
    robot.camera.init_camera_feed()
    robot.behavior.set_head_angle(degrees(10.0))
    # while True:
    #     a = 5
    i = 0
    while True:
        if i >= 100:
            ans = input("Align with face? A,B,C,D?")
            if ans == "A" or ans == "B" or ans == "C" or ans == "D":
                align_with_face(robot,ans)
                ans = input("Straighten? y/n")
                if ans == "y":
                    straighten(robot,rcp)
                    ans = input("Dock? y/n")
                    if ans == "y":
                        adjust_and_dock(robot)
                        ans = input("Pick up? y/n")
                        if ans == "y":
                            pick_up(robot)
                        ans = input("Put down? y/n")
                        if ans == "y":
                            put_down(robot)
        i += 1
    # while True:
    #     # set_pose_test(robot,"x",100)
    #     again = input("Again?")
    #     if again == "y":
    #         xORy = input("Direction\n")
    #         value = input("Distance\n")
    #         set_pose_test(robot,xORy,float(value))
    #     else:
    #         break
    


if __name__ == '__main__':
    main()