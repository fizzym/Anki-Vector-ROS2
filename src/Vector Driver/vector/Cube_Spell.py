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
from anki_vector.util import degrees, Pose
import time
import math
import logging,threading

Cube_in_sight = False
bounding_rect = [0,0,0,0]

class Custom_Pose():
    def __init__(self,pose,cube_num):
        self.x = pose.position.x
        self.y = pose.position.y
        self.z = pose.position.z
        self.a = pose.rotation.angle_z.degrees
        self.id = pose.origin_id
        self.cube_num = cube_num

class Glyph_Tracking():
    def __init__(self):
        self.faces = {} # map of all faces seen to poses of these faces "A" --> [pose1,pose2]
        self.highest_cube_num = 0

    def get_locations(self):
        locs = []
        for key in self.faces.keys():
            for pose in self.faces[key]:
                # x,y,z,a = pose.position.x,pose.position.y,pose.position.z,pose.rotation.angle_z.degrees
                x,y,z,a,n = pose.x,pose.y,pose.z,pose.a,pose.cube_num
                locs.append([key,x,y,z,a,n])
        return locs

    def letter_count(self):
        letters = {}
        for key in self.faces.keys():
            num = len(self.faces[key])
            letters[key] = num
        return letters

def angle_to_side_conversion(ra):
    # converts angle of observed face to which side it is
    # will eventually change to be matching side seen with identified letter but that algorithm has yet to be made
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

def similar_pose(p1,p2):
    xth,yth,zth,ath = 40,40,40,25
    x1,y1,z1,a1 = p1.position.x,p1.position.y,p1.position.z,p1.rotation.angle_z.degrees
    # x2,y2,z2,a2 = p2.position.x,p2.position.y,p2.position.z,p2.rotation.angle_z.degrees
    x2,y2,z2,a2 = p2.x,p2.y,p2.z,p2.a
    dx,dy,dz,da = abs(x2-x1),abs(y2-y1),abs(z2-z1),abs(a2-a1)
    if dx < xth and dy < yth and dz < zth and da < ath:
        return True
    else:
        return False

def get_cube_num(p,Glyphs):
    num = -1
    for key in Glyphs.faces.keys():
        for pose in Glyphs.faces[key]:
            if similar_pose(p,pose):
                num = pose.cube_num
    if num == -1:
        num = Glyphs.highest_cube_num + 1
        Glyphs.highest_cube_num += 1
    return num

def Symbol_Observed(robot, event_type, event,Glyphs):
    global Cube_in_sight, bounding_rect
    Cube_in_sight = True
    obj_pose = event.obj.pose
    x,y,z,a = obj_pose.position.x,obj_pose.position.y,obj_pose.position.z,obj_pose.rotation.angle_z.degrees

    robot_pose = robot.pose
    rel_a = a - robot_pose.rotation.angle_z.degrees
    side = angle_to_side_conversion(rel_a)
    if side not in Glyphs.faces:
        Glyphs.faces[side] = []
        cube_num = get_cube_num(obj_pose,Glyphs)
        Glyphs.faces[side].append(Custom_Pose(obj_pose,cube_num))
    else:
        for pose in Glyphs.faces[side]:
            if similar_pose(obj_pose,pose):
                return
        cube_num = Glyphs.highest_cube_num + 1
        Glyphs.highest_cube_num += 1
        Glyphs.faces[side].append(Custom_Pose(obj_pose,cube_num))
    
    x1,y1 = event.image_rect.x_top_left,event.image_rect.y_top_left
    x2,y2 = x1+event.image_rect.width,y1+event.image_rect.height
    bounding_rect[0],bounding_rect[1],bounding_rect[2],bounding_rect[3]= x1,y1,x2,y2

def Appeared(robot, event_type, event):
    global Cube_in_sight
    Cube_in_sight = True
    print(Cube_in_sight)

def Disappeared(robot, event_type, event):
    global Cube_in_sight
    Cube_in_sight = False


