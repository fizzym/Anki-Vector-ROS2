from cv_bridge.core import CvBridge
import rclpy
from rclpy.node import Node
import sensor_msgs

from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class ImgSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(Image,'Camera_Feed_2',self.listener_callback,10)
        self.subscription  # prevent unused variable warning
        self.img = None
        self.bridge = CvBridge()

    def listener_callback(self, msg):
        self.get_logger().info('Reading image data')
        self.img = self.bridge.imgmsg_to_cv2(msg)
        cv2.imshow("Camera Feed", self.img)
        cv2.waitKey(1)



def main(args=None):
    rclpy.init(args=args)

    image_subscriber = ImgSubscriber()

    rclpy.spin(image_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    image_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
