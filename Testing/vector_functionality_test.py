import anki_vector as av
from anki_vector.util import degrees
from anki_vector.connection import ControlPriorityLevel
import numpy as np
import cv2
from PIL import Image

def main(args=None):
    command_list = "list of commands =\n\
        h <speed val> (moves head at speed val)\n\
        f <speed val> (moves forklift at speed val)\n\
        t <(speed left,speed right)> (sets the tread speeds)\n\
        s *<message> (message will come out of speakers)\n\
        l (laser range finder will print data to screen)\n\
        e <(pose)> (encoder data will print to screen, can set pose by passing (x,y,z))\n\
        a (accelerometer data will print to screen)\n\
        g (gyro data will print to screen)\n\
        i *<path/to/image/data> (sets the image on robots screen to that of img at path)\n\
        c (displays robot camera feed)\n\
        x (floor sensor true or false data will be printed)\n\
        y (capacitor data will be printed\n\
        r (resets all parameters)\n\
        q (ends the program)\n\
        d (displays the commands available)\n"
        
        
    print(command_list)
    robot = av.Robot("00804458",behavior_control_level=ControlPriorityLevel.OVERRIDE_BEHAVIORS_PRIORITY)
    # robot = av.Robot("005030d4",behavior_control_level=ControlPriorityLevel.OVERRIDE_BEHAVIORS_PRIORITY)
    print(robot.conn._has_control) # states true if u have succesfull connection established)
    robot.connect()
    print(robot.conn._has_control)
    # robot.behavior.set_lift_height(1)
    flag = True
    prox_flag = False
    encod_flag = False
    accel_flag = False
    img_flag = False
    gyro_flag = False
    input()
    while flag:
        c = input()
        if c.startswith("h"):
            val = c.strip().split(" ")[-1]
            robot.motors.set_head_motor(float(val))
        if c.startswith("f"):
            val = c.strip().split(" ")[-1]
            robot.motors.set_lift_motor(float(val))
        if c.startswith("t"):
            val = c.strip().split("(")[-1]
            speed = [float(val.split(",")[0]),float(val.split(",")[-1].split(")")[0])]
            robot.motors.set_wheel_motors(speed[0],speed[1])
        if c.startswith("s"):
            val = c.strip().split("*")[-1]
            robot.behavior.say_text(val)
        if c.startswith("l"):
            prox_flag = True
        if c.startswith("e"):
            encod_flag = True
            val = c.strip().split("(")[-1]
            p = [float(val.split(",")[0]),float(val.split(",")[1]),float(val.split(",")[2].split(")")[0])]
            pose = av.util.Pose(p[0],p[1],p[2],angle_z=av.util.Angle(degrees=0))
            robot.behavior.go_to_pose(pose)
        if c.startswith("a"):
            accel_flag = True
        if c.startswith("g"):
            gyro_flag = True
        if c.startswith("i"):
            path = c.strip().split("*")[-1]
            image_file = Image.open(path)
            screen_data = av.screen.convert_image_to_screen_data(image_file)
            robot.screen.set_screen_with_image_data(screen_data,4.0)
        if c.startswith("c"):
            img_flag = True  
        if c.startswith("x"):
            print("Is cliff detected: {}".format(robot.status.is_cliff_detected)) 
        if c.startswith("y"):
            print("Capacitor reading = {}".format(robot.touch.last_sensor_reading.raw_touch_value))
        if c.startswith("r"):
            robot.motors.stop_all_motors()
            robot.camera.close_camera_feed()
            prox_flag = False
            encod_flag = False
            accel_flag = False
            img_flag = False
            gyro_flag = False
        if c.startswith("q"):
            flag = False
        if c.startswith("d"):
            print(command_list)

        if prox_flag:
            print("Proximity data = {}".format(robot.proximity.last_sensor_reading.distance))
        if encod_flag:
            print("Current pose = {}".format(robot.pose))
        if accel_flag:
            print("acceleration data = {}".format(robot.accel))
        if gyro_flag:
            print("gyro data = {}".format(robot.gyro))
        if img_flag:
            robot.camera.init_camera_feed()
            cv_image = cv2.cvtColor(np.array(robot.camera.latest_image.raw_image),cv2.COLOR_RGB2BGR)
            print("Image dimensions = {}".format(cv_image.shape))
            cv2.imshow("camera feed",cv_image)
            cv2.waitKey(1)
    robot.disconnect()



if __name__ == '__main__':
    main()