import qwiic_scmd
import transformations

MOTOR_LEFT = 0
MOTOR_RIGHT= 1


myMotor = qwiic_scmd.QwiicScmd()

def init():
    if myMotor.connected == False:
        print("Motor Driver not connected. Check connections.", \
                file=sys.stderr)
        return
    myMotor.begin()
    print("Motor initialized.")
    myMotor.set_drive(MOTOR_LEFT,0,0)
    myMotor.set_drive(MOTOR_RIGHT,0,0)
    print("Motor Init Complete.")

def motor_test():
    import time
    import sys
    import math
    FWD = 0
    BWD = 1
    while True:
        speed = 20
        for speed in range(20,255):
                print(speed)
                myMotor.set_drive(MOTOR_RIGHT,FWD,speed)
                myMotor.set_drive(MOTOR_LEFT,BWD,speed)
                time.sleep(.05)
        for speed in range(254,20, -1):
                print(speed)
                myMotor.set_drive(MOTOR_RIGHT,FWD,speed)
                myMotor.set_drive(MOTOR_LEFT,BWD,speed)
                time.sleep(.05)
                
def joy_motor_move(joy_x,joy_y):
    '''
    joy_x & joy_y are between -1 and +1
    left_speed = [-1, 1]
    right_speed= [-1, 1]
    '''
    FWD = 0
    BWD = 1
    
    left_speed, right_speed = transformations.joystickToDiff(joy_x, joy_y, -1, 1, -255,255)
    
    if left_speed < 0: #negative
        myMotor.set_drive(MOTOR_LEFT, BWD,-left_speed)
    else:
        myMotor.set_drive(MOTOR_LEFT, FWD, left_speed)
    if right_speed < 0: #negative
        myMotor.set_drive(MOTOR_RIGHT, BWD,-right_speed)
    else:
        myMotor.set_drive(MOTOR_RIGHT, FWD, right_speed)    
    
if __name__ == '__main__':
    try:
        motor_init()
        motor_test()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("Ending example.")
        myMotor.disable()
        sys.exit(0)
