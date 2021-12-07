from videoMarkersTracking import *
import cv2
import pandas as pd
import keyboard

w,h = 360, 240
pid = [0.6, 0.45, 0]
pid2 = [0.3,0.2]
pError = 0
pErrorfb = 0
pErrorh = 0
startCounter = 0  # for no Flight 1   - for flight 0

myDrone = initializeTello()
print(myDrone.get_battery())
data=[]
#try:

## Flight
if startCounter == 0:
    myDrone.takeoff()
    startCounter = 1
while True:

    ## Step 1
    img = telloGetFrame(myDrone, w, h)
    ## Step 2
    img, centers, cordinates, areas = findMarker(img)
    if len(centers)>0:
        pError,pErrorfb, pErrorh = trackMarker(myDrone, centers[0][0],centers[0][1],areas[0], w, h, pError,pErrorfb,pErrorh)
    else:
        pError,pErrorfb, pErrorh = trackMarker(myDrone, 0, 0, 0, w, h, pError,pErrorfb, pErrorh)
    #if len(centers)>0:
        #print(centers[0][0])
    # data.append([myDrone.get_battery(), myDrone.get_height(), myDrone.get_speed_x(), myDrone.get_speed_y(),
    #              myDrone.get_speed_z(), myDrone.get_temperature(), myDrone.get_barometer(), info[1]])

    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        myDrone().land()
        break

# except KeyboardInterrupt:
#     # df = pd.DataFrame(data, columns= ['battary', 'height', 'speed_x', 'speed_y', 'speed_z', 'avg_temperature', 'barometer', 'area'])
#     # df.to_csv('markers_flight_data.csv', index = False)
#     pass
