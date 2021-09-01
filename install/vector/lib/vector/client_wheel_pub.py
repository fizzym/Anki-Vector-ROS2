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
import signal, time, sys

# class _GetchUnix:
#     def __init__(self):
#         import tty, sys

#     def __call__(self):
#         import sys, tty, termios
#         fd = sys.stdin.fileno()
#         old_settings = termios.tcgetattr(fd)
#         try:
#             tty.setraw(sys.stdin.fileno())
#             ch = sys.stdin.read(1)
#         finally:
#             termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#         return ch

# def TimedInput(timeout=0.1):
#     def timeout_error(*_):
#         raise TimeoutError
#     signal.signal(signal.SIGALRM, timeout_error)
#     signal.setitimer(signal.ITIMER_REAL,timeout)
#     try:
#         getch = _GetchUnix()
#         answer = getch()
#         signal.alarm(0)
#         return answer
#     except TimeoutError:   
#         signal.signal(signal.SIGALRM, signal.SIG_IGN)
#         return "No Entry"

class WheelPublisher(Node):
    def __init__(self,):
        super().__init__("wheel_pub")
        self.publisher_ = self.create_publisher(Float64MultiArray, "vector_wheel_speed", 10)
        # timer_period = 0.01 # seconds
        # self.timer = self.create_timer(timer_period, self.timer_callback)
        # self.wheel_speed = float(50)
        # self.wheel = [float(0),float(0)]
        self.msg = Float64MultiArray()

    # def timer_callback(self):
        # d = TimedInput(0.1)
        # if d == "q":
        #     sys.exit()
        # if d == "w":
        #     self.wheel = [self.wheel_speed,self.wheel_speed]
        # if d == "s":
        #     self.wheel = [-self.wheel_speed,-self.wheel_speed]
        # if d == "a":
        #     self.wheel = [-self.wheel_speed,self.wheel_speed]
        # if d == "d":
        #     self.wheel = [self.wheel_speed,-self.wheel_speed]
        # if d != "w" and d != "s" and d != "a" and d != "d":
        #     self.wheel = [float(0),float(0)]
        
        # self.msg.data = self.wheel
        # self.publisher_.publish(self.msg)
        # self.get_logger().info("Publishing {}".format(msg.data))

def calculate_wheel_speed(center):
    base_speed = float(100)
    img_CX = float(320)
    cx,cy = center[0],center[1]
    k = 1.1*(center[0]/img_CX)
    LW = base_speed*k
    RW = (2*base_speed)-LW
    return [LW,RW]


class LineSubscriber(Node):

    def __init__(self):
        super().__init__('line_subscriber')
        self.subscription = self.create_subscription(Float64MultiArray,'line_center',self.listener_callback,10)
        self.subscription  # prevent unused variable warning
        self.center = [float(180),float(320)]

    def listener_callback(self, msg):
        self.center = msg.data

def main(args=None):
    rclpy.init(args=args)

    line_sub = LineSubscriber()
    wheel_pub = WheelPublisher()

    while rclpy.ok():
        rclpy.spin_once(line_sub)
        wheel_pub.msg.data = calculate_wheel_speed(line_sub.center)
        print(wheel_pub.msg.data)
        wheel_pub.publisher_.publish(wheel_pub.msg)
        
        

    line_sub.destroy_node()
    wheel_pub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()