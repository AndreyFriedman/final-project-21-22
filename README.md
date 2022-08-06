# project-20-21

About Tello EDU: https://www.ryzerobotics.com/tello-edu

Goals: 
Our goal was to code an autonomous drone that can interact with a human or a QR code.

Introduction:
Autonomous drones is an up coming subject in our world and has been an important evolving topic. They have multiple uses, such as: delivery purpose, collect information, and even for photography.
In our project we implemented the drones code which gave them the ability to operate as a drone swarms, follow a target and even change targets mid-flight in real time.
We used cv2 and djitellopy libraries in order to interact with the drone open source. In this way we get full access to the drone camera and engines and to the overall drone commands. In addition, we use in the pocket sender application in order to interact with 2 (or more) drones simultaneously
 
Methods:
The main idea of our project was to code the drone to follow a target  (initially it was a face recognition and then aruco code).First, we turn on the drone camera and get each frame mid-flight in live. Then we send the frame to the cv2 aruco code detection and get the aruco code coordinates (if there are any).  When we get the coordinates, we save them and mark the aruco code on the frame. All of this is shown in the user screen (the drone live video with the aruco code marked).
We use the given coordinates to assume where the target is respectively to the drone in the real world. By that we update the drone yaw, pitch and roll velocities to follow the target using our own dynamic speed functions. In the end of the flight a log file is created with data and information about the drone during the flight.
We used the Pocket Sender application to connect the wanted drones with our own router. Then we can communicate with each drone separately using his IP address which give us the ability to active and use several drones simultaneously.
 
Our Classes:
 TelloFaceTracking:
 This class initialize the drone, starting it, getting the frame from the drones camera and going to "utils" class and tells it to folow after the face recognized in the frame
 utills:
 This class tells the drone how to follow after a face it recognize
 MarkerTrackingTello:
 This class initialize the drone, starting it, getting the frame from the drones camera and going to "utils" class and tells it to folow after the aruco-code recognized in the frame
 utills2:
 This class tells the drone how to follow after the aruco-code it recognize
 padLand:
 This class tells the drone to find a pad land and land on it
 swarm-box-mission:
 This class takes the ip of 2 tello drones connected to the same wifi and send thems commands
 
