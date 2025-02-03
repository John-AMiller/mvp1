# mvp1
First iteration of building a Telepresence MVP

# ros2_ws
This code was written by John Miller (John-AMiller, johnamiller056@gmail.com), known from here as the author, and was written under the Apache 2.0 Open Source License. However, since this code was written under "work for hire", commissioned on the site Fiverr for the client telepresent, known on github as ajtoth91 (Andrew Toth), the client now owns the copyright to and only to the code contained within this fork and the origional mvp1 repository. The client acknowleges that they do not own the copyright to any other code located within any of the author's other GitHub repositories. Since the client owns the copyright to this code, it is there decision to retain the Apache 2.0 Open Source License or to make the code proprietary.

This ROS 2 package bridges the `/openxr/left_controller` and `/openxr/HMD` topics to the SparkFun Qwiic SCMD (motor) and Qwiic servo pHAT drivers, reusing code from the original `mvp1` repository (`sf_motor.py`, `sf_servo.py`, `transformations.py`). It also publishes the current servo orientation as `/robot/head`.

## Prerequisites

- **ROS 2** (Galactic, Humble, Iron; Humble recomended) installed and sourced. https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html
- ROS2 does require ubuntu 22.04, recommend following this to install ubuntu 22.04 on the Jetson Nano: https://github.com/xronos-inc/jetson-nano-ubuntu-22.04
- **SparkFun Qwiic SCMD** and **SparkFun Qwiic servo** Python libraries.
  sudo pip3 install sparkfun-qwiic-scmd sparkfun-qwiic-servos pi-servo-hat

## Function
  The node makes subscriptions to:
   - /openxr/left_controller (sensor_msgs/Joy) – The axes[0] and axes[1] values in [-1, +1] are passed into sf_motor.joy_motor_move() to drive the motors in differential drive mode.
   - /openxr/HMD (geometry_msgs/PoseStamped) – The quaternion in the pose is converted to Euler angles. The yaw/pitch are mapped to [-1..+1], then fed into sf_servo.joy_pan_tilt_abs() to move pan/tilt. \

  The node publishes:
   - /robot/head (geometry_msgs/PoseStamped) – Contains [0, 0, 0.076] translation and a quaternion derived from (roll=0, pitch, yaw) based on the current servo angles read from sf_servo.read_pan_tilt().

  In the joy_callback, we take joy_msg.axes[0] (X) and joy_msg.axes[1] (Y), both [−1..+1], and directly call sf_motor.joy_motor_move(x, y).
  
  The existing joy_motor_move method in sf_motor.py calls transformations.joystickToDiff to apply a differential-drive mix (again using [−1..+1] input). That results in the appropriate forward/reverse commands to   the SCMD hardware.
  
## Installation & Build Instructions

  1. **Make a ROS2 Workspace once ROS2 is installed and sourced:**
      ```bash
      mkdir -p ~/ros2_ws/src

  2. **Clone (or copy) this repository** into your ROS 2 workspace:
     ```bash
     cd ~/ros2_ws/src
     git clone <your_repo_url> mvp1_ros2
     
  3. **Build the package:**
     ```bash
     cd
     cd ~/ros2_ws/
     colcon build
     source install/local_setup.bash
   
## Troubleshooting
   - Ensure your I2C devices (SCMD, servo pHAT) are properly connected.
   - Check "sudo i2cdetect -y 1" to verify addresses.
   - If you see import errors for sparkfun-qwiic-scmd or sparkfun-qwiic-servos, double-check your pip install environment.

## Auto Start at Boot
   - On a Jetson Nano (systemd-based environment), you can run the node automatically at boot with a systemd service:
   - 

## Customization
   - Motor Mixing: Adjust in transformations.py (function joystickToDiff) if you need different curves, max speeds, or direction flips.
   - Servo Ranges: In sf_servo.py, you can change servo angle limits, or switch from joy_pan_tilt_abs to joy_pan_tilt_rel depending on how you want to interpret HMD input.
   - Quaternion to Euler: In servo_node.py, you can fine-tune how you interpret roll/pitch/yaw (e.g., offsets, clamp angles, etc.) to match the physical servo geometry.
   - Pose Publication: If you have a different geometry for the servo “head,” adjust the fixed translation [0.0, 0.0, 0.076] or recast how you publish the orientation.
