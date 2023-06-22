import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from flask import Flask, jsonify, request, json


class OdomSubscriber(Node):
    def __init__(self):
        super().__init__("odom_subscriber")
        self.child_frame_id = "No data"
        self.pose_position = "No data"
        self.pose_orentation = "No data"
        self.twist_linear = "No data"
        self.twist_angular = "No data"

    def odom_reciver(self, msg):
        self.pose_position = msg.pose.pose.position
        self.pose_orentation = msg.pose.pose.orientation
        self.child_frame_id = msg.child_frame_id
        self.twist_angular = msg.twist.twist.angular
        self.twist_linear = msg.twist.twist.linear


app = Flask(__name__)


@app.route("/odom", methods=["GET"])
def get_battery_level():
    try:
        # Clear the request body
        request.data = None
        # Retrieve the variable from the query parameters
        variable = request.args.get("idRob")
        # Initialize the ROS node
        rclpy.init(args=None)
        # Create the ROS2 node
        ros2_node = OdomSubscriber()
        # Create the ROS2 subscription
        ros2_node.create_subscription(Odometry, "odom", ros2_node.odom_reciver, 10)
        # respin the node once to get the battery level
        rclpy.spin_once(ros2_node)
        app.logger.info("Odometry data received")

        # save the response in a variable
        (posx, posy, posz) = (
            ros2_node.pose_position.x,
            ros2_node.pose_position.y,
            ros2_node.pose_position.z,
        )
        (qx, qy, qz, ow) = (
            ros2_node.pose_orentation.x,
            ros2_node.pose_orentation.y,
            ros2_node.pose_orentation.z,
            ros2_node.pose_orentation.w,
        )
        (tl_x, tl_y, tl_z) = (
            ros2_node.twist_linear.x,
            ros2_node.twist_linear.y,
            ros2_node.twist_linear.z,
        )
        (ta_x, ta_y, ta_z) = (
            ros2_node.twist_angular.x,
            ros2_node.twist_angular.y,
            ros2_node.twist_angular.z,
        )
        app.logger.info(ros2_node.child_frame_id)
        app.logger.info(ros2_node.pose_position.x)
        app.logger.info(ros2_node.pose_position.y)
        app.logger.info(ros2_node.pose_position.z)
        app.logger.info(posx)
        app.logger.info(posy)
        app.logger.info(posz)
        response = {
            "Child_frame_id": ros2_node.child_frame_id,
            "Linear": {"x": tl_x, "y": tl_y, "z": tl_z},
            "Angular": {"x": ta_x, "y": ta_y, "z": ta_z},
            "Position": {"x": posx, "y": posy, "z": posz},
            "Orientation": {"x": qx, "y": qy, "z": qz, "w": ow},
        }

        # Clean up and exit the node and ROS int
        ros2_node.destroy_node()
        rclpy.shutdown()

        return jsonify(response)

    except KeyError:
        return "Missing 'idRob' field in the query param", 400


def main():
    app.run(debug=True, use_reloader=False, host="0.0.0.0", port=5001)


if __name__ == "__main__":
    main()
