#!/usr/bin/env python3

# Authors: John Miller (JM) & Andrew Toth (AT)
# Last Change: 1/30/25
# What Changed: Updated Line Documentation (JM)
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Joy
from geometry_msgs.msg import PoseStamped
from builtin_interfaces.msg import Time

import math
import time
import sys

# Import existing modules:
import sf_motor  # scmd motor control
import sf_servo  # servo control
import transformations  # joystickToDiff, clamp, map, etc.

class MotorServoNode(Node):
    def __init__(self):
        super().__init__('motor_servo_node')

        self.get_logger().info("Initializing MotorServoNode...")

        # ---------------------------------------------------
        #  A) Initialize existing hardware interfaces
        # ---------------------------------------------------
        try:
            sf_motor.init()  # from sf_motor.py
            self.get_logger().info("SCMD Motor driver initialized.")
        except Exception as e:
            self.get_logger().error(f"Could not init SCMD: {e}")

        try:
            sf_servo.init()  # from sf_servo.py
            self.get_logger().info("Servo pHAT initialized.")
        except Exception as e:
            self.get_logger().error(f"Could not init Servos: {e}")

        # Store last-known servo angles (degrees), if you want to track them
        # Can also read from hardware on each publish if you want.
        self.current_pan_deg = 0.0
        self.current_tilt_deg = 0.0

        # ---------------------------------------------------
        #  B) Create ROS Subscriptions
        # ---------------------------------------------------
        # 1) Subscribe to Joy for motor movement
        self.joy_sub = self.create_subscription(
            Joy,
            '/openxr/left_controller',
            self.joy_callback,
            10
        )

        # 2) Subscribe to PoseStamped for servo orientation
        self.hmd_sub = self.create_subscription(
            PoseStamped,
            '/openxr/HMD',
            self.hmd_callback,
            10
        )

        # ---------------------------------------------------
        #  C) Create ROS Publisher: PoseStamped of servo angles
        # ---------------------------------------------------
        self.head_pub = self.create_publisher(PoseStamped, '/robot/head', 10)

        # Publish the servo pose at 10Hz
        self.timer = self.create_timer(0.1, self.publish_head_pose)

        self.get_logger().info("MotorServoNode ready!")

    # --------------------------------------------------------
    # 1) Callback: Joy -> Motor Movement
    # --------------------------------------------------------
    def joy_callback(self, joy_msg):
        """
        joy_msg.axes[0], joy_msg.axes[1] range: -1..+1
        We simply pass these to sf_motor.joy_motor_move.
        """
        # x = left stick X, y = left stick Y
        x = joy_msg.axes[0]
        y = joy_msg.axes[1]

        # Call existing code from sf_motor.py
        sf_motor.joy_motor_move(x, y)
        # That code also calls transformations.joystickToDiff internally.

    # --------------------------------------------------------
    # 2) Callback: Pose -> Servo Orientation
    # --------------------------------------------------------
    def hmd_callback(self, pose_msg):
        """
        Convert the quaternion from /openxr/HMD into Euler angles,
        then use them (e.g. yaw->pan, pitch->tilt) to drive the servos.

        Adjust the math and any offsets/clamping as needed to match
        your hardware orientation.
        """
        # Extract quaternion
        qx = pose_msg.pose.orientation.x
        qy = pose_msg.pose.orientation.y
        qz = pose_msg.pose.orientation.z
        qw = pose_msg.pose.orientation.w

        # Convert quaternion -> Euler (roll, pitch, yaw in radians)
        roll, pitch, yaw = self.quaternion_to_euler(qx, qy, qz, qw)

        # Example:
        #   Let pan = yaw, tilt = pitch
        #   Convert to a -1..+1 range or directly to degrees?
        # Existing "joy_pan_tilt_abs" or "joy_pan_tilt_rel" expects [-1..1].
        # Simple mapping from radians to [-1..1].
        # You might want to refine scaling after testing.

        # Max “usable” yaw/pitch range in radians. Example ±90 deg => ±1.57 rad
        max_angle_rad = math.radians(90)

        # clamp roll/pitch/yaw to ±max_angle_rad
        pitch = max(-max_angle_rad, min(pitch, max_angle_rad))
        yaw   = max(-max_angle_rad, min(yaw,   max_angle_rad))

        # scale from ±max_angle_rad => ±1.0
        pan_input  = yaw   / max_angle_rad
        tilt_input = pitch / max_angle_rad

        # Call existing servo code, absolute positioning:
        # That function: joy_pan_tilt_abs(pan, tilt) also expects [-1..1]
        sf_servo.joy_pan_tilt_abs(pan_input, tilt_input)

    # --------------------------------------------------------
    # 3) Publish servo pose => /robot/head
    # --------------------------------------------------------
    def publish_head_pose(self):
        """
        Read servo angles from sf_servo, convert them to a PoseStamped
        with (roll=0, pitch, yaw) from servo, and a fixed translation of [0,0,0.076].
        """
        pose_msg = PoseStamped()

        # Fill header with current time
        pose_msg.header.stamp = self.get_clock().now().to_msg()
        pose_msg.header.frame_id = "servo_head_link"

        # Position is fixed [0, 0, 0.076]
        pose_msg.pose.position.x = 0.0
        pose_msg.pose.position.y = 0.0
        pose_msg.pose.position.z = 0.076

        # Read servo angles from hardware (in degrees)
        pan_deg, tilt_deg = sf_servo.read_pan_tilt()

        # Convert from degrees to radians
        # (The code: read_pan_tilt() returns 0..90 by default, adapt to your setup)
        # Suppose 0..90 servo range means -45..+45 in “robot space”
        # For now, assume 0 deg => -45 rad, 90 deg => +45 rad.

        # Example guess: if 0 servo deg is -45° real, 90 servo deg is +45° real,
        # then do a linear transform around the midpoint (45).
        pan_radians  = math.radians(pan_deg - 45)  # shift so 45 deg => 0 rad
        tilt_radians = math.radians(tilt_deg - 45)

        roll = 0.0
        pitch = tilt_radians
        yaw   = pan_radians

        # Convert Euler->Quaternion
        qx, qy, qz, qw = self.euler_to_quaternion(roll, pitch, yaw)
        pose_msg.pose.orientation.x = qx
        pose_msg.pose.orientation.y = qy
        pose_msg.pose.orientation.z = qz
        pose_msg.pose.orientation.w = qw

        self.head_pub.publish(pose_msg)

    # --------------------------------------------------------
    # Quaternion <-> Euler Utility
    # --------------------------------------------------------
    def quaternion_to_euler(self, x, y, z, w):
        """
        Convert quaternion (x, y, z, w) to Euler angles (roll, pitch, yaw) in radians.
        """
        # Code from your transformations
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll = math.atan2(t0, t1)

        t2 = +2.0 * (w * y - z * x)
        t2 =  1.0 if t2 >  1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch = math.asin(t2)

        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw = math.atan2(t3, t4)

        return (roll, pitch, yaw)

    def euler_to_quaternion(self, roll, pitch, yaw):
        """
        Convert Euler angles (radians) to quaternion (x, y, z, w).
        """
        cy = math.cos(yaw * 0.5)
        sy = math.sin(yaw * 0.5)
        cp = math.cos(pitch * 0.5)
        sp = math.sin(pitch * 0.5)
        cr = math.cos(roll * 0.5)
        sr = math.sin(roll * 0.5)

        w = cr*cp*cy + sr*sp*sy
        x = sr*cp*cy - cr*sp*sy
        y = cr*sp*cy + sr*cp*sy
        z = cr*cp*sy - sr*sp*cy
        return (x, y, z, w)

def main(args=None):
    rclpy.init(args=args)
    node = MotorServoNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.get_logger().info("Shutting down MotorServoNode...")
        # Optionally can disable motors:
        sf_motor.myMotor.disable()
        rclpy.shutdown()

if __name__ == '__main__':
    main()



if __name__ == '__main__':
    main()
