import rclpy
from rclpy.node import Node

from yolo_msgs.msg import DetectionArray, Detection, KeyPoint2D


class KeypointsFilterNode(Node):
    def __init__(self):
        super().__init__('keypoints_filter_node')

        self.subscription = self.create_subscription(
            DetectionArray,
            '/yolo/detections',
            self.detections_callback,
            10
        )

        self.publisher = self.create_publisher(
            DetectionArray,
            '/yolo/arm_keypoints',
            10
        )

        # shoulder, elbow, wrist
        self.target_keypoint_ids = {7, 9, 11}

        self.get_logger().info('Keypoints filter node started')

    def detections_callback(self, msg: DetectionArray):
        filtered_msg = DetectionArray()
        filtered_msg.header = msg.header

        for detection in msg.detections:
            new_det = Detection()
            new_det = detection

            filtered_keypoints = []
            for kp in detection.keypoints.data:
                if kp.id in self.target_keypoint_ids:
                    filtered_keypoints.append(kp)

                    self.get_logger().info(
                        f"Detected keypoint id={kp.id} "
                        f"x={kp.point.x:.1f}, y={kp.point.y:.1f}, "
                        f"score={kp.score:.2f}"
                    )

            new_det.keypoints.data = filtered_keypoints
            filtered_msg.detections.append(new_det)

        self.publisher.publish(filtered_msg)


def main(args=None):
    rclpy.init(args=args)
    node = KeypointsFilterNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
