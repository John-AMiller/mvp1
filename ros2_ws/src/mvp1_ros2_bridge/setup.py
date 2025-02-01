from setuptools import setup

package_name = 'mvp1_ros2'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='John Miller',
    maintainer_email='johnamiller056@gmail.com',
    description='ROS 2 node bridging Joy/Pose to mvp1 code',
    license='Apache 2.0',
    entry_points={
        'console_scripts': [
            'motor_node = mvp1_ros2_bridge.motor_servo_node:main'
        ],
    },
)
