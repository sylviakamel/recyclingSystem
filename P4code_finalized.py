import sys
sys.path.append('../')
from Common.project_library import *

# Modify the information below according to you setup and uncomment the entire section

# 1. Interface Configuration
project_identifier = 'P3B' # enter a string corresponding to P0, P2A, P2A, P3A, or P3B
ip_address = '169.254.25.139' # enter your computer's IP address
hardware = False # True when working with hardware. False when working in the simulation

# 2. Servo Table configuration
short_tower_angle = 270 # enter the value in degrees for the identification tower 
tall_tower_angle = 0 # enter the value in degrees for the classification tower
drop_tube_angle = 180# enter the value in degrees for the drop tube. clockwise rotation from zero degrees

# 3. Qbot Configuration
bot_camera_angle = -21.5 # angle in degrees between -21.5 and 0

# 4. Bin Configuration
# Configuration for the colors for the bins and the lines leading to those bins.
# Note: The line leading up to the bin will be the same color as the bin 

bin1_offset = 0.2 # offset in meters
bin1_color = [1,0,0] # e.g. [1,0,0] for red
bin2_offset = 0.2
bin2_color = [0,1,0]
bin3_offset = 0.2
bin3_color = [0,0,1]
bin4_offset = 0.2
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

def load_container():
    ids = [1,2,3,4,5,6] #putting id's in a list
    count = 0 #setting counter at 0
    bot.rotate(100) #rotating bot for drop off
    #dispensing container 1 and assigning each property to a variable
    cont1_properties = table.dispense_container(random.choice(ids),True) 
    material1, mass1, bin_destination1 = cont1_properties

    count += 1
    time.sleep(2)
        
    pick_up_location = (0.644, 0.0, 0.273) # pick up coordinates
    pick_x, pick_y, pick_z = pick_up_location
    arm.move_arm(pick_x, pick_y, pick_z)
    time.sleep(1)
    arm.control_gripper(45)
    time.sleep(1)

    drop_off_location = bot.position()
    drop_x, drop_y, drop_z = drop_off_location
    drop_x = drop_x - 1.52 #changing drop off values for next container
    drop_y = drop_y - 0.5674 #changing values to be within arms reach
    drop_z = drop_z + 0.54
    arm.move_arm(drop_x,drop_y,drop_z) #calculated drop off coordinates
    time.sleep(1)

    arm.control_gripper(-45)
    time.sleep(1)
    arm.rotate_shoulder(-25)
    time.sleep(1)
    arm.home()
    #dispensing container 2
    cont2_properties = table.dispense_container(random.choice(ids),True) #see above
    material2, mass2, bin_destination2 = cont2_properties
    #if statement with conditions for 2nd container
    if bin_destination2 == bin_destination1 and mass2 + mass1 < 90 and count < 3: 
        pick_up_location = (0.644, 0.0, 0.273)
        pick_x, pick_y, pick_z = pick_up_location #pick up location
        arm.move_arm(pick_x, pick_y, pick_z)
        time.sleep(1)
        arm.control_gripper(45) 
        time.sleep(1)

        drop_off_location = bot.position()
        drop_x, drop_y, drop_z = drop_off_location
        drop_x = drop_x - 1.48
        drop_y = drop_y - 0.5694
        drop_z = drop_z + 0.54
        arm.move_arm(drop_x, drop_y, drop_z) #calculated drop off coordinates
        time.sleep(1)

        arm.control_gripper(-45)
        time.sleep(1)
        arm.rotate_shoulder(-25)
        count += 1 # increase container count by 1
        time.sleep(1)
        arm.home()
        #dispensing container 3
        cont3_properties = table.dispense_container(random.choice(ids),True)
        material3, mass3, bin_destination3 = cont3_properties

        #checking container 3 requirements
        if bin_destination1 == bin_destination3 and mass1 + mass2 + mass3 < 90 and count < 3:
            pick_up_location = (0.644, 0.0, 0.273)
            pick_x, pick_y, pick_z = pick_up_location #pick up location
            arm.move_arm(pick_x, pick_y, pick_z)
            time.sleep(1)
            arm.control_gripper(45) 
            time.sleep(1)

            
            drop_off_location = bot.position()
            drop_x, drop_y, drop_z = drop_off_location
            drop_x = drop_x - 1.42
            drop_y = drop_y - 0.5674
            drop_z = drop_z + 0.54
            arm.move_arm(drop_x, drop_y, drop_z) #calculated drop off coordinates
            time.sleep(1)

            arm.control_gripper(-45)
            time.sleep(1)
            count += 1 # increase container count by 1
            arm.rotate_shoulder(-25)
            time.sleep(1)
            arm.home()
        else:
            table.rotate_table_angle(43) #rotating table

    else:
        table.rotate_table_angle(43)

    bot.rotate(-100)
    print(cont1_properties)
    return cont1_properties


