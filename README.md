# Robotic Mimicry

A robotic control system enabling real-time human motion capture and arm mimicry for the **ViperX 150 (px150)** robotic arm, with simulation support for the **WidowX 200 (wx200)** in RViz2.

The package provides the following command-line interfaces:

- **`manipulation_keypoints`** - Real-time YOLO keypoint detection from camera feed
- **`arm_simulation`** - Launch RViz2 simulation environment for WidowX 200
- **`arm_hardware_integration`** - Control PX150 hardware arm
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

## To run the project

This must be done in a series of steps.

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

### Capture data
```bash
ros2 run manipulation_node err_analysis
```


