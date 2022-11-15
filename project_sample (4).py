import sys
sys.path.append('../')
from Common.project_library import *

# Modify the information below according to you setup and uncomment the entire section

# 1. Interface Configuration
project_identifier = 'P3B' # enter a string corresponding to P0, P2A, P2A, P3A, or P3B
ip_address = '169.254.25.139' # enter your computer's IP address
hardware = False # True when working with hardware. False when working in the simulation

# 2. Servo Table configuration
short_tower_angle = 315 # enter the value in degrees for the identification tower 
tall_tower_angle = 90 # enter the value in degrees for the classification tower
drop_tube_angle = 180#270# enter the value in degrees for the drop tube. clockwise rotation from zero degrees

# 3. Qbot Configuration
bot_camera_angle = 0 # angle in degrees between -21.5 and 0

# 4. Bin Configuration
# Configuration for the colors for the bins and the lines leading to those bins.
# Note: The line leading up to the bin will be the same color as the bin 

bin1_offset = 0.2 # offset in meters
bin1_color = [1,0,0] # e.g. [1,0,0] for red
bin2_offset = 0.3
bin2_color = [0,1,0]
bin3_offset = 0.4
bin3_color = [0,0,1]
bin4_offset = 0.5
bin4_color = [0,0,0]

#--------------- DO NOT modify the information below -----------------------------

if project_identifier == 'P0':
    QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
    bot = qbot(0.1,ip_address,QLabs,None,hardware)
    
elif project_identifier in ["P2A","P2B"]:
    QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
    arm = qarm(project_identifier,ip_address,QLabs,hardware)

elif project_identifier == 'P3A':
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    configuration_information = [table_configuration,None, None] # Configuring just the table
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
    
elif project_identifier == 'P3B':
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    qbot_configuration = [bot_camera_angle]
    bin_configuration = [[bin1_offset,bin2_offset,bin3_offset,bin4_offset],[bin1_color,bin2_color,bin3_color,bin4_color]]
    configuration_information = [table_configuration,qbot_configuration, bin_configuration]
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
    bins = bins(bin_configuration)
    bot = qbot(0.1,ip_address,QLabs,bins,hardware)


#---------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------

#numbers = bot.line_following_sensors()
#print(numbers)


def load_container():
    ids = [1,2,3,4,5,6] #putting id's in a list
    count = 0 #setting counter at 0
    
    
    cont1_properties = table.dispense_container(random.choice(ids),True) #dispensing container 1 and assigning each property to a variable
    material1, mass1, bin_destination1 = cont1_properties

    count += 1

    time.sleep(2)
    pick_up_location = (0.644, 0.0, 0.273) # pick up coordinates
    pick_x, pick_y, pick_z = pick_up_location
    arm.move_arm(pick_x, pick_y, pick_z)
    time.sleep(1)
    arm.control_gripper(45)

    time.sleep(1)

    arm.rotate_shoulder(-30)
    arm.rotate_base(-90)
    arm.rotate_shoulder(15)
    arm.control_gripper(-45)
    time.sleep(1)
    arm.home()

    cont2_properties = table.dispense_container(random.choice(ids),True) #see above
    material2, mass2, bin_destination2 = cont2_properties

    if material2 == material1 and mass2 + mass1 < 90 and count < 3: #while loop with conditions for 2nd container
        pick_up_location = (0.644, 0.0, 0.273)
        pick_x, pick_y, pick_z = pick_up_location #pick up location
        arm.move_arm(pick_x, pick_y, pick_z)
        time.sleep(1)
        arm.control_gripper(45) 
        time.sleep(1)
        arm.rotate_shoulder(-30)
        arm.rotate_base(-90)
        arm.rotate_shoulder(5)
        arm.control_gripper(-45)
        count += 1 # increase container count by 1
        time.sleep(1)
        arm.home()
        cont3_properties = table.dispense_container(random.choice(ids),True)
        material3, mass3, bin_destination3 = cont3_properties
        
        if material1 == material3 and mass1 + mass2 + mass3 < 90 and count < 3:
            pick_up_location = (0.644, 0.0, 0.273)
            pick_x, pick_y, pick_z = pick_up_location #pick up location
            arm.move_arm(pick_x, pick_y, pick_z)
            time.sleep(1)
            arm.control_gripper(45) 
            time.sleep(1)
            arm.rotate_shoulder(-30)
            arm.rotate_base(-90)
            arm.rotate_shoulder(5)
            arm.control_gripper(-45)
            count += 1 # increase container count by 1
            time.sleep(1)
            arm.home()
        
    return cont1_properties

load_container()

