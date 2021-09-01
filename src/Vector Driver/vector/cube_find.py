#!/usr/bin/env python3
import numpy as np
import cv2
from matplotlib import pyplot as plt
import glob

import anki_vector as av
from anki_vector.events import Events
from anki_vector.util import degrees
import time

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


def handle_object_observed(robot, event_type, event):
    # This will be called whenever an EvtObjectObserved is dispatched -
    # whenever an Object comes into view.
    robot_pose = robot.pose
    obj_pose = event.obj.pose
    relative_x = obj_pose.position.x - robot_pose.position.x
    relative_y = obj_pose.position.y - robot_pose.position.y
    relative_z = obj_pose.position.z - robot_pose.position.z
    relative_angle = obj_pose.rotation.angle_z.degrees - robot_pose.rotation.angle_z.degrees
    print("Object is located at:\nX = {}\nY = {}\nZ = {}\nA = {}\n\n".format(relative_x,relative_y,relative_z,relative_angle))


class TeleopSubscriber(Node):

    def __init__(self):
        super().__init__('teleop_subscriber')
        self.subscription = self.create_subscription(Twist,'cmd_vel',self.listener_callback,10)
        self.subscription  # prevent unused variable warning
        self.vel = [float(0),float(0)]
        self.stop = [float(0),float(0)]
        self.speed = float(75)

    def listener_callback(self, msg):
        self.msg = msg
        x,z = self.msg.linear.x, self.msg.linear.z
        ax,az = self.msg.angular.x, self.msg.angular.z
        if az == 0:
                self.vel = [self.speed*x,self.speed*x]
        else:
            if x == 0:
                self.vel = [-self.speed*az,self.speed*az]

def main(args = None):
    rclpy.init(args=args)
    teleop_sub = TeleopSubscriber()
    

    robot = av.Robot("00804458")
    robot.connect()
    robot.events.subscribe(handle_object_observed, Events.object_observed)
    # If necessary, move Vector's Head and Lift down
    robot.behavior.set_lift_height(0.0)
    robot.behavior.set_head_angle(degrees(0.0))

    while rclpy.ok():
        rclpy.spin_once(teleop_sub)
        robot.motors.set_wheel_motors(teleop_sub.vel[0],teleop_sub.vel[1])
    


if __name__ == '__main__':
    main()


# #!/usr/bin/env python3
# import rclpy
# import numpy as np
# import cv2
# from matplotlib import pyplot as plt
# import anki_vector as av
# from anki_vector.util import degrees
# import time
# from cv_bridge import CvBridge
# from sensor_msgs.msg import Image
# from rclpy.node import Node
# from example_interfaces.msg import Float64
# from geometry_msgs.msg import Twist

# class ImgSubscriber(Node):

#     def __init__(self):
#         super().__init__('img_subscriber')
#         self.subscription = self.create_subscription(Image,'vector_camera',self.listener_callback,10)
#         self.subscription  # prevent unused variable warning
#         self.img = None
#         self.bridge = CvBridge()

#     def listener_callback(self, msg):
#         # self.get_logger().info('Reading image data')
#         self.img = self.bridge.imgmsg_to_cv2(msg)
#         # cv2.imshow("Camera Feed", self.img)
#         # cv2.waitKey(1)
#         # img_processing(self.img)

# class Publisher(Node):
#     def __init__(self, topic_name, DataType, name,robot_serial):
#         super().__init__(name)
#         self.publisher_ = self.create_publisher(DataType, topic_name, 10)
#         self.data_type = DataType
#         self.robot_serial = robot_serial

# def take_static_image():
#     robot = av.Robot("00804458")
#     robot.connect()
#     height = input("Select head height\n")
#     robot.behavior.set_head_angle(degrees(float(height)))
#     robot.camera.init_camera_feed()
#     input("Hit enter when want to take image\n")
#     image_data = robot.camera.capture_single_image()
#     img = np.array(image_data.raw_image)
#     cv2.imshow("static image",img)
#     cv2.waitKey(0)
#     save = input("Save this image? y/n\n")
#     if save == "y":
#         name = "cube_"+str(time.time())+".jpg"
#         cv2.imwrite("/home/fizzer/Documents/Cube_Images/"+name,img)

# def compare_2_imgs(base,img):
#     img1 = cv2.cvtColor(base,cv2.COLOR_BGR2GRAY)
#     img2 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#     sift = cv2.SIFT_create()

#     keypoints_1, descriptors_1 = sift.detectAndCompute(img1,None)
#     keypoints_2, descriptors_2 = sift.detectAndCompute(img2,None)

#     #feature matching
#     bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

#     matches = bf.match(descriptors_1,descriptors_2)
#     matches = sorted(matches, key = lambda x:x.distance)

#     img3 = cv2.drawMatches(img1, keypoints_1, img2, keypoints_2, matches[:50], img2, flags=2)
#     # cv2.imshow("Matches",img3)
#     # cv2.waitKey(1)
#     for i in keypoints_1:
#         print(i.size)

#     plt.imshow(img3)
#     plt.show()

# def main(args=None):
#     # take_static_image()

#     rclpy.init(args=args)

#     # head_pub = Publisher("set_head_angle",Float64,"vector_head","0080458")
#     # msg = Float64()
#     # angle = input("Enter the angle you would like vectors head to be at in degrees:\n")
#     # chosen = True
#     # msg.data = float(angle)
#     # head_pub.publisher_.publish(msg)
#     # time.sleep(1)
#     # head_pub.destroy_node()
#     # img_sub = ImgSubscriber()

#     folder = "/home/fizzer/Documents/Cube_Images"
#     # img1_path = folder + "/Cube_Face_Smaller.jpg"
#     img1_path = folder + "/cube_extra_whited.jpg"
#     img1 = cv2.imread(img1_path)
#     # while rclpy.ok():
#     #     rclpy.spin_once(img_sub)
#     #     img2 = img_sub.img
#     #     compare_2_imgs(img1,img2)

#     # img2_path = folder + "/cube_1622668396.8305697.jpg"
#     # img2_path = folder + "/cube_1622668491.704268.jpg"
#     img2_path = folder + "/cube_1622671767.4466546.jpg"
#     img2 = cv2.imread(img2_path)
#     compare_2_imgs(img1,img2)



# class Subscriber(Node):

#     def __init__(self):
#         super().__init__('teleop_subscriber')
#         self.subscription = self.create_subscription(Twist,'cmd_vel',self.listener_callback,10)
#         self.subscription  # prevent unused variable warning
#         self.center = [float(180),float(320)]

#     def listener_callback(self, msg):
#         self.msg = msg
#         print(msg)

# def main2(args=None):
#     rclpy.init(args=args)
#     sub = Subscriber()
#     rclpy.spin(sub)
#     rclpy.shutdown()


# if __name__ == '__main__':
#     # main()
#     main2()




