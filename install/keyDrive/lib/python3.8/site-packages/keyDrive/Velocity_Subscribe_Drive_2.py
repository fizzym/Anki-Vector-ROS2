import rclpy
from rclpy.node import Node

from std_msgs.msg import String

import anki_vector as av

def read_ini_file(path):
    f = open(path,"r")
    lines = f.readlines()
    serial = lines[0].strip().split("[")[-1].split("]")[0]
    cert = lines[1].strip().split("cert = ")[-1]
    ip = lines[2].strip().split("ip = ")[-1]+":443"
    name = lines[3].strip().split("name = ")[-1]
    guid = lines[4].strip().split("guid = ")[-1]
    return serial, cert, ip, name, guid

def convert_to_vel(keyIn):
    if keyIn == "w":
        vel = (50,50)
    if keyIn == "s":
        vel = (-50,-50)
    if keyIn == "a":
        vel = (-50,50)
    if keyIn == "d":
        vel = (50,-50)
    if keyIn != "w" and keyIn != "s" and keyIn != "a" and keyIn != "d":
        vel = (0,0)
    return vel

class VelSubscriber(Node):

    def __init__(self,robot):
        super().__init__('minimal_subscriber')
        self.robot = robot
        self.subscription = self.create_subscription(String,'Drive_Motors',self.listener_callback,10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)
        vel = convert_to_vel(msg.data)
        self.robot.motors.set_wheel_motors(vel[0],vel[1])


def main(args=None):
    sdk_ini_2 = "/home/fizzer/.anki_vector/sdk_config_M8J3.ini"
    serial, cert, ip, name, guid = read_ini_file(sdk_ini_2)
    print(read_ini_file(sdk_ini_2))
    robot2 = av.Robot(config = {"name": name, "host": ip, "cert": cert, "guid": guid})
    robot2.connect()

    rclpy.init(args=args)

    velocity_subscriber = VelSubscriber(robot2)

    rclpy.spin(velocity_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    velocity_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
