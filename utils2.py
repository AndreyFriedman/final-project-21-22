import argparse
import math
import imutils
import time
import cv2
import sys
from djitellopy import Tello
import numpy as np
w, h = 360, 240
pid = [0.4, 0.4, 0]
pid2 = [0.3, 0.2]
left = 0
right = 0
up = 0
down = 0
pError = 0
fbRange = [1180, 1230]  # about [60, 130] cm
# fbRange2 = [4000, 6500]  # about [60, 130] cm
down_up_dist = [4, 8]
left_right_curved = [2, 4]


priorityID = 23
# priorityType = "DICT_6X6_100"
PIDflag = False


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
    img = cv2.resize(myFrame, (w, h))
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


def findMarker(img, givenId: int, type: str):  # id example: "DICT_ARUCO_ORIGINAL"
    ap = argparse.ArgumentParser()

    ap.add_argument("-i", "--image", required=False, help="path to input image containing ArUCo tag")
    ap.add_argument("-t", "--type", type=str, default=type, help="type of ArUCo tag to detect")
    args = vars(ap.parse_args())
    # verify that the supplied ArUCo tag exists and is supported by
    # OpenCV
    if ARUCO_DICT.get(args["type"], None) is None:
        # print("[INFO] ArUCo tag of '{}' is not supported".format(
        #     args["type"]))
        sys.exit(0)
    # load the ArUCo dictionary and grab the ArUCo parameters
    # print("[INFO] detecting '{}' tags...".format(args["type"]))
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
        global PIDflag
        if priorityID in ids:
            PIDflag = True
        else:
            # global PIDflag
            PIDflag = False

        print(ids)

        for (markerCorner, markerID) in zip(corners, ids):
            # extract the marker corners (which are always returned
            # in top-left, top-right, bottom-right, and bottom-left
            # order)
            if markerID == priorityID:
                print("yay!")
                corners = markerCorner.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners
                # convert each of the (x, y)-coordinate pairs to integers
                topRight = (int(topRight[0]), int(topRight[1]))
                bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                topLeft = (int(topLeft[0]), int(topLeft[1]))
                # AREA
                # print("-------")
                area = int(abs(math.dist(topRight, topLeft)) * abs(math.dist(topLeft, bottomLeft)))
                # print(area)
                global right
                right = int(abs(math.dist(topRight, bottomRight)))
                global left
                left = int(abs(math.dist(topLeft, bottomLeft)))
                global up
                up = int(abs(math.dist(topLeft, topRight)))
                global down
                down = int(abs(math.dist(bottomLeft, bottomRight)))
                # draw the bounding box of the ArUCo detection
                cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
                cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
                cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
                cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)
                # compute and draw the center (x, y)-coordinates of the ArUco marker
                cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                cY = int((topLeft[1] + bottomRight[1]) / 2.0)
                cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)
                # PRINT DOTS POS
                cv2.circle(frame, (topLeft[0], topLeft[1]), 4, (255, 255, 255), -1)
                cv2.putText(frame, "TL",
                            (topLeft[0] - 15, topLeft[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.circle(frame, (topRight[0], topRight[1]), 4, (255, 255, 255), -1)
                cv2.putText(frame, "TR",
                            (topRight[0] + 15, topRight[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.circle(frame, (bottomRight[0], bottomRight[1]), 4, (255, 255, 255), -1)
                cv2.putText(frame, "BR",
                            (bottomRight[0], bottomRight[1] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                # saving markers info in center and cordi
                cordinates.append([topLeft, topRight, bottomRight, bottomLeft])
                centers.append([cX, cY])
                areas.append(area)
                # draw the ArUco marker ID on the frame
                cv2.putText(frame, str(markerID),
                            (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                break
            elif markerID == givenId and PIDflag == False:
                corners = markerCorner.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners
                # convert each of the (x, y)-coordinate pairs to integers
                topRight = (int(topRight[0]), int(topRight[1]))
                bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                topLeft = (int(topLeft[0]), int(topLeft[1]))
                # AREA
                # print("-------")
                area = int(abs(math.dist(topRight, topLeft)) * abs(math.dist(topLeft, bottomLeft)))
                # print(area)
                # global right
                right = int(abs(math.dist(topRight, bottomRight)))
                # global left
                left = int(abs(math.dist(topLeft, bottomLeft)))
                # global up
                up = int(abs(math.dist(topLeft, topRight)))
                # global down
                down = int(abs(math.dist(bottomLeft, bottomRight)))
                # draw the bounding box of the ArUCo detection
                cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
                cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
                cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
                cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)
                # compute and draw the center (x, y)-coordinates of the ArUco marker
                cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                cY = int((topLeft[1] + bottomRight[1]) / 2.0)
                cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)
                # PRINT DOTS POS
                cv2.circle(frame, (topLeft[0], topLeft[1]), 4, (255, 255, 255), -1)
                cv2.putText(frame, "TL",
                            (topLeft[0] - 15, topLeft[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.circle(frame, (topRight[0], topRight[1]), 4, (255, 255, 255), -1)
                cv2.putText(frame, "TR",
                            (topRight[0] + 15, topRight[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.circle(frame, (bottomRight[0], bottomRight[1]), 4, (255, 255, 255), -1)
                cv2.putText(frame, "BR",
                            (bottomRight[0], bottomRight[1] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                # saving markers info in center and cordi
                cordinates.append([topLeft, topRight, bottomRight, bottomLeft])
                centers.append([cX, cY])
                areas.append(area)
                # draw the ArUco marker ID on the frame
                cv2.putText(frame, str(markerID),
                            (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                break

    return frame, centers, cordinates, areas


def trackMarker(myDrone, x, y, area, w, h, pError):
    print("-----new loop-----")
    flag = True

    if PIDflag == False:
        flag = False

    # forward and backward
    print("area is:", area)
    if fbRange[0] < area < fbRange[1]:
        myDrone.for_back_velocity = 0
        # flag = change_flag_true()
    elif area > fbRange[1]:
        # dynamic_spd = -1 * int(math.pow((area - fbRange[1]) / (10000-fbRange[1]), 2))
        dynamic_spd = -1 * int((area - fbRange[1]) / 20)
        print("dynamic speed is:", dynamic_spd)
        if dynamic_spd < -50:
            dynamic_spd = -50
        if 0 > dynamic_spd < -25:
            dynamic_spd = -25
        myDrone.for_back_velocity = dynamic_spd
        flag = False
        print("need to go back")
    elif area < fbRange[0] and area != 0:
        dynamic_spd = int(math.pow((fbRange[0] - area)/(fbRange[0]/7.5), 2.5))
        if dynamic_spd > 100:
            dynamic_spd = 100
        elif dynamic_spd < 15:
            dynamic_spd = 15
        myDrone.for_back_velocity = int(0.6 * dynamic_spd)
        print("dynamic speed is:", dynamic_spd)
        flag = False
        print("need to go forword")
    else:
        myDrone.for_back_velocity = 0
        flag = False

    # up and down       TODO remove 0.7 *
    if y > h // 2 - 10 and y < h // 2 + 10:
        myDrone.up_down_velocity = 0
    elif y > h // 2 + 10:
        myDrone.up_down_velocity = int(0.7 * (-math.pow(((y - h // 2 + 10)//3), 1.3)))
        flag = False
        print("need to go down")
    elif y < h // 2 - 10 and y != 0:
        myDrone.up_down_velocity = int(0.7 * (math.pow((((h // 2-10-y)//3)), 1.3)))
        flag = False
        print("need to go up")
    else:
        myDrone.up_down_velocity = 0
        flag = False

    # better left right curved
    lfc = left-right
    if lfc > 4:
        myDrone.left_right_velocity = 40
        print("need to rotate")
        flag = False
    elif lfc < -4:
        myDrone.left_right_velocity = -40
        flag = False
        print("need to rotate")
    else:
        myDrone.left_right_velocity = lfc*-10
        if abs(lfc) > 1:
            flag = False
            print("need to rotate")


    error = x - w // 2
    speed = pid[0] * error + pid[1] * (error - pError)
    speed = int(np.clip(speed, -100, 100))
    # spin
    if x != 0:
        myDrone.yaw_velocity = speed
        # flag = False
        # print("flag changed in line 233")
    else:
        myDrone.yaw_velocity = 0
    if myDrone.send_rc_control:
        myDrone.send_rc_control(myDrone.left_right_velocity,
                                myDrone.for_back_velocity,
                                myDrone.up_down_velocity,
                                myDrone.yaw_velocity)

    print("check for landing")
    if flag == True:
        print("landing")
        # myDrone.move_forward(40)
        # time.sleep(2)
        # myDrone.move_right(10)
        # myDrone.move_down(10)
        # time.sleep(1.5)qqqqqqqqqqqqq
        myDrone.land()
    else:
        print("cant land")
    return error

    # # up down curved
    # print("down-up = ", (down - up))
    # if fbRange[0] < area < ((fbRange[1] - fbRange[0]) / 2) + fbRange[0]:
    #     downUpDist = down_up_dist[0]
    # else:
    #     downUpDist = down_up_dist[1]
    # if down - up > downUpDist:
    #     print("need to land")
    #     if flag is True:
    #         print("landing")
    #         myDrone.land()
    #     else:
    #         print("cant land")
    # return error
