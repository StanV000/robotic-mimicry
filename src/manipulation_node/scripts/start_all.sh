#!/bin/bash
set -e

SESSION="manipulation_node"
if tmux has-session -t "$SESSION" 2>/dev/null; then
    tmux attach-session -t "$SESSION"
    exit 0
fi

source /opt/ros/humble/setup.bash
source /workspace/install/setup.bash

tmux new-session -d -s "$SESSION" -n realsense \
    "bash -lc 'ros2 launch realsense2_camera rs_launch.py'"

tmux new-window -t "$SESSION" -n yolo \
    "bash -lc 'ros2 launch yolo_bringup yolo.launch.py input_image_topic:=/camera/camera/color/image_rect_raw model:=yolov8n-pose.pt device:=cpu imgsz_height:=320 imgsz_width:=320 augment:=False half:=False'"

tmux new-window -t "$SESSION" -n keypoints \
    "bash -lc 'ros2 run manipulation_node manipulation_keypoints'"

tmux new-window -t "$SESSION" -n armangle \
    "bash -lc 'ros2 run manipulation_node arm_angle_node'"

tmux new-window -t "$SESSION" -n xsarm \
    "bash -lc 'ros2 launch interbotix_xsarm_control xsarm_control.launch.py robot_model:=wx200 use_sim:=true use_rviz:=true'"

exec tmux attach-session -t "$SESSION"
