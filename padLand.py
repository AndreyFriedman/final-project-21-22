from time import sleep

from utlis import *
import cv2
import pandas as pd
from djitellopy import Tello


myDrone = initializeTello()
print("battery is: " + str(myDrone.get_battery()))
myDrone.enable_mission_pads()
myDrone.set_mission_pad_detection_direction(2)
myDrone.takeoff()
pid = myDrone.get_mission_pad_id()
if pid == 1:
    print("1")
else:
    print("none")
myDrone.go_xyz_speed_mid(100, 20, 0, 20, 1)
print("moved")
myDrone.go_xyz_speed(-100, -20, 0, 20)
pid = myDrone.get_mission_pad_id()
if pid == 1:
    print("1")
else:
    print("none")

print("battery is: " + str(myDrone.get_battery()))
myDrone.land()
