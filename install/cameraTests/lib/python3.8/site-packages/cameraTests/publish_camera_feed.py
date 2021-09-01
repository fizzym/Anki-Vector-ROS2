import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from sensor_msgs.msg import Image

from cv_bridge import CvBridge
import cv2
import numpy as np

import anki_vector as av

def change_sdk_ini(path):
    inPath = path
    outPath = "/home/fizzer/.anki_vector/sdk_config.ini"
    inFile = open(inPath,"r")
    Text = inFile.read()
    inFile.close()
    outFile = open(outPath,"w")
    outFile.write(Text)
    outFile.close()

def read_ini(path):
    f = open(path,"r")
    lines = f.readlines()
    serial = lines[0].strip().split("[")[-1].split("]")[0]
    cert = lines[1].strip().split("cert = ")[-1]
    ip = lines[2].strip().split("ip = ")[-1]+":443"
    name = lines[3].strip().split("name = ")[-1]
    guid = lines[4].strip().split("guid = ")[-1]
    return serial, cert, ip, name, guid

class ImgPublisher(Node):

    def __init__(self,robot):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(Image, 'Camera_Feed', 10)
        timer_period = 0.01  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        self.cv_image = None
        self.bridge = CvBridge()
        self.robot = robot

    def timer_callback(self):
        self.cv_image = cv2.cvtColor(np.array(self.robot.camera.latest_image.raw_image),cv2.COLOR_RGB2BGR)
        self.publisher_.publish(self.bridge.cv2_to_imgmsg(np.array(self.cv_image), "bgr8"))
        self.get_logger().info('Publishing an image')
        self.i += 1

    


def main(args=None):
    sdk_ini = "/home/fizzer/.anki_vector/sdk_config_M9P3.ini"
    change_sdk_ini(sdk_ini)
    serial, cert, ip, name, guid = read_ini(sdk_ini)
    robot = av.Robot(config = {"name": name, "host": ip, "cert": cert, "guid": guid})
    robot.connect()
    robot.camera.init_camera_feed()

    rclpy.init(args=args)

    image_publisher = ImgPublisher(robot)

    rclpy.spin(image_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    image_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()