# mvp1
First iteration of building a Telepresence MVP

# ros2_ws

This ROS 2 package bridges the `/openxr/left_controller` and `/openxr/HMD` topics to the SparkFun Qwiic SCMD (motor) and Qwiic servo pHAT drivers, reusing code from the original `mvp1` repository (`sf_motor.py`, `sf_servo.py`, `transformations.py`). It also publishes the current servo orientation as `/robot/head`.

## Prerequisites

- **ROS 2** (Galactic, Humble, Iron; Humble recomended) installed and sourced.
- **SparkFun Qwiic SCMD** and **SparkFun Qwiic servo** Python libraries.
  sudo pip3 install sparkfun-qwiic-scmd sparkfun-qwiic-servos pi-servo-hat

# Function
  The node makes subscriptions to:
   - /openxr/left_controller (sensor_msgs/Joy) – The axes[0] and axes[1] values in [-1, +1] are passed into sf_motor.joy_motor_move() to drive the motors in differential drive mode.
   - /openxr/HMD (geometry_msgs/PoseStamped) – The quaternion in the pose is converted to Euler angles. The yaw/pitch are mapped to [-1..+1], then fed into sf_servo.joy_pan_tilt_abs() to move pan/tilt. \

  The node publishes:
   - /robot/head (geometry_msgs/PoseStamped) – Contains [0, 0, 0.076] translation and a quaternion derived from (roll=0, pitch, yaw) based on the current servo angles read from sf_servo.read_pan_tilt().

  In the joy_callback, we take joy_msg.axes[0] (X) and joy_msg.axes[1] (Y), both [−1..+1], and directly call sf_motor.joy_motor_move(x, y).
  
  The existing joy_motor_move method in sf_motor.py calls transformations.joystickToDiff to apply a differential-drive mix (again using [−1..+1] input). That results in the appropriate forward/reverse commands to   the SCMD hardware.
  
## Installation & Build Instructions

  1. **Make a ROS2 Workspace once ROS2 is installed and sourced:**
      

  3. **Clone (or copy) this repository** into your ROS 2 workspace:
     ```bash
     cd ~/ros2_ws/src
     git clone <your_repo_url> mvp1_ros2
   
# Troubleshooting
   - Ensure your I2C devices (SCMD, servo pHAT) are properly connected.
   - Check "sudo i2cdetect -y 1" to verify addresses.
   - If you see import errors for sparkfun-qwiic-scmd or sparkfun-qwiic-servos, double-check your pip install environment.
