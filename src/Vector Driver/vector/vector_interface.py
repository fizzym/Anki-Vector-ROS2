#!/usr/bin/env python3

import anki_vector as av
from anki_vector.util import degrees
import rclpy
from rclpy.node import Node
from vector.srv import VectorConnect
from vector.srv import VectorSpeak
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np
from example_interfaces.msg import Float64MultiArray
from example_interfaces.msg import Float64
import time

import cProfile, pstats


robot_serial_map = {} # global variable map of serial# --> robot object


class VectorConnectionService(Node):
    def __init__(self,name,topic):
        super().__init__(name)
        self.srv = self.create_service(VectorConnect, topic, self.vector_connect_callback)
        self.new_connection = False
        self.serial = ""

    def vector_connect_callback(self, request, response):
        self.get_logger().info("Incoming request to connect to: {}".format(request.serial))
        robot = av.Robot(request.serial)
        try:
            robot.connect()
            response.success = robot.conn._has_control
            response.message = "Succesfully connected to robot {}".format(request.serial)
            robot_serial_map[request.serial] = robot
            self.new_connection = True
            self.serial = request.serial
        except:
            response.success = robot.conn._has_control
            response.message = "Failed to connect to robot {}".format(request.serial)
        return response


class Publisher(Node):
    def __init__(self, topic_name, data_type,name,robot_serial):
        super().__init__(name)
        self.publisher_ = self.create_publisher(String, topic_name, 10)
        timer_period = 0.01 # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.data_type = data_type
        self.robot_serial = robot_serial
        self.robot = None

    def timer_callback(self):
        if self.robot_serial in robot_serial_map:
            if self.robot is None:
                self.robot = robot_serial_map[self.robot_serial]
            msg = String()
            if self.data_type == "acc":
                msg.data = str(self.robot.accel)
            if self.data_type == "gyro":
                msg.data = str(self.robot.gyro)
            if self.data_type == "pose":
                msg.data = str(self.robot.pose)
            if self.data_type == "prox":
                msg.data = str(self.robot.proximity.last_sensor_reading.distance)
            if self.data_type == "head":
                msg.data = str(self.robot.head_angle_rad)
            if self.data_type == "lift":
                msg.data = str(self.robot.lift_height_mm)
            if self.data_type == "cliff":
                msg.data = str(self.robot.status.is_cliff_detected)
            if self.data_type == "cap":
                msg.data = str(self.robot.touch.last_sensor_reading.raw_touch_value)
            self.publisher_.publish(msg)
            # self.get_logger().info('Publishing: "%s"' % msg.data)


class CameraPublisher(Node):
    def __init__(self, topic_name, data_type,name,robot_serial):
        super().__init__(name)
        self.publisher_ = self.create_publisher(Image, topic_name, 10)
        timer_period = 0.01 # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.data_type = data_type
        self.robot_serial = robot_serial
        self.bridge = CvBridge()
        self.robot = None
        self.camera_init = False

    def timer_callback(self):
        if self.robot_serial in robot_serial_map:
            if self.robot is None:
                self.robot = robot_serial_map[self.robot_serial]
                self.robot.camera.init_camera_feed()
            self.cv_image = cv2.cvtColor(np.array(self.robot.camera.latest_image.raw_image),cv2.COLOR_RGB2BGR)
            # self.resize()
            self.publisher_.publish(self.bridge.cv2_to_imgmsg(np.array(self.cv_image), "bgr8"))

    def resize(self):
        scale_percent = 8
        width = int(self.cv_image.shape[1]*scale_percent/100)
        height = int(self.cv_image.shape[0]*scale_percent/100)
        dim = (width,height)
        resized = cv2.resize(self.cv_image,dim,interpolation=cv2.INTER_AREA)
        self.cv_image = resized


class Subscriber(Node):
    def __init__(self,topic_name,Data_Type,name,robot_serial):
        super().__init__(name)
        self.subscription = self.create_subscription(Data_Type,topic_name,self.listener_callback,10)
        self.subscription  # prevent unused variable warning
        self.robot_serial = robot_serial
        self.robot = None
        self.data = None
        self.name = name

    def listener_callback(self, msg):
        if self.robot_serial in robot_serial_map:
            if self.robot is None:
                self.robot = robot_serial_map[self.robot_serial]
            self.data = msg.data
        # self.get_logger().info("I heard: {}".format(msg.data))

class VectorSpeakService(Node):
    def __init__(self,topic,name,robot_serial):
        super().__init__(name)
        self.srv = self.create_service(VectorSpeak, topic, self.vector_speak_callback)
        self.robot_serial = robot_serial
        self.robot = None

    def vector_speak_callback(self, request, response):
        if self.robot_serial in robot_serial_map:
            if self.robot is None:
                self.robot = robot_serial_map[self.robot_serial]
            try:
                self.robot.behavior.say_text(request.message)
                response.success = True
            except:
                response.success = False
        return response

def command_head_speed(HeadSub):
    if HeadSub.robot is not None:
        HeadSub.robot.motors.set_head_motor(HeadSub.data)
def command_lift_speed(LiftSub):
    if LiftSub.robot is not None:
        LiftSub.robot.motors.set_lift_motor(LiftSub.data)
