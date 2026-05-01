# Robotic Mimicry

A robotic control system enabling real-time human motion capture and arm mimicry for the **ViperX 150 (px150)** robotic arm, with simulation support for the **WidowX 200 (wx200)** in RViz2.

## Overview

This project implements a complete pipeline for capturing human poses via YOLO-based keypoint detection, processing the captured data, and executing corresponding manipulator movements on hardware or in simulation.

## Features

- **YOLO-based Pose Detection**: Real-time human keypoint extraction using YOLO
- **Intel RealSense Integration**: Hardware camera support for live pose capture
- **ROS 2 Architecture**: Modular ROS 2 nodes for distributed processing
- **Hardware & Simulation**: 
  - ViperX 150 arm hardware integration
  - RViz2 simulation for WidowX 200
- **Pose Logging & Analysis**: 
  - CSV-based pose data recording
  - Statistical analysis of capture accuracy
  - Visualization of results

## Project Structure

```
robotic-mimicry/
├── README.md
├── src/
│   ├── manipulation_node/          # Main ROS 2 package
│   │   ├── manipulation_node/
│   │   │   ├── manipulation_keypoints.py    # Keypoint extraction
│   │   │   ├── arm_simulation.py            # RViz2 simulation interface
│   │   │   ├── arm_hardware_integration.py  # px150 hardware control
│   │   │   ├── arm_angle_node.py            # Angle computation
│   │   │   ├── err_analysis.py              # Error analysis utilities
│   │   │   ├── plot_csv.py                  # Visualization & plotting
│   │   │   ├── *.csv                        # Pose data logs
│   │   │   └── *.png                        # Analysis results
│   │   ├── package.xml
│   │   ├── setup.py
│   │   └── setup.cfg
│   └── pose_log.csv                # Main pose dataset
```

## Entry Points

The package provides the following command-line interfaces:

- **`manipulation_keypoints`** - Real-time YOLO keypoint detection from camera feed
- **`arm_simulation`** - Launch RViz2 simulation environment for WidowX 200
- **`arm_hardware_integration`** - Control ViperX 150 hardware arm
- **`arm_angle_node`** - Compute and process arm joint angles
- **`err_analysis`** - Analyze capture accuracy and generate statistical reports

## Dependencies

**ROS 2 Packages:**
- `rclpy` - ROS 2 Python client library
- `yolo_msgs` - YOLO detection message definitions

**Testing:**
- `pytest`
- `ament_flake8`
- `ament_copyright`
- `ament_pep257`

## Installation

### Prerequisites
- ROS 2 (tested on Humble)
- Python 3.8+
- Intel RealSense SDK (for camera integration)
- YOLOv8 dependencies

### Docker Setup (Coming Soon)

A Docker containerization is currently in progress to streamline installation. The Docker setup will automatically:

- Install YOLO and dependencies
- Configure Intel RealSense camera drivers
- Set up all Python dependencies
- Pre-configure ROS 2 environment

Once available, you'll be able to run everything with a single command.

### Manual Installation

```bash
# Clone the repository
git clone <repo-url>
cd robotic-mimicry

# Source ROS 2 setup
source /opt/ros/<ros-distro>/setup.bash

# Build the package
colcon build

# Source the workspace
source install/setup.bash
```

## Usage

### Capture Human Poses
```bash
ros2 run manipulation_node manipulation_keypoints
```

### Simulate Arm Movement
```bash
ros2 run manipulation_node arm_simulation
```

### Control Hardware Arm
```bash
ros2 run manipulation_node arm_hardware_integration
```

### Analyze Capture Accuracy
```bash
ros2 run manipulation_node err_analysis
```

## Data

The project includes pose datasets for validation:
- `45_degree_pose.csv` - 45° angle capture session
- `horizontal_pose.csv` - Horizontal pose capture session
- `upward_pose.csv` - Upward pose capture session
- `pose_log.csv` - Primary pose dataset

Associated analysis images:
- `*_results.png` - Raw pose trajectory plots
- `*_stats.png` - Statistical accuracy analysis
- `error_rate_between_each_pose.png` - Cross-pose error comparison

## Getting Started

1. Ensure ROS 2 is installed and sourced
2. Build the package: `colcon build`
3. Run pose detection: `ros2 run manipulation_node manipulation_keypoints`
4. Monitor results via RViz2 or hardware output

## License

TODO: License declaration

## Contributing

For issues, questions, or contributions, please open a GitHub issue.

## Maintainer

**robotics** - robotics@todo.todo

---

**Status**: Under active development. Docker setup coming soon.