def transfer_container(cont1_properties):
    bin_number = cont1_properties[2]
    print('bin destination: ', bin_number)
    default_speed = 0.04
    l_speed = default_speed #set initial l_speed and r_speed to 0.1
    r_speed = default_speed
    turn_speed = 0.001 # setting initial turn speed
    bot.activate_color_sensor()
    
    while True: # setting a while loop for the motion of the Q bot
        bot.set_wheel_speed([l_speed, r_speed])
        ir_values = bot.line_following_sensors()

        if ir_values == [1, 0]: #if values equal [1,0] then turn left, speed up right wheel and slow down left wheel
            l_speed = default_speed
            r_speed = 1.65*default_speed
        elif ir_values == [0, 1]: # if values equal [0.1] then turn right, speed up left wheel and slow down left
            r_speed = default_speed
            l_speed = 1.65*default_speed
        else:
         # otherwise, speeds will remain the same
            r_speed = default_speed
            l_speed = default_speed
        
            
        sensor_value = bot.read_color_sensor()

        bot_position = bot.position()
        if bin_number == 'Bin01':
            if sensor_value[0] == [1,0,0]:
                if (bot_position[0] > 1 and bot_position[0] < 1.1 and (bot_position[1] > 0.7 and bot_position[1] < 0.77)):
                    print('we are going to bin 1')
                    bot.deactivate_color_sensor()
                    bot.stop()
                    break
        if bin_number == 'Bin02':
            if sensor_value[0] == [0,1,0]:
                if (bot_position[0] > 0 and bot_position[0] < 0.1 and (bot_position[1] > 0.7 and bot_position[1] < 0.77)):
                    print('we are going to bin 2')
                    bot.deactivate_color_sensor()
                    bot.stop()
                    break
        if bin_number == 'Bin03':
            if sensor_value[0] == [0,0,1]:
                if (bot_position[0] > -0.05 and bot_position[0] < 0.08 and (bot_position[1] < -0.67 and bot_position[1] > -0.8)):
                    print('we are going to bin 3')
                    bot.deactivate_color_sensor()
                    bot.stop()
                    break
        if bin_number == 'Bin04':
            if sensor_value[0] == [0,0,0]:
                if (bot_position[0] > 0.95 and bot_position[0] < 1.05 and (bot_position[1] < -0.67 and bot_position[1] > -0.8)):
                    print('we are going to bin 4')
                    bot.deactivate_color_sensor()
                    bot.stop()
                    break


def deposit_container():
    bot.activate_stepper_motor() #activating the rotary actuator
    time.sleep(1)
    bot.rotate_hopper(45) #rotating the hopper by 45 degrees
    time.sleep(2)
    bot.rotate_hopper(0)
    time.sleep(2) #giving it time to sleep so movement is smoother
    bot.deactivate_stepper_motor() #deactivation


def return_home():
    default_speed = 0.04
    l_speed = default_speed #set initial l_speed and r_speed to 0.1
    r_speed = default_speed
    turn_speed = 0.001 # setting initial turn speed
    
    while True: # setting a while loop for the motion of the Q bot
        bot.set_wheel_speed([l_speed, r_speed])
        ir_values = bot.line_following_sensors()
        bot_position = bot.position()
        #if the robot is in the following range of coordinates, stop and break
        if (bot_position[0] > 1.45 and bot_position[0] < 1.55 and (bot_position[1] > -0.05 and bot_position[1] < 0.05)):
            print('Bot has returned home')
            bot.stop()
            break

        if ir_values == [1, 0]: #if values equal [1,0] then turn left, speed up right wheel and slow down left wheel
            l_speed = default_speed
            r_speed = 1.65*default_speed
        elif ir_values == [0, 1]: # if values equal [0.1] then turn right, speed up left wheel and slow down left
            r_speed = default_speed
            l_speed = 1.65*default_speed
        else:
        # otherwise, speeds will remain the same
            r_speed = default_speed
            l_speed = default_speed
        

def main_function():
    while True:
        transfer_container(load_container())
        deposit_container()
        return_home()
        time.sleep(2)
    return 

main_function()

#STUDENT CODE ENDS
#---------------------------------------------------------------------------------