# def command_pose(PoseSub):
def command_wheels(WheelSub):
    if WheelSub.robot is not None:
        WheelSub.robot.motors.set_wheel_motors(WheelSub.data[0],WheelSub.data[1])
# def command_face(FaceSub):
def set_head(HeadAngleSub):
    if HeadAngleSub.robot is not None:
        HeadAngleSub.robot.behavior.set_head_angle(degrees(HeadAngleSub.data))
def set_lift(LiftHeightSub):
    print("")
def set_pose(PoseSub):
    print("")

def execute_commands(Subs):
    for sub in Subs:
        if sub.name.startswith("vector_wheel_speed"):
            command_wheels(sub)


def main(args = None):
    print("In main bby")
    rclpy.init(args=args)
    all_pub = []
    all_sub = []

    connect_srv = VectorConnectionService("vec_conn_srv","vector_connect")
    
    while rclpy.ok():
        rclpy.spin_once(connect_srv,timeout_sec=0)
        if connect_srv.new_connection:
            acceleration_pub = Publisher("acc_"+connect_srv.serial,"acc","vector_acc_"+connect_srv.serial,connect_srv.serial)
            gyro_pub = Publisher("gyro_"+connect_srv.serial,"gyro","vector_gyro_"+connect_srv.serial,connect_srv.serial)
            pose_pub = Publisher("pose_read_"+connect_srv.serial,"pose","vector_pose_read_"+connect_srv.serial,connect_srv.serial)
            proximity_pub = Publisher("proximity_"+connect_srv.serial,"prox","vector_proximity_"+connect_srv.serial,connect_srv.serial)
            head_pub = Publisher("head_read_"+connect_srv.serial,"head","vector_head_read_"+connect_srv.serial,connect_srv.serial)
            lift_pub = Publisher("lift_read_"+connect_srv.serial,"lift","vector_lift_read_"+connect_srv.serial,connect_srv.serial)
            camera_pub = CameraPublisher("camera_"+connect_srv.serial,"cam","vector_camera_"+connect_srv.serial,connect_srv.serial)
            cliff_pub = Publisher("cliff_"+connect_srv.serial,"cliff","vector_cliff_"+connect_srv.serial,connect_srv.serial)
            cap_pub = Publisher("capacitance_"+connect_srv.serial,"cap","vector_capacitance_"+connect_srv.serial,connect_srv.serial)

            head_sub = Subscriber("head_speed_write_"+connect_srv.serial,Float64,"vector_head_speed_write+"+connect_srv.serial,connect_srv.serial)
            head_angle_sub = Subscriber("head_angle_write_"+connect_srv.serial,Float64,"vector_head_angle_write+"+connect_srv.serial,connect_srv.serial)
            lift_sub = Subscriber("lift_speed_write_"+connect_srv.serial,Float64,"lift_speed_write_"+connect_srv.serial,connect_srv.serial)
            lift_height_sub = Subscriber("lift_height_write_"+connect_srv.serial,Float64,"lift_height_write_"+connect_srv.serial,connect_srv.serial)
            wheel_sub = Subscriber("wheel_speed_write_"+connect_srv.serial,Float64MultiArray,"vector_wheel_speed_write_"+connect_srv.serial,connect_srv.serial)
            # speaker_srv = VectorSpeakService("speaker_"+connect_srv.serial,"vector_speaker_"+connect_srv.serial,connect_srv.serial)
            # face_sub = Subscriber("face_write_"+connect_srv.serial,Image,"vector_face_"+connect_srv.serial,connect_srv.serial)
            # pose_sub = Subscriber("pose_write_"+connect_srv.serial,Float64MultiArray,"vector_pose_write_"+connect_srv.serial,connect_srv.serial)
            all_pub.append(acceleration_pub)
            all_pub.append(gyro_pub)
            all_pub.append(pose_pub)
            all_pub.append(proximity_pub)
            all_pub.append(head_pub)
            all_pub.append(lift_pub)
            all_pub.append(camera_pub)
            all_pub.append(cliff_pub)
            all_pub.append(cap_pub)
            all_sub.append(head_sub)
            all_sub.append(head_angle_sub)
            all_sub.append(lift_sub)
            all_sub.append(lift_height_sub)
            all_sub.append(wheel_sub)
            # all_sub.append(speaker_srv)
            # all_sub.append(face_sub)
            # all_sub.append(pose_sub)
            # reset the connection node flag so that new pub/sub nodes are not created without request
            connect_srv.new_connection = False

        for pub in all_pub:
            rclpy.spin_once(pub)
        for sub in all_sub:
            rclpy.spin_once(sub,timeout_sec=0.001)

        execute_commands(all_sub)
        

    rclpy.shutdown()


if __name__ == '__main__':
    # main()
    profiler = cProfile.Profile()
    profiler.enable()
    main()
    profiler.disable()
    # stats = pstats.Stats(profiler).sort_stats('ncalls')
    # stats.print_stats()
    with open("/home/fizzer/Documents/cProfile_Vector_Stats/content/interface_data.txt", "w") as f:
        stats = pstats.Stats(profiler,stream=f).sort_stats('ncalls')
        stats.print_stats()
    f.close()
