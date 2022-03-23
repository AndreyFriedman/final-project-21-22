from utils2 import *
import cv2
import pandas as pd
import keyboard
import logging
from threading import Thread


w, h = 360, 240
pid = [0.6, 0.45, 0]
pid2 = [0.3, 0.2]
pError = 0
pErrorfb = 0
pErrorh = 0
startCounter = 0  # for no Flight 1   - for flight 0
loop_counter = 0


# create logging
logging.basicConfig(filename='TelloLogFile.log', filemode='w', level=logging.INFO)
out = cv2.VideoWriter('TelloVideoRecorder.avi', -1, 20.0, (640,480))

myDrone = initializeTello()
print(myDrone.get_battery())


# try:
while True:

    # Flight
    if startCounter == 0:
        myDrone.takeoff()
        logging.info("Take off")
        startCounter = 1

    # Step 1
    img = telloGetFrame(myDrone, w, h)
    # if myDrone.get_height() < 15:
    #     myDrone.land()
    #     break
    # Step 2
    img, centers, cordinates, areas = findMarker(img, 33, "DICT_ARUCO_ORIGINAL")
    if len(centers) > 0:
        pError, keepRecording = trackMarker(myDrone, centers[0][0], centers[0][1], areas[0], w, h, pError)
    else:
        pError, keepRecording = trackMarker(myDrone, 0, 0, 0, w, h, pError)

    # if drone land and we finished
    if not keepRecording:
        myDrone.land()
        logging.info("Land")
        print(myDrone.get_battery())
        out.release()
        break

    if loop_counter == 100:
        logging.info("Battery:", myDrone.get_battery(), "Height:", myDrone.get_height(), "X Speed:",
                     myDrone.get_speed_x(), "Y Speed:", myDrone.get_speed_y(),
                     "Z Speed:", myDrone.get_speed_z(), "Temperature:", myDrone.get_temperature(), "Barometer:",
                     myDrone.get_barometer())
    else:
        loop_counter += 1

    cv2.imshow('Image', img)
    out.write(img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        myDrone.land()
        logging.info("Land")
        print(myDrone.get_battery())
        out.release()
        break

