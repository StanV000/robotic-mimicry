import rclpy
from rclpy.node import Node
from math import atan2, pi, sin, cos
from collections import deque
from yolo_msgs.msg import DetectionArray
from interbotix_xs_msgs.msg import JointGroupCommand

class ArmAngleNode(Node):
    def __init__(self):
        super().__init__('arm_angle_node')
        self.subscription = self.create_subscription(
            DetectionArray,
            '/yolo/arm_keypoints',
            self.keypoints_callback,
            10
        )
        self.joint_pub = self.create_publisher(
            JointGroupCommand,
            '/px150/commands/joint_group',
            10
        )
        self.last_publish_time = self.get_clock().now()
        self.PUBLISH_RATE_HZ = 5

        # Sliding window
        self.WINDOW_SIZE     = 5
        self.shoulder_window = deque(maxlen=self.WINDOW_SIZE)
        self.elbow_window    = deque(maxlen=self.WINDOW_SIZE)

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
        elbow    = keypoints[9]
        wrist    = keypoints[11]

        now = self.get_clock().now()
        dt  = (now - self.last_publish_time).nanoseconds / 1e9
        if dt < (1.0 / self.PUBLISH_RATE_HZ):
            return
        self.last_publish_time = now

        a1 = atan2(-(elbow[1] - shoulder[1]), (elbow[0] - shoulder[0]))
        a2 = atan2(-(wrist[1] - elbow[1]),    (wrist[0] - elbow[0]))
        a1 = atan2(sin(a1), cos(a1))

        relative = a2 - a1
        relative = atan2(sin(relative), cos(relative))

        shoulder_cmd = atan2(
            (elbow[1] - shoulder[1]),
            abs(elbow[0] - shoulder[0])
        )
        elbow_cmd = -pi/2 - relative

 
        self.shoulder_window.append(shoulder_cmd)
        self.elbow_window.append(elbow_cmd)


        if len(self.shoulder_window) < self.WINDOW_SIZE:
            print(f"{len(self.shoulder_window)}/{self.WINDOW_SIZE}")
            return

        # Average the window
        smooth_shoulder = sum(self.shoulder_window) / self.WINDOW_SIZE
        smooth_elbow    = sum(self.elbow_window)    / self.WINDOW_SIZE

        print(f"Shoulder {smooth_shoulder:.3f}, Elbow {smooth_elbow:.3f}")

        msg_out      = JointGroupCommand()
        msg_out.name = 'arm'
        #below for simulation
        # msg_out.cmd  = [
        #     0.0,            # waist
        #     smooth_shoulder, # shoulder
        #     smooth_elbow,    # elbow
        #     0.0,            # forearm_roll
        #     0.0,            # wrist_angle
        #     0.0             # wrist_rotate
        # ]
        #actual robot integration 5 degrees of freedom, but we only use 4, dont' need wrist rotate
        msg_out.cmd = [
            0.0,           # waist
            shoulder_cmd,  # shoulder
            elbow_cmd,     # elbow
            0.0,           # wrist_angle
        ]

        self.joint_pub.publish(msg_out)

def main(args=None):
    rclpy.init(args=args)
    node = ArmAngleNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()