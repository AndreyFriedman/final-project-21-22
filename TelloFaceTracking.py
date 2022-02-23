from utlis import *
import cv2
import pandas as pd
import keyboard

fbRange = [5000,6000]
w,h = 360, 240
pid = [0.4, 0.4, 0]
pError = 0
startCounter = 0  # for no Flight 1   - for flight 0

myDrone = initializeTello()
data=[]
try:
    while True:

        ## Flight
        if startCounter == 0:
             myDrone.takeoff()
             #myDrone.move_up(20)
             startCounter = 1

        ## Step 1
        img = telloGetFrame(myDrone, w, h)
        ## Step 2
        img, info = findFace(img)
        # data.append([myDrone.get_battery(), myDrone.get_height(), myDrone.get_speed_x(), myDrone.get_speed_y(),
        #              myDrone.get_speed_z(), myDrone.get_temperature(), myDrone.get_barometer(), info[1]])
        # pError = trackFace(myDrone, info, w, h, pid, pError, fbRange)

        cv2.imshow('Image', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            myDrone().land()
            break

except KeyboardInterrupt:
#     df = pd.DataFrame(data, columns= ['battary', 'height', 'speed_x', 'speed_y', 'speed_z', 'avg_temperature', 'barometer', 'area'])
#     df.to_csv('flight_data.csv', index = False)
    pass
