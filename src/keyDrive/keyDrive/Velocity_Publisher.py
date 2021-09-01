import rclpy
from rclpy.node import Node

from std_msgs.msg import String

import signal, time, sys

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


class VelPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'Drive_Motors', 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        timeout = 0.1
        msg.data = TimedInput(timeout)
        if msg.data == "q":
            sys.exit()
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: {}'.format(msg.data))
        self.i += 1

    


def main(args=None):
    rclpy.init(args=args)

    velocity_publisher = VelPublisher()

    rclpy.spin(velocity_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    velocity_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()