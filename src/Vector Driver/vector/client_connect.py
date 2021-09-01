#!/usr/bin/env python3
import sys

from vector.srv import VectorConnect
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
        super().__init__('camera_subscriber')
        self.subscription = self.create_subscription(Image,'vector_camera',self.listener_callback,10)
        self.subscription  # prevent unused variable warning
        self.img = None
        self.bridge = CvBridge()

    def listener_callback(self, msg):
        # self.get_logger().info('Reading image data')
        self.img = self.bridge.imgmsg_to_cv2(msg)
        cv2.imshow("Camera Feed", self.img)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    # image_subscriber = ImgSubscriber()
    connect_client = VectorConnectClient()
    connect_client.send_request()

    while rclpy.ok():
        rclpy.spin_once(connect_client)
        if connect_client.future.done():
            try:
                response = connect_client.future.result()
            except Exception as e:
                connect_client.get_logger().info(
                    'Service call failed %r' % (e,))
            else:
                connect_client.get_logger().info("Result of Vector Connect: for {} = \n{}\n{}".format(connect_client.req.serial,response.success,response.message))
            break

    # rclpy.spin(image_subscriber)

    rclpy.shutdown()


if __name__ == '__main__':
    main()