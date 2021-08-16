# Hand-Volume-Control
In this project I have built an OpenCV application in which a user can control his system's (laptop/pc) volume by making
some Hand Gestures.<br>

### Introduction :
This project is a use case of Hand Tracking technology. <br>
As soon as the user shows up his hand in the camera the application detects it & draws a bounding box around the hand.
Then according to the distance between user's Index finger and Thumb it displays the volume in the volume bar on the screen, to set
this volume as the system's volume user has to bend his pinky finger simultaneously.

### Demo :
<img src="Demo.gif" alt="this slowpoke moves"  width="780" height = "480">

### Main Libs Used :
- OpenCV lib(for image processing and drawing)
- Mediapipe lib(for Hand Tracking)
- Pycaw lib(to link up with the system's volume)