def transfer_container():
    l_speed = 0.1 #set initial l_speed and r_speed to 0.1
    r_speed = 0.1
    turn_speed = 0.008 # setting initial turn speed
    bot.activate_color_sensor() # activating sensors
    bot.activate_ultrasonic_sensor()
    while True: # setting a while loop for the motion of the Q bot
        ir_values = bot.line_following_sensors()

        if ir_values == [1, 0]: #if values equal [1,0] then turn left, speed up right wheel and slow down left wheel
            print('Turn Left')
            l_speed -= turn_speed
            r_speed += turn_speed
        elif ir_values == [0, 1]: # if values equal [0.1] then turn right, speed up left wheel and slow down left
            print('Turn Right')
            r_speed -= turn_speed
            l_speed += turn_speed
        else:
            print('Go Straight') # otherwise, speeds will remain the same
            r_speed = 0.1
            l_speed = 0.1
        bot.set_wheel_speed([l_speed, r_speed])
        color_sensor = bot.read_color_sensor() #activating colour and ultrasonic sensors
        depth_sensor = bot.read_ultrasonic_sensor()
        # Get target bin color
        target_bin_color = [0,1,0]
        target_bin_offset = 0.2

        if color_sensor[0] == target_bin_color and depth_sensor == target_bin_offset:
            r_speed = 0
            l_speed = 0
            bot.set_wheel_speed([l_speed, r_speed])
            deposit_container() #run this function (dumping the container)
            time.sleep(10) #giving it time to dump the container(s)
            r_speed = 0.1
            l_speed = 0.1
            bot.set_wheel_speed([l_speed, r_speed])
        # Compare color sensor reading to target bin 
transfer_container()

#below is another transfer_container fucntion we're considering
'''
def approach_bin(x):
    bot.forward_time(6.5)
    bot.rotate(95)
    bot.forward_time(6)
    if x == 1:
        #where 1 is equal to metal bin
        bot.rotate(-95)
        bot.forward_time(1)
        bot.rotate(95)
    elif x == 2:
        #where 2 is equal to paper bin
        bot.forward_time(12)
        bot.rotate(-95)
        bot.forward_time(2)
        bot.rotate(95)
    elif x == 3:
        #where 3 is equal to plastic bin
        bot.forward_time(18)
        bot.rotate(100)
        bot.forward_time(15)
        bot.rotate(95)
        bot.forward_time(4)
        bot.rotate(-95)
        bot.forward_time(4)
        bot.rotate(95)
    else:
        #where any other number is equal to garbage bin
        bot.forward_time(18)
        bot.rotate(100)
        bot.forward_time(15)
        bot.rotate(95)
        bot.forward_time(19)
        bot.rotate(-95)
        bot.forward_time(5)
        bot.rotate(95)
    return

approach_bin()'''   

time.sleep(3)

def deposit_container():
    bot.activate_stepper_motor() #activating the rotary actuator
    bot.rotate_hopper(40) #rotating the hopper by 40 degrees
    time.sleep(3)
    bot.rotate_hopper(40)
    time.sleep(2) #giving it time to sleep so movement is smoother
    bot.deactivate_stepper_motor() #deactivation
deposit_container()

def bot_returns_home(x):
    bot.rotate(95) #rotating the bot
    if x == 1: 
        bot.forward_time(1) 
        bot.rotate(-95)
        bot.forward_time(18)
        bot.rotate(100)
        bot.forward_time(15)
        bot.rotate(95)
        bot.forward_time(24)
        bot.rotate(95)
        bot.forward_time(6)
    elif x == 2:
        bot.forward_time(2)
        bot.rotate(-95)
        bot.forward_time(6)
        bot.rotate(100)
        bot.forward_time(15)
        bot.rotate(95)
        bot.forward_time(24)
        bot.rotate(95)
        bot.forward_time(6)
    elif x == 2: #if statements for the motion of the bot returning home
        bot.forward_time(4)
        bot.rotate(-95)
        bot.forward_time(6)
        bot.rotate(95)
        bot.forward_time(6)
    else:
        bot.forward_time(5)
        bot.rotate(-95)
        bot.forward_time(6)
        bot.rotate(95)
        bot.forward(6)
    return

bot_returns_home()       






































'''arm.rotate_shoulder(-30)
    arm.rotate_base(-90)
    arm.rotate_shoulder(15)
    random.choice(ids)

    arm.rotate_shoulder(45)
    arm.rotate_elbow(-30)
    arm.rotate_wrist(-10)
    arm.control_gripper(45)

print(arm.effector_position())
    arm.move_arm(-0.5, 0.2, 0.3)
    time.sleep(2)'''
'''weight = 0
    previous_material = ''

    while True:
        item = table.dispense_container(random.choice(ids),True)
        material, item_weight, bin_destination = item
        if previous_material == '':
            previous_material = material
        weight += item_weight

        if weight >= 90 or count == 3 or material != previous_material:
            print('Qbot moved and emptied')
            weight = 0
            count = 0
            time.sleep(10)
            
        
        # Move from table to cart
        pick_up_location = (0.644, 0.0, 0.273)
        pick_x, pick_y, pick_z = pick_up_location
        arm.move_arm(pick_x, pick_y, pick_z)
        time.sleep(2)
        arm.control_gripper(45)

        time.sleep(2)

        arm.rotate_shoulder(-30)
        arm.rotate_base(-90)
        arm.rotate_shoulder(15)
        arm.control_gripper(-45)
        time.sleep(2)
        arm.home()
        count += 1

        time.sleep(10)
    

random.choice(ids)
'''
   

#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