def spin(robot,angle):
    new_pose = robot.pose.define_pose_relative_this(Pose(0,0,0,angle_z=av.util.Angle(degrees=angle)))
    robot.behavior.go_to_pose(new_pose)






import signal, time, sys

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def TimedInput(timeout=0.1):
    def timeout_error(*_):
        raise TimeoutError
    signal.signal(signal.SIGALRM, timeout_error)
    signal.setitimer(signal.ITIMER_REAL,timeout)
    try:
        getch = _GetchUnix()
        answer = getch()
        signal.alarm(0)
        return answer
    except TimeoutError:   
        signal.signal(signal.SIGALRM, signal.SIG_IGN)
        return "No Entry"

def convert_to_vel(keyIn):
    speed = 75
    if keyIn == "w":
        vel = (speed,speed)
    if keyIn == "s":
        vel = (-speed,-speed)
    if keyIn == "a":
        vel = (-speed,speed)
    if keyIn == "d":
        vel = (speed,-speed)
    if keyIn != "w" and keyIn != "s" and keyIn != "a" and keyIn != "d":
        vel = (0,0)
    return vel
    
def adjust_and_dock(robot):
    global bounding_rect
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
    
        prox = robot.proximity.last_sensor_reading.distance.distance_mm
        if prox <= 30:
            docked = True
            robot.motors.set_wheel_motors(0,0)
    # sometimes sensor goes off slightly too early
    robot.motors.set_wheel_motors(20,20)
    time.sleep(1.5)
    robot.motors.set_wheel_motors(0,0)



def handle_camera(robot,event_type,event):
    img = cv2.cvtColor(np.array(robot.camera.latest_image.raw_image),cv2.COLOR_RGB2BGR)
    cv2.imshow("img",img)
    cv2.waitKey(1)


def main(args=None):
    global Cube_in_sight
    # available_letters = ["A,B,C,D"]
    # word = input("Please enter a 1 to 3 letter word to spell using these letter:\n{}".format(available_letters))
    Glyphs = Glyph_Tracking()
    robot = av.Robot("00804458",behavior_control_level=ControlPriorityLevel.OVERRIDE_BEHAVIORS_PRIORITY)
    robot.connect()
    robot.motors.stop_all_motors()
    robot.behavior.set_lift_height(0.0)
    robot.behavior.set_head_angle(degrees(10.0))

    robot.camera.init_camera_feed()
    # robot.events.subscribe(handle_camera,Events.new_raw_camera_image)
    robot.events.subscribe(handle_camera,Events.object_observed)

    # robot.events.subscribe(Symbol_Observed, Events.object_observed,Glyphs)
    while True:
        timeout = 0.1
        data = TimedInput(timeout)
        if data == "q":
            sys.exit()
        vel = convert_to_vel(data)
        robot.motors.set_wheel_motors(vel[0],vel[1])
        # print(Glyphs.p)
        # print(Glyphs.get_locations())
        # print(have_enough_letters(word,Glyphs))
        if Cube_in_sight:
            ans = input("Automatic dock? y/n\n")
            if ans == "y":
                robot.motors.set_wheel_motors(0,0)
                adjust_and_dock(robot)


def thread_test(robot):
    print("Starting Thread")
    global Cube_in_sight
    # robot.motors.set_wheel_motors(10,10)
    while True:
        if Cube_in_sight:
            break
    robot.motors.set_wheel_motors(0,0)
    print("Thread Finished")




def main2():
    global Cube_in_sight
    Glyphs = Glyph_Tracking()
    robot = av.Robot("00804458",behavior_control_level=ControlPriorityLevel.OVERRIDE_BEHAVIORS_PRIORITY)
    robot.connect()
    robot.motors.stop_all_motors()
    robot.behavior.set_lift_height(0.0)
    robot.behavior.set_head_angle(degrees(10.0))
    # robot.events.subscribe(Symbol_Observed, Events.object_observed,Glyphs)

    
    th = threading.Thread(target=thread_test,args=(robot,))
    th.start()
    while True:
        time.sleep(1)
    

if __name__ == '__main__':
    main()
    # main2()