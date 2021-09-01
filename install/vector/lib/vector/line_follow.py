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
import signal, time
import cProfile, pstats

class ImgSubscriber(Node):

    def __init__(self):
        super().__init__('img_subscriber')
        self.subscription = self.create_subscription(Image,'vector_camera',self.listener_callback,10)
        self.subscription  # prevent unused variable warning
        self.img = None
        self.bridge = CvBridge()

    def listener_callback(self, msg):
        # self.get_logger().info('Reading image data')
        self.img = self.bridge.imgmsg_to_cv2(msg)
        # cv2.imshow("Camera Feed", self.img)
        # cv2.waitKey(1)
        # img_processing(self.img)

class Publisher(Node):
    def __init__(self, topic_name, DataType, name,robot_serial):
        super().__init__(name)
        self.publisher_ = self.create_publisher(DataType, topic_name, 10)
        self.data_type = DataType
        self.robot_serial = robot_serial

def img_processing(img_raw):
    gray = cv2.cvtColor(img_raw,cv2.COLOR_BGR2GRAY)
    # cv2.imshow("Grayscale", gray)
    # cv2.waitKey(1)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    # cv2.imshow("blurred", blur)
    # cv2.waitKey(1)
    ret,thresh = cv2.threshold(blur,127,255,cv2.THRESH_BINARY_INV)
    # cv2.imshow("Threshold", thresh)
    # cv2.waitKey(1)
    h,w = thresh.shape[0],thresh.shape[1]
    region = np.copy(thresh)
    region[0:int(h/2),0:w] = 0
    region[0:h,0:int(w/4)] = 0
    region[0:h,int(3*(w/4)):w] = 0
    # region = cv2.rectangle(region,(int(w/4),int(h/2.25)),(int(3*(w/4)),h),0,2)
    # cv2.imshow("Region", region)
    # cv2.waitKey(1)

    cntrs,hier = cv2.findContours(region,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    m = 0
    if len(cntrs) > 0:
        cntr = cntrs[0]
        for i in cntrs:
            if len(i) > m:
                m = len(i)
                cntr = i
    else:
        cx = int(w/2)
        cy = int(h/2)
    # contoured = cv2.drawContours(img_raw,[cntr],0,255,2)
    # cv2.imshow("Contoured", contoured)
    # cv2.waitKey(1)

    try:
        M = cv2.moments(cntr)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
    except:
        cx = int(w/2)
        cy = int(h/2)
        print("Error calculating moments and center")
    
    center = cv2.circle(img_raw,(cx,cy),3,255,-1,cv2.LINE_AA)
    cv2.imshow("Center", center)
    cv2.waitKey(1)
    return [float(cx),float(cy)]




def main(args=None):
    rclpy.init(args=args)
    img_sub = ImgSubscriber()
    head_pub = Publisher("set_head_angle",Float64,"vector_head","0080458")
    chosen = False
    msg = Float64()
    while rclpy.ok():
        if not chosen:
            angle = input("Enter the angle you would like vectors head to be at in degrees:\n")
            chosen = True
            msg.data = float(angle)
        head_pub.publisher_.publish(msg)
        time.sleep(1)
        rclpy.spin_once(img_sub)
        if chosen:
            ok = input("Is this ok? y/n\n")
            if ok == "y":
                break
            else:
                chosen = False
    head_pub.destroy_node()

    center_pub = Publisher("line_center",Float64MultiArray,"line_center","0080458")
    center_msg = Float64MultiArray()
    while rclpy.ok():
        rclpy.spin_once(img_sub)
        center_msg.data = img_processing(img_sub.img)
        center_pub.publisher_.publish(center_msg)

    center_pub.destroy_node()
    img_sub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()