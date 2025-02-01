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
   - /openxr/left_controller (sensor_msgs/Joy) – The axes[0] and axes[1] values in [-1, +1] are passed into sf_motor.joy_motor_move() to drive the motors in differential mode.
   - /openxr/HMD (geometry_msgs/PoseStamped) – The quaternion in the pose is converted to Euler angles. The yaw/pitch are mapped to [-1..+1], then fed into sf_servo.joy_pan_tilt_abs() to move pan/tilt.
