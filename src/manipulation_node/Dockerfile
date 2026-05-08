FROM osrf/ros:humble-desktop

ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=humble

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-vcstool \
    git \
    wget \
    curl \
    tmux \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install numpy<2 matplotlib psutil opencv-python ultralytics autopep8

RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-humble-realsense2-camera \
    ros-humble-librealsense2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
RUN mkdir -p src

# Copy this package into a workspace under src/
COPY . /workspace/src/manipulation_node

# Clone the YOLO ROS packages and Interbotix XSArm sources needed to run the launch commands.
RUN cd /workspace/src && git clone --depth 1 https://github.com/mgonzs13/yolo_ros.git && \
    git clone --depth 1 https://github.com/Interbotix/interbotix_ros_manipulators.git

RUN if [ ! -f /workspace/src/yolo_ros/yolov8n-pose.pt ]; then \
      wget -O /workspace/src/yolo_ros/yolov8n-pose.pt \
        https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n-pose.pt; \
    fi

RUN rosdep update || true
RUN rosdep install --from-paths src --ignore-src -r -y

RUN . /opt/ros/humble/setup.sh && cd /workspace && colcon build --symlink-install

COPY scripts /workspace/scripts
RUN chmod +x /workspace/scripts/start_all.sh

ENTRYPOINT ["/workspace/scripts/start_all.sh"]
