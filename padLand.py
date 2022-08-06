from time import sleep

from utlis import *
import cv2
import pandas as pd
from djitellopy import Tello
import time


# myDrone = initializeTello()
# print("battery is: " + str(myDrone.get_battery()))
# myDrone.enable_mission_pads()
# myDrone.set_mission_pad_detection_direction(2)
# myDrone.takeoff()
# pid = myDrone.get_mission_pad_id()
# if pid == 1:
#     print("1")
# else:
#     print("didnt recognized mission pad. abort mission")
#     myDrone.land()
# time.sleep(3)
# # myDrone.go_xyz_speed_mid(100, 20, 0, 20, 1)
# myDrone.move_forward(50)
# time.sleep(3)
# print("moved forward")
# # myDrone.go_xyz_speed(-100, -20, 0, 20)
# myDrone.move_back(50)
# time.sleep(3)
# print("moved backwards")
# pid = myDrone.get_mission_pad_id()
# if pid == 1:
#     print("1")
# else:
#     print("none")
# time.sleep(3)
#
# print("battery is: " + str(myDrone.get_battery()))
# myDrone.land()

if __name__ == '__main__':
    myDrone = initializeTello()
    print("battery is: " + str(myDrone.get_battery()))
    myDrone.enable_mission_pads()
    myDrone.set_mission_pad_detection_direction(2)
    myDrone.takeoff()
    #myDrone.move_up(30)
    pid = myDrone.get_mission_pad_id()
    time.sleep(2)

    if 0 < pid < 9:
        print("found mission pad number", pid)

        myDrone.go_xyz_speed_mid(-25, -25, 70, 30, pid)
        time.sleep(2)
        # bap
        # dist_x = myDrone.get_mission_pad_distance_x()
        # dist_y = myDrone.get_mission_pad_distance_y()
        # dist_z = myDrone.get_mission_pad_distance_z()
        #
        # print("get mission pad x distance:", dist_x)
        # print("get mission pad y distance:", dist_y)
        # print("get mission pad z distance:", dist_z)

        myDrone.move_forward(25)
        myDrone.move_left(25)

        print("battery is: " + str(myDrone.get_battery()))
        x = myDrone.get_height()
        print(x)
        myDrone.move_down(x)
        print(myDrone.get_height())
        myDrone.land()
    else:
        print("didnt recognized any of the mission pad. abort mission")
        myDrone.land()


    #myDrone.move_right(20)
    #myDrone.move_forward(20)
    # try:
    #     # move y axis
    #     if dist_y < 0:
    #         myDrone.move_forward(abs(dist_y))
    #     else:
    #         myDrone.move_back(dist_y)
    #     # move x axis
    #     if dist_x < 0:
    #         myDrone.move_right(abs(dist_x))
    #     else:
    #         myDrone.move_left(dist_x)
    #     myDrone.move_down(dist_z - 30)
    #     print("moved")
    # except:
    #     print("probably values between -20 and 20")
    #     myDrone.land()

    # print("battery is: " + str(myDrone.get_battery()))
    # myDrone.land()
