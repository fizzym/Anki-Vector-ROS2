#!/usr/bin/env python3
import sys

from vector.srv import VectorConnect
from vector.srv import VectorSpeak
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np
from example_interfaces.msg import Float64MultiArray
from example_interfaces.msg import Float64
import time


import signal, time, sys

import cProfile, pstats

Quit_flag = False


class VectorConnectClient(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(VectorConnect, 'vector_connect')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = VectorConnect.Request()

    def send_request(self):
        self.req.serial = sys.argv[1]
        self.future = self.cli.call_async(self.req)

class ImgSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber1')
        self.subscription = self.create_subscription(Image,'vector_camera',self.listener_callback,10)
        self.subscription  # prevent unused variable warning
        self.img = None
        self.bridge = CvBridge()

    def listener_callback(self, msg):
        # self.get_logger().info('Reading image data')
        self.img = self.bridge.imgmsg_to_cv2(msg)
        cv2.imshow("Camera Feed", self.img)
        cv2.waitKey(1)

class Publisher(Node):
    def __init__(self, topic_name, DataType, data_name, name,robot_serial):
        super().__init__(name)
        self.publisher_ = self.create_publisher(DataType, topic_name, 10)
        # timer_period = 0.01 # seconds
        # self.timer = self.create_timer(timer_period, self.timer_callback)
        # self.data_type = DataType
        # self.data_name = data_name
        # self.robot_serial = robot_serial
        # self.robot = None


def main(args=None):
    rclpy.init(args=args)

    head_pub = Publisher("vector_head_angle",Float64,"head","vector_head_angle_"+"00804458","00804458")
    lift_pub = Publisher("vector_lift_height",Float64,"lift","vector_lift_height_"+"00804458","00804458")
    pose_pub = Publisher("vector_pose",Float64MultiArray,"pose","vector_pose_"+"00804458","00804458")
    wheel_pub = Publisher("vector_wheel_speed",Float64MultiArray,"wheel","vector_wheel_speed_"+"00804458","00804458")

    image_subscriber = ImgSubscriber()

    minimal_client = VectorConnectClient()
    minimal_client.send_request()

    while rclpy.ok():
        rclpy.spin_once(minimal_client)
        if minimal_client.future.done():
            try:
                response = minimal_client.future.result()
            except Exception as e:
                minimal_client.get_logger().info(
                    'Service call failed %r' % (e,))
            else:
                minimal_client.get_logger().info("Result of Vector Connect: for {} = \n{}\n{}".format(minimal_client.req.serial,response.success,response.message))
            break
    
    conn = True
    if response.message.startswith("F"):
        conn = False
    
    t0 = time.time()
    tstart = time.time()
    head_msg = Float64()
    lift_msg = Float64()
    wheel_msg = Float64MultiArray()
    pose_msg = Float64MultiArray()
    while rclpy.ok() and conn:
        

        head_msg.data = float(0)
        lift_msg.data = float(0)
        pose_msg.data = [float(0),float(0),float(0),float(0)]
        # wheel_msg.data = [float(0),float(0)]

        t1 = time.time()
        dt = t1-t0
        if dt <= 3:
            wheel_msg.data = [float(50),float(50)]
        if dt > 3 and dt <= 4:
            wheel_msg.data = [float(0),float(0)]
        if dt > 4 and dt <= 7:
            wheel_msg.data = [float(-50),float(-50)]
        if dt > 7 and dt <= 8:
            wheel_msg.data = [float(0),float(0)]
        if dt > 8:
            t0 = time.time()
        if (time.time() - tstart) > 20:
            wheel_msg.data = [float(0),float(0)]
            wheel_pub.publisher_.publish(wheel_msg)
            head_msg.data = float(69.69)
            head_pub.publisher_.publish(head_msg)
            break

        head_pub.publisher_.publish(head_msg)
        lift_pub.publisher_.publish(lift_msg)
        pose_pub.publisher_.publish(pose_msg)
        wheel_pub.publisher_.publish(wheel_msg)
        rclpy.spin_once(image_subscriber)
        

    head_pub.destroy_node()
    lift_pub.destroy_node()
    wheel_pub.destroy_node()
    pose_pub.destroy_node()
    image_subscriber.destroy_node()
    
    rclpy.shutdown()


if __name__ == '__main__':
    # main()
    profiler = cProfile.Profile()
    profiler.enable()
    main()
    profiler.disable()
    # stats = pstats.Stats(profiler).sort_stats('ncalls')
    # stats.print_stats()
    with open("/home/fizzer/Documents/cProfile_Vector_Stats/content/client_data.txt", "w") as f:
        stats = pstats.Stats(profiler,stream=f).sort_stats('ncalls')
        stats.print_stats()
    f.close()