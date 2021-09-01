#!/usr/bin/env python3
import rclpy
import numpy as np
import cv2
from matplotlib import pyplot as plt, rc
import anki_vector as av
from anki_vector.util import degrees
import time
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from rclpy.node import Node
from example_interfaces.msg import Float64
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from example_interfaces.msg import Float64MultiArray


class Publisher(Node):
    def __init__(self, topic_name, DataType, name,robot_serial):
        super().__init__(name)
        self.publisher_ = self.create_publisher(DataType, topic_name, 10)
        self.data_type = DataType
        self.robot_serial = robot_serial

class TeleopSubscriber(Node):

    def __init__(self):
        super().__init__('teleop_subscriber')
        self.subscription = self.create_subscription(Twist,'cmd_vel',self.listener_callback,10)
        self.subscription  # prevent unused variable warning
        self.center = [float(180),float(320)]
        self.msg = None

    def listener_callback(self, msg):
        self.msg = msg

class LaserSubscriber(Node):

    def __init__(self):
        super().__init__('laser_subscriber')
        self.subscription = self.create_subscription(String,'vector_proximity',self.listener_callback,10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.msg = msg
        print(msg.data)


def main(args=None):
    # take_static_image()

    rclpy.init(args=args)

    head_pub = Publisher("set_head_angle",Float64,"vector_head","00804458")
    laser_sub = LaserSubscriber()
    wheel_pub = Publisher("vector_wheel_speed",Float64MultiArray,"name","00804458")
    teleop_sub = TeleopSubscriber()

    msg = Float64()
    angle = input("Enter the angle you would like vectors head to be at in degrees:\n")
    msg.data = float(angle)
    head_pub.publisher_.publish(msg)
    time.sleep(1)
    head_pub.destroy_node()

    wheel_msg = Float64MultiArray()
    while rclpy.ok():
        rclpy.spin_once(teleop_sub,timeout_sec=0.1)
        if teleop_sub.msg is not None:
            x,y,z = float(teleop_sub.msg.linear.x), float(teleop_sub.msg.linear.y), float(teleop_sub.msg.linear.z)
            ax,ay,az = float(teleop_sub.msg.angular.x), float(teleop_sub.msg.angular.y), float(teleop_sub.msg.angular.z)
            # print("x = {}\ny = {}\nz = {}\nax = {}\nay = {}\naz = {}\n".format(x,y,z,ax,ay,az))
            if az == 0:
                speed = [50*x,50*x]
            else:
                if x == 0:
                    speed = [-50*az,50*az]
            wheel_msg.data = speed
            wheel_pub.publisher_.publish(wheel_msg)
        rclpy.spin_once(laser_sub)



    laser_sub.destroy_node()
    wheel_pub.destroy_node()
    teleop_sub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
