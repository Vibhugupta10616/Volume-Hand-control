import cv2
import numpy as np
import time
import HandTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

###############################
wCam, hCam = 640, 480
pTime = 0
min_dist = 25
max_dist = 190
vol = 0
vol_bar = 340
vol_perc = 0
area = 0
vol_color = (250, 0, 0)
################################


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.HandDetector(detection_conf=0.75, max_hands=1)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Volume Range -65 - 0
vol_range = volume.GetVolumeRange()
min_vol = vol_range[0]
max_vol = vol_range[1]


while True:
    success, img = cap.read()

    # Find Hand
    img = detector.findHands(img, draw=True)
    lmList, b_box = detector.findPosition(img, draw=True)
    if len(lmList) != 0:

        # Filter based on Size
        area = (b_box[2] - b_box[0]) * (b_box[3] - b_box[1]) // 100
        # print(area)
        if 200 < area < 1000:

            # Find Dist btw index & thumb
            ## Fings Distance Range 25 - 205
            len_line, img, line_info = detector.findDistance(4, 8, img)

            # Convert Vol
            vol_bar = np.interp(len_line, [min_dist, max_dist], [340, 140])
            vol_perc = np.interp(len_line, [min_dist, max_dist], [0, 100])

            # Reduce Resolution to make it smoother
            smoothness = 10
            vol_perc = smoothness * round(vol_perc / smoothness)

            # Check fingers up
            fingers = detector.fingersUp()
            # print(fingers)

            # If pinky is down set volume
            if not fingers[4]:
                volume.SetMasterVolumeLevelScalar(vol_perc / 100, None)
                cv2.circle(img, (line_info[4], line_info[5]), 5, (255, 255, 0), cv2.FILLED)
                vol_color = (135, 0, 255)
            else:
                vol_color = (135, 0, 255)

            # Min - Max Vol Button Color
            if len_line < min_dist:
                cv2.circle(img, (line_info[4], line_info[5]), 5, (0, 0, 255), cv2.FILLED)
            elif len_line > max_dist:
                cv2.circle(img, (line_info[4], line_info[5]), 5, (0, 255, 0), cv2.FILLED)

    # Drawings
    cv2.rectangle(img, (55, 140), (85, 340), (255, 255, 0), 3)
    cv2.rectangle(img, (55, int(vol_bar)), (85, 340), (255, 255, 0), cv2.FILLED)
    cv2.putText(img, f'Vol = {int(vol_perc)} %', (18, 380), cv2.FONT_HERSHEY_COMPLEX, 0.6, (51, 255, 255), 2)
    curr_vol = int(volume.GetMasterVolumeLevelScalar() * 100)
    cv2.putText(img, f'Vol set to: {int(curr_vol)} %', (410, 50), cv2.FONT_HERSHEY_COMPLEX, 0.7, vol_color, 2)


    # Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS:{int(fps)}', (30, 50), cv2.FONT_HERSHEY_COMPLEX,  0.7, (255, 0, 0), 2)

    cv2.imshow("Frame", img)
    cv2.waitKey(1)

