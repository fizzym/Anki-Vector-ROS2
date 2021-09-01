import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):

    def __init__(self, topic_name, m,name):
        super().__init__(name)
        self.publisher_ = self.create_publisher(String, topic_name, 10)
        timer_period = 0.01 # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        self.m = m

    def timer_callback(self):
        msg = String()
        msg.data = self.m + ': %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    pub1 = MinimalPublisher("topic1", "Hello on topic 1","minpub1")
    pub2 = MinimalPublisher("topic2", "Hello on topic 2","minpub2")

    while rclpy.ok():
        rclpy.spin_once(pub1)
        rclpy.spin_once(pub2)

    rclpy.shutdown()


if __name__ == '__main__':
    main()