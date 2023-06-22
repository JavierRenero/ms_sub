import rclpy
from rclpy.node import Node
from pkg_interfaces.msg import Batterylvl
from flask import Flask, jsonify, request, json



class BatterySubscriber(Node):
    def __init__(self):
        super().__init__("battery_subscriber")
        self.battery_level = "No data"
   
    def receive_battery_level(self, msg):
        self.battery_level = msg.level

app = Flask(__name__)


@app.route("/battery", methods=["GET"])
def get_battery_level():
    try:
        # Clear the request body
        request.data = None
        # Retrieve the variable from the query parameters
        variable = request.args.get("idRob")
        # Initialize the ROS node
        rclpy.init(args=None)
        # Create the ROS2 node
        ros2_node = BatterySubscriber()
        # Create the ROS2 subscription
        ros2_node.create_subscription(
            Batterylvl(), "battery_topic_" + variable, ros2_node.receive_battery_level, 10
        )
        # respin the node once to get the battery level
        rclpy.spin_once(ros2_node) 
        # save the response in a variable
        response = jsonify({"battery_level": str(ros2_node.battery_level)})

        # Clean up and exit the node and ROS int
        ros2_node.destroy_node()
        rclpy.shutdown()

        return response

    except KeyError:
        return "Missing 'idRob' field in the query param", 400


def main():
    app.run(debug=True, use_reloader=False, host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
