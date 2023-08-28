import pi_servo_hat
import time
import transformations

PAN_SERVO = 1
TILT_SERVO =2
MAX_ANGLE = 90

old_pan_angle = old_tilt_angle = MAX_ANGLE/2

NUM_SERVOS = 2 #Required for test_ functions
test = pi_servo_hat.PiServoHat()

def init():
    test.restart()
    # Moves servo position to 0 degrees (1ms), Channel 0
    for servo_i in range(1, NUM_SERVOS):
        test.move_servo_position(servo_i, 0)
    print("Initialized Servo.")

def test_90_servo():
    while True:
        for servo_i in range(1, NUM_SERVOS):
            test.move_servo_position(servo_i, 0)
        print("Going up")
        for i in range(0, 90):
            #print(i)
            for servo_i in range(1, NUM_SERVOS):
                test.move_servo_position(servo_i, i)
                time.sleep(.001)
        print("Going Down")
        for i in range(90, 0, -1):
            #print(i)
            for servo_i in range(1, NUM_SERVOS):
                test.move_servo_position(servo_i, i)
                time.sleep(.001)
            
def test_180_servo():
    while True:
        for servo_i in range(1, NUM_SERVOS):
            test.move_servo_position(servo_i, 0, 180)
        for i in range(0, 90):
            print(i)
            for servo_i in range(1, NUM_SERVOS):
                test.move_servo_position(servo_i, i, 180)
                time.sleep(.001)
        for i in range(90, 0, -1):
            print(i)
            for servo_i in range(1, NUM_SERVOS):
                test.move_servo_position(servo_i, i,180)
                time.sleep(.001)
                
def read_pan_tilt():
    return (test.get_servo_position(PAN_SERVO), test.get_servo_position(TILT_SERVO))

def joy_pan_tilt_abs(pan_angle, tilt_angle):
    '''
    Takes in x/y (pan_angle/tilt_angle) from a joystick between -1 and 1
    And drives the servos accordingly to match the joystick position.
    This is jittery AF.
    
    transformations.map gracefully handles out-of-bounds inputs
    '''
    pan_angle = transformations.map(pan_angle,-1,1,0,MAX_ANGLE)
    tilt_angle = transformations.map(tilt_angle,-1,1,0,MAX_ANGLE)
    
    test.move_servo_position(PAN_SERVO, pan_angle, MAX_ANGLE)
    test.move_servo_position(TILT_SERVO,tilt_angle,MAX_ANGLE)


def joy_pan_tilt_rel(joy_x, joy_y):
    '''
    Takes in a pan_angle and tilt_angle between -1 and 1
    And drives the servos accordingly.
    
    transformations.map gracefully handles out-of-bounds inputs
    '''
    speed = 20
    
    pan_speed = speed * joy_x
    tilt_speed = speed* joy_y
    
    pan_angle = test.get_servo_position(PAN_SERVO) + pan_speed
    tilt_angle = test.get_servo_position(TILT_SERVO) + tilt_speed
    # old_pan_angle += speed * pan_speed # Removed because it requires a global variable old_pan_angle
    # old_tilt_angle += speed * tilt_speed
    
    # old_pan_angle = transformations.clamp(old_pan_angle,0,MAX_ANGLE)
    # old_tilt_angle = transformations.clamp(old_tilt_angle,0,MAX_ANGLE)
    
    pan_angle = transformations.clamp(pan_angle,0,MAX_ANGLE)
    tilt_angle = transformations.clamp(tilt_angle,0,MAX_ANGLE)
    
    test.move_servo_position(PAN_SERVO, pan_angle, MAX_ANGLE)
    test.move_servo_position(TILT_SERVO,tilt_angle,MAX_ANGLE)
    # old_pan_angle = pan_angle
    # old_tilt_angle = tilt_angle
    
        
if __name__ == '__main__':
    try:
        servo_init()
        test_90_servo()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("Ending example.")
        #myMotor.disable()
        sys.exit(0)
