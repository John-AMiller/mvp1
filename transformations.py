# This code was written by
# https://github.com/joncoop/pygame-xbox360controller
import math

def joystickToDiff(x, y, minJoystick, maxJoystick, minSpeed, maxSpeed): # If x and y are 0, then there is not much to calculate...
    if x == 0 and y == 0:
        return (0, 0)
    

    # First Compute the angle in deg
    # First hypotenuse
    z = math.sqrt(x * x + y * y)

    # angle in radians
    rad = math.acos(math.fabs(x) / z)

    # and in degrees
    angle = rad * 180 / math.pi

    # Now angle indicates the measure of turn
    # Along a straight line, with an angle o, the turn co-efficient is same
    # this applies for angles between 0-90, with angle 0 the coeff is -1
    # with angle 45, the co-efficient is 0 and with angle 90, it is 1

    tcoeff = -1 + (angle / 90) * 2
    turn = tcoeff * math.fabs(math.fabs(y) - math.fabs(x))
    turn = round(turn * 100, 0) / 100

    # And max of y or x is the movement
    mov = max(math.fabs(y), math.fabs(x))

    # First and third quadrant
    if (x >= 0 and y >= 0) or (x < 0 and y < 0):
        rawLeft = mov
        rawRight = turn
    else:
        rawRight = mov
        rawLeft = turn

    # Reverse polarity
    if y < 0:
        rawLeft = 0 - rawLeft
        rawRight = 0 - rawRight

    # minJoystick, maxJoystick, minSpeed, maxSpeed
    # Map the values onto the defined rang
    rightOut = map(rawRight, minJoystick, maxJoystick, minSpeed, maxSpeed)
    leftOut = map(rawLeft, minJoystick, maxJoystick, minSpeed, maxSpeed)

    return (rightOut, leftOut)
    
def map(v, in_min, in_max, out_min, out_max):
    # Check that the value is at least in_min
    if v < in_min:
        v = in_min
    # Check that the value is at most in_max
    if v > in_max:
        v = in_max
    return (v - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def clamp(n, minn, maxn): #Clamp/Constrain value n between min and max values.
    if n < minn:
        return minn
    elif n > maxn:
        return maxn
    else:
        return n