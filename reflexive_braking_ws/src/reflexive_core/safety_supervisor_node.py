import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry


class SafetySupervisorNode(Node):
    """
    Subscribes to LiDAR and Odometry data to monitor Time-to-Collision (TTC).
    Arbitrates /cmd_vel commands to enforce emergency reflexive braking.
    """
    def __init__(self):
        super().__init__('safety_supervisor_node')

        # Tunable safety thresholds
        self.declare_parameter('ttc_threshold_sec', 1.2)
        self.declare_parameter('min_stopping_distance_m', 0.75)

        # Internal state
        self.current_velocity = 0.0
        self.min_forward_distance = float('inf')

        # Subscriptions
        self.odom_sub = self.create_subscription(
            Odometry, '/odom', self.odom_callback, 10
        )
        self.scan_sub = self.create_subscription(
            LaserScan, '/scan', self.scan_callback, 10
        )
        self.raw_cmd_sub = self.create_subscription(
            Twist, '/cmd_vel_teleop', self.cmd_callback, 10
        )

        # Filtered output directly controlling the robot
        self.safe_cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        self.get_logger().info('Safety Supervisor Node Initialized and Monitoring.')

    def odom_callback(self, msg: Odometry):
        self.current_velocity = msg.twist.twist.linear.x

    def scan_callback(self, msg: LaserScan):
        # Extract forward arc: ±15 degrees from center heading
        total_rays = len(msg.ranges)
        if total_rays == 0:
            return

        mid_idx = total_rays // 2
        window = max(1, int(total_rays * (15 / 360)))

        forward_ranges = [
            r for r in msg.ranges[mid_idx - window : mid_idx + window]
            if msg.range_min < r < msg.range_max
        ]

        self.min_forward_distance = min(forward_ranges) if forward_ranges else float('inf')

    def cmd_callback(self, msg: Twist):
        safe_msg = Twist()
        ttc_threshold = self.get_parameter('ttc_threshold_sec').value
        min_distance = self.get_parameter('min_stopping_distance_m').value

        # Calculate Time-to-Collision (TTC)
        if self.current_velocity > 0.05:
            ttc = self.min_forward_distance / self.current_velocity
        else:
            ttc = float('inf')

        # Failsafe arbitration check
        if ttc <= ttc_threshold or self.min_forward_distance < min_distance:
            self.get_logger().warn(
                f'[REFLEX TRIGGERED] TTC: {ttc:.2f}s | Dist: {self.min_forward_distance:.2f}m -> Clamping velocity to 0.'
            )
            safe_msg.linear.x = 0.0
            safe_msg.angular.z = 0.0
        else:
            # Passthrough nominal driving command
            safe_msg = msg

        self.safe_cmd_pub.publish(safe_msg)


def main(args=None):
    rclpy.init(args=args)
    node = SafetySupervisorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()