from utils2 import *
import cv2
import pandas as pd
import keyboard
# from threading import Thread

w, h = 360, 240
pid = [0.6, 0.45, 0]
pid2 = [0.3, 0.2]
pError = 0
pErrorfb = 0
pErrorh = 0
startCounter = 0  # for no Flight 1   - for flight 0
loop_counter = 0
currentID = 33

myDrone = initializeTello()
print(myDrone.get_battery())

# create logging
with open('logging.txt', 'w') as f:
    # try:
    while True:

        # Flight
        if startCounter == 0:
            myDrone.takeoff()
            myDrone.move_up(20)
            f.write("Take off\n")
            startCounter = 1

        # Step 1
        img = telloGetFrame(myDrone, w, h)
        # if myDrone.get_height() < 15:
        #     myDrone.land()
        #     break

        # Step 2
        img, centers, cordinates, areas = findMarker(img, currentID, "DICT_ARUCO_ORIGINAL")
        if len(centers) > 0:
            # pError, keepRecording = trackMarker(myDrone, centers[0][0], centers[0][1], areas[0], w, h, pError)
            pError = trackMarker(currentID, myDrone, centers[0][0], centers[0][1], areas[0], w, h, pError)
        else:
            # pError, keepRecording = trackMarker(myDrone, 0, 0, 0, w, h, pError)
            pError = trackMarker(currentID, myDrone, 0, 0, 0, w, h, pError)

        # if drone land and we finished
        if not myDrone.is_flying:
            f.write("Landing\n")
            print(myDrone.get_battery())
            break

        if loop_counter == 100:
            f.write("Drone info:\nBattery: " + str(myDrone.get_battery()) + " Height: " + str(myDrone.get_height()) + " X Speed: " +
                    str(myDrone.get_speed_x()) + " Y Speed: " + str(myDrone.get_speed_y()) +
                    " Z Speed: " + str(myDrone.get_speed_z()) + " Temperature: " + str(myDrone.get_temperature()) + " Barometer: " +
                    str(myDrone.get_barometer()) + "\n\n")
        else:
            loop_counter += 1

        cv2.imshow('Image', img)
        # out.write(img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            myDrone.land()
            f.write("Landing\n")
            print(myDrone.get_battery())
            # out.release()
            break
