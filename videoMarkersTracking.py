# import the necessary packages
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import sys
from djitellopy import Tello
import numpy as np

w,h = 360, 240
pid = [0.4, 0.4, 0]
pid2 = [0.3,0.2]

pError = 0
fbRange = [1000,1100]
areaF=1000

def initializeTello():
    myDrone = Tello()
    myDrone.connect()
    myDrone.for_back_velocity = 0
    myDrone.left_right_velocity = 0
    myDrone.up_down_velocity = 0
    myDrone.yaw_velocity = 0
    myDrone.speed = 0
    myDrone.streamoff()
    myDrone.streamon()
    return myDrone


def telloGetFrame(myDrone, w=360, h=240):
    myFrame = myDrone.get_frame_read()
    myFrame = myFrame.frame
    img = cv2.resize(myFrame,(w,h))
    return img

def findMarker(img):
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=False, help="path to input image containing ArUCo tag")
    ap.add_argument("-t", "--type", type=str, default="DICT_ARUCO_ORIGINAL", help="type of ArUCo tag to detect")
    #ap.add_argument("-t", "--type", type=str, help="type of ArUCo tag to detect")
    args = vars(ap.parse_args())

    # define names of each possible ArUco tag OpenCV supports
    ARUCO_DICT = {
        "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
        "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
        "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
        "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
        "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
        "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
        "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
        "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
        "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
        "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
        "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
        "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
        "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
        "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
        "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
        "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
        "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
        "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
        "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
        "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
        "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
    }

    # verify that the supplied ArUCo tag exists and is supported by
    # OpenCV
    if ARUCO_DICT.get(args["type"], None) is None:
        print("[INFO] ArUCo tag of '{}' is not supported".format(
            args["type"]))
        sys.exit(0)

    # load the ArUCo dictionary and grab the ArUCo parameters
    print("[INFO] detecting '{}' tags...".format(args["type"]))
    arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])
    arucoParams = cv2.aruco.DetectorParameters_create()

    # loop over the frames from the video stream
    frame = img #vs.read()
    frame = cv2.resize(frame,(w,h))#imutils.resize(frame, width=1000)

    # detect ArUco markers in the input frame
    (corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)

    centers=[]
    cordinates=[]
    areas=[]
    # verify *at least* one ArUco marker was detected
    if len(corners) > 0:

        # flatten the ArUco IDs list
        ids = ids.flatten()

        # loop over the detected ArUCo corners
        for (markerCorner, markerID) in zip(corners, ids):
            # extract the marker corners (which are always returned
            # in top-left, top-right, bottom-right, and bottom-left
            # order)
            corners = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners


            # convert each of the (x, y)-coordinate pairs to integers
            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))
            # area=(topRight[0]-topLeft[0])*(bottomRight[1]-topRight[1])
            area=10*(abs((topRight[0]-topLeft[0]))+abs((bottomRight[0]-bottomLeft[0]))+abs((bottomRight[1]-topRight[1]))+abs((bottomLeft[1]-topLeft[1])))
            # draw the bounding box of the ArUCo detection
            cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
            cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
            cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
            cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)

            # compute and draw the center (x, y)-coordinates of the ArUco marker
            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)
            cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)

            #saving markers info in center and cordi
            cordinates.append([topLeft, topRight, bottomRight, bottomLeft])
            centers.append([cX, cY])
            areas.append(area)
            # draw the ArUco marker ID on the frame
            cv2.putText(frame, str(markerID),
                        (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # show the output frame
        #cv2.imshow("Frame", frame)
        #key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        #if key == ord("q"):
            #break

    return frame, centers, cordinates, areas
    # do a bit of cleanup
    #cv2.destroyAllWindows()
    #vs.stop()




def trackMarker(myDrone, cX,cY, area, w, h , pError, pErrorfb, pErrorh):
    error=0
    errorfb=0
    errorh=0
    if cX != 0:
        error = cX-(w // 2)
        speed = pid[0] * error + pid[1] * (error - pError)
        speed = int(np.clip(speed, -100, 100))
        myDrone.yaw_velocity = speed

    else:
        myDrone.yaw_velocity = 0

    # up and down
    if cY != 0:
        if cY<((h // 2)+20):
            myDrone.up_down_velocity=15
        elif cY<((h // 2)-20):
            myDrone.up_down_velocity=-15
    else:
        myDrone.up_down_velocity = 0


    # if cY > h//2 - 10 and cY < h//2 + 10:
    #     myDrone.up_down_velocity = 0
    # elif cY > h//2 + 10:
    #     myDrone.up_down_velocity = -20
    # elif cY < h//2 - 10 and cY != 0:
    #     myDrone.up_down_velocity = 20
    # else:
    #     myDrone.up_down_velocity = 0

    # forward and backward
    if area!=0:
        errorfb = areaF - area
        speedfb = pid2[0] * errorfb + pid2[1] * (errorfb - pErrorfb)
        speedfb = int(np.clip(speedfb, -10, 10))
        myDrone.for_back_velocity = speedfb
    else:
        myDrone.for_back_velocity = 0

    # if area > fbRange[0] and area < fbRange[1]:
    #     print("stop")
    #     myDrone.for_back_velocity = 0
    # elif area > fbRange[1]:
    #     print("back")
    #     myDrone.for_back_velocity = -10
    # elif area < fbRange[0] and area != 0:
    #     print("forward")
    #     myDrone.for_back_velocity = 10
    # else:
    #     myDrone.for_back_velocity = 0

    print(area)


    if myDrone.send_rc_control:
         myDrone.send_rc_control(myDrone.left_right_velocity,
                                 myDrone.for_back_velocity,
                                 myDrone.up_down_velocity,
                                 myDrone.yaw_velocity)
    return error, errorfb, errorh
