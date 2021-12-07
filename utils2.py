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

def findMarker(img,givenId:int,type:str):#id example: "DICT_ARUCO_ORIGINAL"
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=False, help="path to input image containing ArUCo tag")
    ap.add_argument("-t", "--type", type=str, default=type, help="type of ArUCo tag to detect")
    args = vars(ap.parse_args())
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
    frame = img
    frame = cv2.resize(frame, (w, h))
    # detect ArUco markers in the input frame
    (corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)

    centers = []
    cordinates = []
    areas = []

    if len(corners) > 0:

        # flatten the ArUco IDs list
        ids = ids.flatten()

        # loop over the detected ArUCo corners
        for (markerCorner, markerID) in zip(corners, ids):
            # extract the marker corners (which are always returned
            # in top-left, top-right, bottom-right, and bottom-left
            # order)
            if markerID == givenId:
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



#
#
#
# def trackMarker(cx,cy,area):
