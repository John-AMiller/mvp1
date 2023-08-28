#This code uses
# A xbox360 controller
# A Sparkfun Servo Controller for head-tilt
# A Sparkfun SCMD Motor Controller to Move
import sys
import signal
import transformations
from xbox360controller import Xbox360Controller as x360
#from jetbot import Robot #This crashes big-time on a venv

import sf_motor
import sf_servo

PAN_SERVO = 0
TILT_SERVO =1

#This code may rely on running the first two commands in basic_motion.ipynb
def on_axis_moved(axis):
    if (axis.name == "axis_l"): #Movement
        #robot.set_motors(left_motor, right_motor)
        sf_motor.joy_motor_move(axis.x, axis.y)
    elif (axis.name == "axis_r"): #Looking
        sf_servo.joy_pan_tilt_abs(axis.x,axis.y)

        

if (__name__ == '__main__'):
    
    sf_servo.init()
    sf_motor.init()
    #robot = Robot()
  
    
    while (1): 
        #left_x, left_y = my_controller.get_left_stick()
        #right_x, right_y = my_controller.get_right_stick()
        try:
            with x360 (0, axis_threshold=0.2) as controller:
                controller.axis_l.when_moved = on_axis_moved
                controller.axis_r.when_moved = on_axis_moved
                signal.pause()
        except KeyboardInterrupt:
            pass

