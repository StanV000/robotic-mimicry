from setuptools import find_packages, setup

package_name = 'manipulation_node'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'numpy', 'matplotlib', 'psutil'],
    zip_safe=True,
    maintainer='robotics',
    maintainer_email='robotics@example.com',
    description='ROS2 package for real-time robotic arm manipulation using YOLO keypoint detection',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
    'console_scripts': [
        'manipulation_keypoints = manipulation_node.nodes.manipulation_keypoints:main',
        'arm_simulation     = manipulation_node.nodes.arm_simulation:main',
        'arm_hardware_integration = manipulation_node.nodes.arm_hardware_integration:main',
        'arm_angle_node     = manipulation_node.arm_angle_node:main',
        'err_analysis      = manipulation_node.nodes.err_analysis:main',
    ],
},
)
