import torch
import cv2 as cv
import numpy as np
import mediapipe as mp
import csv
import copy
import time
from collections import Counter
from collections import deque
import torch
import torch.nn as nn
import time
import os
import pandas as pd
import sys
from os import path
from gesture.skills import *
#import win32api, win32con
import pyautogui
import threading

# gotta back that shit up for imports to work
sys.path.append("..")

from gesture.model.gesture.gestureModel import NeuralNetG
# from model.motion.motionModel import NeuralNetM



pyautogui.PAUSE = 0.01
# print(os.getcwd())

# def mouseDown():
#     print("mouse down")

#     if sys.platform == 'win32':
#         win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
#     else:
#         pyautogui.mouseDown()


# def mouseUp():
#     print("mouse up")

#     if sys.platform == 'win32':
#         win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
#     else:
#         pyautogui.mouseUp()


# def zoomOut():
#     print("zooming out")

# def zoomIn():
#     print("zooming in")
#     pyautogui.hotkey('ctrl', '=')


# def click():
#     print('click')

#     if sys.platform == 'win32':
#         print('click on windows')
#     else:
#         pyautogui.click()


class HandDetection():


    def getCamera(self):
        # Load Camera
        self.cap = cv.VideoCapture(self.cap_device)
        # self.cap = cv.VideoCapture(cap_device,cv.CAP_DSHOW)
        self.cap.set(cv.CAP_PROP_FPS,self.setFPS) 
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, self.cap_width)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, self.cap_height)
        print("got camera")

    def loadGestureSettings(self):
        self.df = pd.read_json(path.join(self.dir_name, 'csv/gestureSettings.json'), orient="records")

    def __init__(self):
        # Camera Params
        self.cap_device = 0
        self.cap_width = 1280
        self.cap_height = 720

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # Hand Model
        use_static_image_mode = False
        min_detection_confidence = 0.8
        min_tracking_confidence = 0.5

        # FPS Time counter
        self.pTime = 0
        self.cTime = 0
        self.setFPS = 30

        # Varaibles to keep track of points
        # self.point_history = deque(maxlen=4)
        self.point_counter = 0
        # self.motion_history = deque(maxlen=4)
        self.gesture_history = deque(maxlen=4)
        self.gesture_cords = []
        self.hand_exit = True
        self.old_gesture = None
        self.old_tracker = None
        self.last_function_time = 0
        self.shortdelay = 0.3 # in seconds
        self.longdelay = 1.5 # in seconds
        self.isChanging = False

        self.mapping = {
            "Left Click" : leftClick,
            "Right Click" : rightClick,
            "Zoom In" : zoomIn,
            "Zoom Out" : zoomOut,
            "Scroll Up" : scrollUp,
            "Scroll Down" : scrollDown,
            "Go Back" : goBack,
            "Go Forward" : goForward,
            "Switch App" : switchApp,
            "Switch Desktop" : switchDesktop,
            "Slide App Left" : slideAppLeft,
            "Slide App Right" : slideAppRight,
            "Maximize App" : maximizeApp,
            "Minimize App" : minimizeApp,
            "Play" : play,
            "Pause" : pause,
            "Next Track" : nextTrack,
            "Previous Track" : prevTrack,
            "Increase Volume" : increaseVolume,
            "Decrease Volume" : decreaseVolume,
            "Unmute" : unmute,
            "Mute" : mute
        }
        t1 = threading.Thread(target=self.getCamera)
        t1.start()

        # Define CSV paths
        self.dir_name = path.dirname(__file__)

        gesture_label_csv_path = path.join(self.dir_name, 'csv/gesture_label.csv')
        self.gesture_csv_path = path.join(self.dir_name, 'csv/gesture.csv')

        self.loadGestureSettings()
        # print(self.df)
        # motion_label_csv_path = 'csv/motion_label.csv'
        # self.motion_csv_path = 'csv/motion.csv'

        # Read in csv
        with open(gesture_label_csv_path) as f:
            reader = csv.reader(f)
            self.gesture_labels = [row[0] for row in reader]
        
        self.num_classes = len(self.gesture_labels)

        # with open(motion_label_csv_path) as f:
        #     reader = csv.reader(f)
        #     self.motion_labels = [row[0] for row in reader]

        # self.num_classes2 = len(self.motion_labels)

        print("read csv")
        self.current_gesture_to_record = 0
        # self.current_motion_to_record = 0

        # Load Hand Model
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=use_static_image_mode,
            max_num_hands=1,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )
        self.mpDraw = mp.solutions.drawing_utils
        print("loaded hand model")

        # Define Model Paths
        GESTURE_PATH = path.join(self.dir_name, 'model/gesture/GestureModel.pth')

        # MOTION_PATH = "model/motion/MotionModel.pth"

        # Load Gesture Model
        self.model = NeuralNetG(self.num_classes)
        self.model.load_state_dict(torch.load(GESTURE_PATH, map_location=self.device))
        self.model.eval()
        print("loaded gesture model")

        # Load Motion Detector
        # self.model2 = NeuralNetM(self.num_classes2)
        # self.model2.load_state_dict(torch.load(MOTION_PATH))
        # self.model2.eval()
        # print("loaded motion model")
        t1.join()


    def loop(self):
        while True:
            # Get Camera input
            success, image = self.cap.read()
            if not success:
                break

            # Flip Camera on the y-axis
            image = cv.flip(image, 1)

            # Create a copy
            debug_image = copy.deepcopy(image)

            # Detection implementation
            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            results = self.hands.process(image)

            # Draw Landmarks
            gesture_cords = []
            if results.multi_hand_landmarks is not None:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks,results.multi_handedness):
                    left_or_right = handedness.classification[0].index
                    self.mpDraw.draw_landmarks(debug_image, hand_landmarks, self.mpHands.HAND_CONNECTIONS)
                    for index, lm in enumerate(hand_landmarks.landmark):
                        gesture_cords.append([lm.x,lm.y,lm.z])

            # Relative Coorindates and nomalize data
            if (len(gesture_cords) > 0):
                if (self.hand_exit == True):
                    self.hand_exit = False
                    self.prev_point = np.array(gesture_cords[9])
                    current_predict_motion = ""
                    self.point_counter = 6

                # Add to coordinate history
                self.point_counter += 1
                if (self.point_counter == 7):
                    self.point_counter = 0
                    # self.point_history.append(np.array(gesture_cords).flatten())
                    # distance = (self.prev_point - np.average(gesture_cords,axis=0)) * 100
                    distance = (self.prev_point - np.array(gesture_cords[9])) * 100
                    # self.prev_point = np.average(gesture_cords,axis=0)
                    self.prev_point = gesture_cords[9]

                    if (np.abs(distance[0]) > 12):
                        if (distance[0] > 0):
                            current_predict_motion = "left"
                        else:
                            current_predict_motion = "right"
                    elif (np.abs(distance[1]) > 12):
                        if (distance[1] > 0):
                            current_predict_motion = "up"
                        else:
                            current_predict_motion = "down"
                    else:
                        current_predict_motion = "no motion"

                # Relative
                normalized_points = np.array(gesture_cords) - gesture_cords[9]
                
                # Flatten
                normalized_points = normalized_points.flatten()
                # fully_flat = np.array(self.point_history).flatten()

                # Normalize
                max_value = np.max(normalized_points)
                normalized_points = normalized_points / max_value
                
                output = self.model.forward(torch.from_numpy(np.append([left_or_right], normalized_points)).float())
                self.gesture_history.append(torch.argmax(output))
                new_prediction = Counter(self.gesture_history).most_common()[0][0]

                if (self.old_gesture != new_prediction): # detecting change in gesture

                    # wait a short delay before recording new gesture
                    if (self.isChanging == False):
                        self.isChanging = True
                        self.old_tracker = self.old_gesture
                        self.short_delay_time = time.time()
                    elif (self.isChanging == True and ((self.short_delay_time + self.shortdelay) < time.time())):
                        # execute function after long delay
                        if ( (self.last_function_time + self.longdelay) < time.time()):
                            # print(self.gesture_labels[self.old_gesture],self.gesture_labels[new_prediction])
                            record = self.df.loc[(self.df["starting position"] == self.gesture_labels[self.old_tracker]) & ((self.df["ending position"] == self.gesture_labels[new_prediction]) | (self.df["ending position"] == "any"))]
                            if (len(record) > 0):
                                print(record.iloc[0]["name"],record.iloc[0]["pre-defined function name"])
                                # print(type(record.iloc[0]["pre-defined function name"]))
                                t1 = threading.Thread(target=self.mapping[record.iloc[0]["pre-defined function name"]])
                                t1.start()
                                # print(threading.active_count())
                                # self.mapping[record.iloc[0]["pre-defined function name"]]()
                            # function_to_be_executed = self.df.loc[(self.df["starting position"] == self.gesture_labels[self.old_gesture]) & ((self.df["ending position"] == self.gesture_labels[new_prediction]) | (self.df["ending position"] == "any"))]["name"]
                            # print(function_to_be_executed)
                            # if (len(function_to_be_executed) > 0):
                            #     function_to_be_executed = function_to_be_executed.iloc[0]
                            #     print(function_to_be_executed)
                                # if function_to_be_executed in self.mapping.keys():
                                    # self.mapping[function_to_be_executed]()
                        self.isChanging = False
                        self.old_tracker = self.old_gesture
                        self.old_gesture = new_prediction
                        if self.old_tracker == None:
                            self.old_tracker = new_prediction
                        self.last_function_time = time.time()

                elif ((current_predict_motion != "no motion") and (current_predict_motion != "no hand detected")): # detecting change in motion
                    if ( (self.last_function_time + self.longdelay) < time.time() ):
                        self.last_function_time = time.time()
                        record = self.df.loc[(self.df["ending position"] == self.gesture_labels[new_prediction]) & (self.df["motion"] == current_predict_motion)]
                        # print(gesture_name)
                        if (len(record) > 0):
                            print(record.iloc[0]["name"],record.iloc[0]["pre-defined function name"])
                            t1 = threading.Thread(target=self.mapping[record.iloc[0]["pre-defined function name"]])
                            t1.start()
                            # print(threading.active_count())
                        # print(current_predict_motion, self.gesture_labels[new_prediction])

                current_predict_gesture = self.gesture_labels[new_prediction]


                # if (len(self.point_history) == 4):
                #     output2 = self.model2.forward(torch.from_numpy(np.append([left_or_right], fully_flat)).float())
                #     self.motion_history.append(torch.argmax(output2))
                #     current_predict_motion = self.motion_labels[Counter(self.motion_history).most_common()[0][0]]
            else:
                current_predict_gesture = "no hand detected"
                current_predict_motion = "no hand detected"
                self.old_gesture = None
                self.old_tracker = None
                self.hand_exit = True
                self.last_function_time = time.time()

            # Move Mouse
            # if (len(gesture_cords) > 0):
            #     mouse_pos = (max(0,min(1920,int(gesture_cords[8][0]*1920*1.2))),max(0,min(1080,int(gesture_cords[8][1]*1080*1.4))))
            #     # if sys.platform == 'win32':
            #     #     win32api.SetCursorPos(mouse_pos)
            #     # else:
            #     pyautogui.moveTo(mouse_pos)

            # Calculate FPS
            self.cTime = time.time()
            fps = 1 / (self.cTime - self.pTime)
            self.pTime = self.cTime

            # Press esc to exit
            key = cv.waitKey(10)

            if key != -1:
                # decrease current gesture to record counter
                if (key == 49): # 1 key
                    self.current_gesture_to_record = self.current_gesture_to_record - 1
                    if (self.current_gesture_to_record < 0):
                        self.current_gesture_to_record = len(self.gesture_labels) - 1

                # increase current gesture to record counter
                if (key == 50): # 2 key
                    self.current_gesture_to_record = self.current_gesture_to_record + 1
                    if (self.current_gesture_to_record >= len(self.gesture_labels)):
                        self.current_gesture_to_record = 0

                # record current gesture to csv
                if (key == 51): # 3 key
                    with open(self.gesture_csv_path, 'a', newline="") as f:
                        writer = csv.writer(f)
                        writer.writerow(np.append([self.current_gesture_to_record,left_or_right], normalized_points))

                # # decrease current motion to record counter
                # if (key == 52): # 4 key
                #     self.current_motion_to_record = self.current_motion_to_record - 1
                #     if (self.current_motion_to_record < 0):
                #         self.current_motion_to_record = len(self.motion_labels) - 1

                # # increase current motion to record counter
                # if (key == 53): # 5 key
                #     self.current_motion_to_record = self.current_motion_to_record + 1
                #     if (self.current_motion_to_record >= len(self.motion_labels)):
                #         self.current_motion_to_record = 0

                # # record current motion to csv
                # if (key == 54): # 6 key
                #     with open(self.motion_csv_path, 'a', newline="") as f:
                #         writer = csv.writer(f)
                #         writer.writerow(np.append([self.current_motion_to_record,left_or_right], np.array(self.point_history).flatten()))

                

            if key == 27:  # ESC key
                break

            # Display Image
            cv.putText(debug_image, "fps: " + str(int(fps)), (10, 700), cv.FONT_HERSHEY_PLAIN, 1.5, (182, 236, 249), 2) # bot left

            cv.putText(debug_image, "Predicted Gesture: " + current_predict_gesture, (10, 30), cv.FONT_HERSHEY_PLAIN, 1.5, (182, 236, 249), 2) # top left
            cv.putText(debug_image, "Record Gesture: " + self.gesture_labels[self.current_gesture_to_record], (10, 90), cv.FONT_HERSHEY_PLAIN, 1.5, (182, 236, 249), 2) # top left

            if (self.old_gesture == None):
                old_gesture_print = "none"
            else:
                old_gesture_print = self.gesture_labels[self.old_tracker]
            cv.putText(debug_image, "Old Gesture: " + old_gesture_print, (10, 60), cv.FONT_HERSHEY_PLAIN, 1.5, (182, 236, 249), 2) # top left

            cv.putText(debug_image, "Predicted Motion: " + current_predict_motion, (10, 120), cv.FONT_HERSHEY_PLAIN, 1.5, (182, 236, 249), 2) # top left
            # cv.putText(debug_image, "Record Motion: " + self.motion_labels[self.current_motion_to_record], (10, 120), cv.FONT_HERSHEY_PLAIN, 1.5, (182, 236, 249), 2) # top left


            cv.imshow('Hand Gesture Recognition', debug_image)
        self.cap.release()
        cv.destroyAllWindows()

def launch_gesture():
    gest = HandDetection() 
    gest.loop()