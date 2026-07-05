# Human-Following Robotic Arm with YOLOv8 Pose Estimation

This project uses YOLOv8 pose estimation with an Intel RealSense D435 camera to detect human keypoints and drive an Interbotix robotic arm (simulated or real) based on the detected pose.

## Dependencies / Related Repos

| Component | Repo |
|---|---|
| YOLOv8 ROS 2 wrapper (`yolo_bringup`) | [mgonzs13/yolo_ros](https://github.com/mgonzs13/yolo_ros) |
| Ultralytics YOLOv8 (underlying model) | [ultralytics/ultralytics](https://github.com/ultralytics/ultralytics) |
| Intel RealSense ROS 2 wrapper | [IntelRealSense/realsense-ros](https://github.com/IntelRealSense/realsense-ros) |
| Intel RealSense SDK (librealsense) | [IntelRealSense/librealsense](https://github.com/IntelRealSense/librealsense) |
| Interbotix X-Series Arms | [Interbotix/interbotix_ros_manipulators](https://github.com/Interbotix/interbotix_ros_manipulators) |

> **Note:** There are several forks/renames of `yolo_ros` floating around (`yolov8_ros`, `yolo_ros_wrapper`, etc.). Use the canonical [mgonzs13/yolo_ros](https://github.com/mgonzs13/yolo_ros) to avoid outdated versions.

## System Overview

```
RealSense D435  →  YOLOv8 Pose (yolo_bringup)  →  manipulation_keypoints  →  arm_angle_node  →  Interbotix Arm (sim or hardware)
```

Each stage depends on the topics published by the previous one, so nodes must be started in order.

## Usage

### 1. Perception (YOLOv8 + RealSense)

Launch the RealSense D435 camera and YOLOv8 pose detection **before** starting the robot.

```bash
ros2 launch realsense2_camera rs_launch.py
```

```bash
ros2 launch yolo_bringup yolo.launch.py \
    input_image_topic:=/camera/camera/color/image_rect_raw \
    model:=yolov8n-pose.pt \
    device:=cpu \
    imgsz_height:=320 \
    imgsz_width:=320 \
    augment:=False \
    half:=False
```

> **Note:** The parameters above (model, device, image size, etc.) are tuned for limited hardware. Adjust them freely  e.g. use `device:=cuda:0` and a larger model like `yolov8m-pose.pt` if you have a GPU available.

### 2. Manipulation Nodes

Once perception is running, start the keypoint and arm-angle nodes, in this order:

```bash
ros2 run manipulation_node manipulation_keypoints
```

```bash
ros2 run manipulation_node arm_angle_node
```

`manipulation_keypoints` subscribes to YOLO's pose output and publishes processed keypoint data. `arm_angle_node` subscribes to that keypoint data and computes the target joint angles for the arm.

### 3. Robot Arm

Finally, launch either the simulated or real robot arm.

**Simulation (`wx200` model):**
```bash
ros2 launch interbotix_xsarm_control xsarm_control.launch.py \
    robot_model:=wx200 \
    use_sim:=true \
    use_rviz:=true
```

**Hardware (`px150` model):**
```bash
ros2 launch interbotix_xsarm_control xsarm_control.launch.py \
    robot_model:=px150
```

> Note: `wx200` is used for simulation and `px150` for the physical arm in this setup adjust `robot_model` if your hardware differs.

## Startup Order Summary

1. **Camera**  `realsense2_camera`
2. **Perception**  `yolo_bringup` (YOLOv8 pose)
3. **Manipulation**  `manipulation_keypoints` → `arm_angle_node`
4. **Robot**  simulation (`wx200`) or hardware (`px150`)

## Troubleshooting

- If YOLO struggles to keep up in real time, lower `imgsz_height`/`imgsz_width` or switch to a smaller model (`yolov8n-pose.pt`).
- If running on limited hardware, keep `device:=cpu` and `half:=False`.
- Ensure the RealSense camera is publishing on `/camera/camera/color/image_rect_raw` before launching YOLO  check with `ros2 topic list`.
