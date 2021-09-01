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

    def vector_connect_callback(self, request, response):
        self.get_logger().info("Incoming request to connect to: {}".format(request.serial))
        robot = av.Robot(request.serial)
        try:
            robot.connect()
            response.success = robot.conn._has_control
            response.message = "Succesfully connected to robot {}".format(request.serial)
            robot_serial_map[request.serial] = robot
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


def command_head(HeadSub):
    if HeadSub.robot is not None:
        HeadSub.robot.motors.set_head_motor(HeadSub.data)
def command_lift(LiftSub):
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

def main(args = None):
    print("In main bby")
    rclpy.init(args=args)

    connect_srv = VectorConnectionService("vec_conn_srv","vector_connect")
    # going to need to fix this block so that it instantiates these Publishers whenever a new vector is connected automatically
    # topic names etc will need to be auto generated, probably use robot serial for differentiating
    acceleration_pub = Publisher("vector_acc","acc","vector_acc_"+"00804458","00804458")
    gyro_pub = Publisher("vector_gyro","gyro","vector_gyro_"+"00804458","00804458")
    pose_pub = Publisher("vector_current_pose","pose","vector_current_pose_"+"00804458","00804458")
    proximity_pub = Publisher("vector_proximity","prox","vector_proximity_"+"00804458","00804458")
    head_pub = Publisher("vector_current_head","head","vector_current_head_"+"00804458","00804458")
    lift_pub = Publisher("vector_current_lift","lift","vector_current_lift_"+"00804458","00804458")
    camera_pub = CameraPublisher("vector_camera","cam","vector_camera_"+"00804458","00804458")

    head_sub = Subscriber("vector_head_angle",Float64,"vector_head_angle_"+"00804458","00804458")
    head_angle_sub = Subscriber("set_head_angle",Float64,"set_head_angle_"+"00804458","00804458")
    lift_sub = Subscriber("vector_lift_height",Float64,"vector_lift_height_"+"00804458","00804458")
    wheel_sub = Subscriber("vector_wheel_speed",Float64MultiArray,"vector_wheel_speed_"+"00804458","00804458")
    speaker_srv = VectorSpeakService("vector_speaker","vector_speaker_"+"00804458","00804458")
    # # # face_sub = Subscriber("vector_face",Image,"vector_face_"+"00804458","00804458")
    # # pose_sub = Subscriber("vector_pose",Float64MultiArray,"vector_pose_"+"00804458","00804458")

    while rclpy.ok():
        rclpy.spin_once(connect_srv,timeout_sec=0)

        rclpy.spin_once(acceleration_pub)
        rclpy.spin_once(gyro_pub)
        rclpy.spin_once(pose_pub)
        rclpy.spin_once(proximity_pub)
        rclpy.spin_once(head_pub)
        rclpy.spin_once(lift_pub)
        rclpy.spin_once(camera_pub)

        rclpy.spin_once(head_sub,timeout_sec=0.001)
        rclpy.spin_once(head_angle_sub,timeout_sec=0.001)
        rclpy.spin_once(lift_sub,timeout_sec=0.001)
        rclpy.spin_once(wheel_sub,timeout_sec=0.001)
        rclpy.spin_once(speaker_srv,timeout_sec=0.001)
        # rclpy.spin_once(face_sub,timeout_sec=0.001)
        # rclpy.spin_once(pose_sub,timeout_sec=0.001)

        if head_sub.data == 69.69:
            break
    
        command_head(head_sub)
        set_head(head_angle_sub)
        command_lift(lift_sub)
        command_wheels(wheel_sub)


    
    # rclpy.spin_once(connect_srv)
    # rclpy.spin(camera_pub)
        

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
