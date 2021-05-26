import cv2
import mediapipe as mp
import math


class HandDetector():
    def __init__(self, mode=False, max_hands=2, detection_conf=0.5, track_conf=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_conf = detection_conf
        self.track_conf = track_conf

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.max_hands,
                                        self.detection_conf, self.track_conf)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, hand_no=0, draw=True):
        x_list = []
        y_list = []
        b_box = []

        self.lm_list = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_no]

            for id, lm in enumerate(my_hand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                x_list.append(cx)
                y_list.append(cy)
                # print(id, cx, cy)
                self.lm_list.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 230), 2, cv2.FILLED)

            xmin, xmax = min(x_list), max(x_list)
            ymin, ymax = min(y_list), max(y_list)
            b_box = xmin, ymin, xmax, ymax

            if draw:
                cv2.rectangle(img, (b_box[0] - 15, b_box[1] - 15),
                              (b_box[2] + 15, b_box[3] + 15), (255, 255, 0), 2)

        return self.lm_list, b_box

    def fingersUp(self):
        fingers = []
        # Thumb
        if self.lm_list[self.tipIds[0]][1] > self.lm_list[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # 4 Fingers
        for id in range(1, 5):
            if self.lm_list[self.tipIds[id]][2] < self.lm_list[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

    def findDistance(self, pt1, pt2, img, draw=True):
        x1, y1 = self.lm_list[pt1][1], self.lm_list[pt1][2]
        x2, y2 = self.lm_list[pt2][1], self.lm_list[pt2][2]
        cx, cy = (x1 + x2)//2, (y1 + y2)//2

        if draw:
            cv2.circle(img, (x1, y1), 10, (255, 165, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 165, 0), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 240), 2)
            cv2.circle(img, (cx, cy), 5, (0, 0, 0), cv2.FILLED)

        len_line = math.hypot(x2 - x1, y2 - y1)
        return len_line, img, [x1, y1, x2, y2, cx, cy]
