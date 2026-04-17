import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from interbotix_xs_msgs.msg import JointGroupCommand
import csv
import time
import os

class PoseLogger(Node):
    def __init__(self):
        super().__init__('pose_logger')
        self.create_subscription(JointState, '/px150/joint_states', self.joint_state_callback, 10)
        self.create_subscription(JointGroupCommand, '/px150/commands/joint_group', self.command_callback, 10)
        self.actual_shoulder = None
        self.actual_elbow    = None
        self.cmd_shoulder    = None
        self.cmd_elbow       = None
        self.t0              = None
        save_dir = os.path.expanduser('~/ros2_ws/src/manipulation_node/manipulation_node')
        file_path = os.path.join(save_dir, '45_degree_pose.csv')

        self.csv_file = open(file_path, 'w', newline='')
        self.writer   = csv.writer(self.csv_file)
        self.writer.writerow([
            'time_s',
            'cmd_shoulder_rad', 'actual_shoulder_rad', 'shoulder_error_rad', 'shoulder_error_deg',
            'cmd_elbow_rad',    'actual_elbow_rad',    'elbow_error_rad',    'elbow_error_deg',
        ])
        self.create_timer(10.0, self.stop)
        self.get_logger().info('PoseLogger started — logging for 10 seconds then saving.')

    def joint_state_callback(self, msg: JointState):
        name_to_pos = dict(zip(msg.name, msg.position))
        self.actual_shoulder = name_to_pos.get('shoulder')
        self.actual_elbow    = name_to_pos.get('elbow')
        self._try_log()

    def command_callback(self, msg: JointGroupCommand):
        if len(msg.cmd) >= 3:
            self.cmd_shoulder = msg.cmd[1]
            self.cmd_elbow    = msg.cmd[2]

    def _try_log(self):
        if any(v is None for v in [self.cmd_shoulder, self.cmd_elbow,
                                    self.actual_shoulder, self.actual_elbow]):
            return

        now = time.time()
        if self.t0 is None:
            self.t0 = now
        t = round(now - self.t0, 3)

        sh_err = self.cmd_shoulder - self.actual_shoulder
        el_err = self.cmd_elbow    - self.actual_elbow

        self.writer.writerow([
            t,
            round(self.cmd_shoulder,    4), round(self.actual_shoulder, 4), round(sh_err, 4), round(sh_err * 57.296, 3),
            round(self.cmd_elbow,       4), round(self.actual_elbow,    4), round(el_err, 4), round(el_err * 57.296, 3),
        ])
        self.csv_file.flush()

        self.get_logger().info(
            f't={t:.2f}s | '
            f'Shoulder  sent={self.cmd_shoulder:+.4f}  actual={self.actual_shoulder:+.4f}  err={sh_err:+.4f} rad ({sh_err * 57.296:+.2f} deg) | '
            f'Elbow  sent={self.cmd_elbow:+.4f}  actual={self.actual_elbow:+.4f}  err={el_err:+.4f} rad ({el_err * 57.296:+.2f} deg)'
        )

    def stop(self):
        self.csv_file.close()
        self.get_logger().info('10 seconds done — 45_degree.csv saved. Shutting down.')
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = PoseLogger()
    rclpy.spin(node)
    node.destroy_node()


if __name__ == '__main__':
    main()