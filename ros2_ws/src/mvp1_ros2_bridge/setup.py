from setuptools import setup, find_packages
import os
from glob import glob

package_name = 'mvp1_ros2'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=[]),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Optionally install any launch files or config
        # Do this like: ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],  # plus any other Python deps you need
    zip_safe=True,
    maintainer='John Miller',
    maintainer_email='your@email.com',
    description='ROS 2 node bridging Joy messages and PoseStamped to Sparkfun motor/servo hardware from mvp1 project.',
    license='Apache 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'motor_node = mvp1_ros2_bridge.servo_node:main',
        ],
    },
)
