import rclpy
from rclpy.node import Node
from collections import deque
from yolo_msgs.msg import DetectionArray
from interbotix_xs_msgs.msg import JointGroupCommand
from ..utils.angle_utils import calculate_arm_angles


class ArmAngleSimNode(Node):
    def __init__(self):
        super().__init__('arm_angle_sim_node')
        self.subscription = self.create_subscription(
            DetectionArray,
            '/yolo/arm_keypoints',
            self.keypoints_callback,
            10
        )
        self.joint_pub = self.create_publisher(
            JointGroupCommand,
            '/wx200/commands/joint_group',
            10
        )
        self.last_publish_time = self.get_clock().now()
        self.PUBLISH_RATE_HZ = 5
        self.WINDOW_SIZE = 5
        self.shoulder_window = deque(maxlen=self.WINDOW_SIZE)
        self.elbow_window = deque(maxlen=self.WINDOW_SIZE)

    def keypoints_callback(self, msg: DetectionArray):
        if not msg.detections:
            return
        detection = msg.detections[0]
        keypoints = {
            kp.id: (kp.point.x, kp.point.y)
            for kp in detection.keypoints.data
        }
        if not all(k in keypoints for k in [7, 9, 11]):
            return
        shoulder = keypoints[7]
        elbow = keypoints[9]
        wrist = keypoints[11]
        now = self.get_clock().now()
        dt = (now - self.last_publish_time).nanoseconds / 1e9
        if dt < (1.0 / self.PUBLISH_RATE_HZ):
            return
        self.last_publish_time = now
        shoulder_cmd, elbow_cmd = calculate_arm_angles(shoulder, elbow, wrist)
        self.shoulder_window.append(shoulder_cmd)
        self.elbow_window.append(elbow_cmd)
        if len(self.shoulder_window) < self.WINDOW_SIZE:
            self.get_logger().debug(f"{len(self.shoulder_window)}/{self.WINDOW_SIZE}")
            return
        smooth_shoulder = sum(self.shoulder_window) / self.WINDOW_SIZE
        smooth_elbow = sum(self.elbow_window) / self.WINDOW_SIZE
        self.get_logger().info(f"Shoulder {smooth_shoulder:.3f}, Elbow {smooth_elbow:.3f}")
        msg_out = JointGroupCommand()
        msg_out.name = 'arm'
        msg_out.cmd = [
            0.0,             # waist
            smooth_shoulder,  # shoulder
            smooth_elbow,    # elbow
            0.0,             # forearm_roll
            0.0,             # wrist_angle
            0.0              # wrist_rotate
        ]
        self.joint_pub.publish(msg_out)


def main(args=None):
    rclpy.init(args=args)
    node = ArmAngleSimNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
