import xbox360_controller

if __name__ == '__main__':
 
    my_controller = xbox360_controller.Controller()
    
    while (1):
        my_controller.debug_axes()
    
    while (0):
        
        left_x, left_y = my_controller.get_left_stick()
        right_x, right_y = my_controller.get_right_stick()
        
        print('Left Stick moved to {0} {1}'.format(left_x, left_y))
