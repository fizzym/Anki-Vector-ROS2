from typing import Set
from example_interfaces.srv import SetBool

import rclpy
from rclpy.node import Node


class MinimalService(Node):

    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(SetBool, 'set_bool', self.set_bool_callback)
        self.value_set = False

    def set_bool_callback(self, request, response):
        print("Value previously set to {}".format(self.value_set))
        self.value_set = request.data
        if self.value_set == request.data:
            response.success = True
            response.message = "Succesfully set data"
        self.get_logger().info("Value set to {}".format(self.value_set))


        return response


def main(args=None):
    rclpy.init(args=args)

    minimal_service = MinimalService()

    rclpy.spin(minimal_service)

    rclpy.shutdown()


if __name__ == '__main__':
    main()