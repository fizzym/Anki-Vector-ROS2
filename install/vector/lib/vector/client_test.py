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

class Commands():
    def __init__(self):
        fzero = float(0)
        self.head = fzero
        self.lift = fzero
        self.pose = [fzero,fzero,fzero,fzero]
        self.wheel = [fzero,fzero]
        self.speaker = ""
        self.face = None
        self.wheel_speed = float(50)
        self.head_speed = float(0.5)
        self.lift_speed = float(0.5)
    
    def head_command(self,d):
        # print("Getting head command")
        if d == "h":
            self.head = self.head_speed
        if d == "g":
            self.head = -self.head_speed
        if d != "h" and d != "g":
            self.head = float(0)

    def lift_command(self,d):
        # print("Getting lift command")
        if d == "l":
            self.lift = self.lift_speed
        if d == "k":
            self.lift = -self.lift_speed
        if d != "l" and d != "k":
            self.lift = float(0)

    # def pose_command(self,d):
    #     print("Getting pose command")

    def wheel_command(self,d):
        # print("Getting wheel command")
        if d == "w":
            self.wheel = [self.wheel_speed,self.wheel_speed]
        if d == "s":
            self.wheel = [-self.wheel_speed,-self.wheel_speed]
        if d == "a":
            self.wheel = [-self.wheel_speed,self.wheel_speed]
        if d == "d":
            self.wheel = [self.wheel_speed,-self.wheel_speed]
        if d != "w" and d != "s" and d != "a" and d != "d":
            self.wheel = [float(0),float(0)]
 
    def speaker_command(self,d):
        # print("Getting speaker command")
        msg = ""
        if d == "t":
            msg = input("Input the message you want vector to say:\n")
        self.speaker = msg

    # def face_command(self,d):
    #     print("Getting face command")


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

class VectorSpeakClient(Node):

    def __init__(self,command_object):
        super().__init__('minimal_client_async_speak')
        self.cli = self.create_client(VectorSpeak, 'vector_speaker')
        while not self.cli.wait_for_service(timeout_sec=0.1):
            self.get_logger().info('service not available, waiting again...')
        self.req = VectorSpeak.Request()
        self.command = command_object

    def send_request(self):
        input_data = TimedInput(0.1)
        if input_data == "q":
            sys.exit()
        self.command.speaker_command(input_data)
        self.req.message = self.command.speaker
        self.future = self.cli.call_async(self.req)

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(String,'vector_acc',self.listener_callback,10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

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
    def __init__(self, topic_name, DataType, data_name, name,robot_serial, command_object):
        super().__init__(name)
        self.publisher_ = self.create_publisher(DataType, topic_name, 10)
        timer_period = 0.01 # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.data_type = DataType
        self.data_name = data_name
        self.robot_serial = robot_serial
        self.robot = None
        self.command = command_object

    def timer_callback(self):
        global Quit_flag
        input_data = TimedInput(0.1)
        if input_data == "q":
            # sys.exit()
            Quit_flag = True
        # print(input_data)
        self.command.head_command(input_data)
        self.command.lift_command(input_data)
        # self.command.pose_command(input_data)
        self.command.wheel_command(input_data)
        # self.command.face_command(input_data)
        if self.data_name == "head":
            msg = Float64()
            msg.data = self.command.head
            self.publisher_.publish(msg)
        if self.data_name == "lift":
            msg = Float64()
            msg.data = self.command.lift
            self.publisher_.publish(msg)
        # if self.data_name == "pose":
        #     msg = Float64MultiArray()
        #     msg.data = self.command.pose
        #     self.publisher_.publish(msg)
        if self.data_name == "wheel":
            msg = Float64MultiArray()
            msg.data = self.command.wheel
            self.publisher_.publish(msg)
        # if self.data_name == "face":
        #     msg = Image()
        #     msg.data = self.command.face
        #     self.publisher_.publish(msg)
        
        # self.get_logger().info('Publishing: "%s"' % msg.data)


def main(args=None):
    global Quit_flag
    rclpy.init(args=args)

    C = Commands()
    head_pub = Publisher("vector_head_angle",Float64,"head","vector_head_angle_"+"00804458","00804458",C)
    lift_pub = Publisher("vector_lift_height",Float64,"lift","vector_lift_height_"+"00804458","00804458",C)
    pose_pub = Publisher("vector_pose",Float64MultiArray,"pose","vector_pose_"+"00804458","00804458",C)
    wheel_pub = Publisher("vector_wheel_speed",Float64MultiArray,"wheel","vector_wheel_speed_"+"00804458","00804458",C)
    # speaker_client = VectorSpeakClient(C)
    # face_pub = Publisher("vector_face",Image,"face","vector_face_"+"00804458","00804458",C)
    

    # min_sub = MinimalSubscriber()
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
    
    # conn = True
    # if response.message.startswith("F"):
    #     conn = False
    
    while rclpy.ok():
        # rclpy.spin_once(min_sub)
        rclpy.spin_once(image_subscriber)
        rclpy.spin_once(head_pub)
        rclpy.spin_once(lift_pub)
        rclpy.spin_once(pose_pub)
        rclpy.spin_once(wheel_pub)
        if Quit_flag:
            msg = Float64()
            msg.data = float(69.69)
            head_pub.publisher_.publish(msg)
            break

        # speaker_client.send_request()
        # rclpy.spin_once(speaker_client,timeout_sec=0.001)
        # if speaker_client.future.done():
        #     try:
        #         response = speaker_client.future.result()
        #     except Exception as e:
        #         speaker_client.get_logger().info('Service call failed %r' % (e,))
        #     else:
        #         speaker_client.get_logger().infor("Result of vector speak = \n{}".format(response.success))
        # rclpy.spin_once(face_pub)

    # rclpy.spin(image_subscriber)



    # minimal_client.destroy_node()
    # min_sub.destroy_node()
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