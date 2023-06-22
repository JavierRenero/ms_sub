import random
import rclpy

# import requests
from rclpy.node import Node
from pkg_interfaces.msg import Batterylvl
import signal


class BatteryPublisher(Node):
    def __init__(self):
        super().__init__("battery_publisher")
        self.publisher_ = self.create_publisher(Batterylvl, "battery_topic_8LJ9", 10)
        self.timer_ = self.create_timer(1.0, self.publish_battery_level)

    def publish_battery_level(self):
        msg = Batterylvl()
        msg.level = random.randint(0, 100)
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%d"' % msg.level)


def main(args=None):
    try:
        rclpy.init(args=args)
        publisher = BatteryPublisher()
        rclpy.spin(publisher)
        publisher.destroy_node()
        rclpy.shutdown()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected, exiting...")


if __name__ == "__main__":
    main()
