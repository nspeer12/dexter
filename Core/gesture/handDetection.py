import cv2 as cv
import numpy as np
import mediapipe as mp
import csv
import copy
import time
# import win32api, win32con
from collections import Counter
from collections import deque
import torch
import torch.nn as nn
from model.gesture.gestureModel import NeuralNetG
from model.motion.motionModel import NeuralNetM

def main():
    # Camera Params
    cap_device = 0
    cap_width = 1280
    cap_height = 720

    # Hand Model
    use_static_image_mode = False
    min_detection_confidence = 0.8
    min_tracking_confidence = 0.5

    # FPS Time counter
    pTime = 0
    cTime = 0
    setFPS = 30

    # Varaibles to keep track of points
    point_history = deque(maxlen=4)
    point_counter = 0
    gesture_history = deque(maxlen=8)
    gesture_cords = []

    # Define CSV paths
    gesture_label_csv_path = 'csv/gesture_label.csv'
    gesture_csv_path = 'csv/gesture.csv'

    motion_label_csv_path = 'csv/motion_label.csv'
    motion_csv_path = 'csv/motion.csv'

    # Read in csv
    with open(gesture_label_csv_path) as f:
        reader = csv.reader(f)
        gesture_labels = [row[0] for row in reader]
    
    num_classes = len(gesture_labels)

    with open(motion_label_csv_path) as f:
        reader = csv.reader(f)
        motion_labels = [row[0] for row in reader]

    num_classes2 = len(motion_labels)

    print("read csv")
    current_gesture_to_record = 0
    current_motion_to_record = 0

    # Load Camera
    cap = cv.VideoCapture(cap_device)
    # cap = cv.VideoCapture(cap_device,cv.CAP_DSHOW)
    cap.set(cv.CAP_PROP_FPS,setFPS) 
    cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)
    print("got camera")

    # Load Hand Model
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(
        static_image_mode=use_static_image_mode,
        max_num_hands=1,
        min_detection_confidence=min_detection_confidence,
        min_tracking_confidence=min_tracking_confidence,
    )
    mpDraw = mp.solutions.drawing_utils
    print("loaded hand model")

    # Define Model Paths
    GESTURE_PATH = "model/gesture/GestureModel.pth"
    MOTION_PATH = "model/motion/MotionModel.pth"

    # Load Gesture Model
    model = NeuralNetG(num_classes)
    model.load_state_dict(torch.load(GESTURE_PATH))
    model.eval()
    print("loaded gesture model")

    # Load Motion Detector
    model2 = NeuralNetM(num_classes2)
    model2.load_state_dict(torch.load(MOTION_PATH))
    model2.eval()
    print("loaded motion model")

    while True:
        # Get Camera input
        success, image = cap.read()
        if not success:
            break

        # Flip Camera on the y-axis
        image = cv.flip(image, 1)

        # Create a copy
        debug_image = copy.deepcopy(image)

        # Detection implementation
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        results = hands.process(image)

        # Draw Landmarks
        gesture_cords = []
        if results.multi_hand_landmarks is not None:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks,results.multi_handedness):
                left_or_right = handedness.classification[0].index
                mpDraw.draw_landmarks(debug_image, hand_landmarks, mpHands.HAND_CONNECTIONS)
                for index, lm in enumerate(hand_landmarks.landmark):
                    gesture_cords.append([lm.x,lm.y,lm.z])

        # Relative Coorindates and nomalize data
        if (len(gesture_cords) > 0):

            # Add to coordinate history
            point_counter += 1
            if (point_counter == 7):
                point_counter = 0
                point_history.append(np.array(gesture_cords).flatten())

            # Relative
            normalized_points = np.array(gesture_cords) - gesture_cords[9]
            
            # Flatten
            normalized_points = normalized_points.flatten()
            fully_flat = np.array(point_history).flatten()

            # Normalize
            max_value = np.max(normalized_points)
            normalized_points = normalized_points / max_value
            
            output = model.forward(torch.from_numpy(np.append([left_or_right], normalized_points)).float())
            gesture_history.append(torch.argmax(output))
            current_predict_gesture = gesture_labels[Counter(gesture_history).most_common()[0][0]]

            if (len(point_history) == 4):
                output2 = model2.forward(torch.from_numpy(np.append([left_or_right], fully_flat)).float())
                current_predict_motion = motion_labels[torch.argmax(output2)]
        else:
            point_history.clear()
            current_predict_gesture = "none"
            current_predict_motion = "none"



        # Move Mouse
        # if (len(gesture_cords) > 0):
            # win32api.SetCursorPos((max(0,min(1920,int(gesture_cords[8][0]*1920*1.2))),max(0,min(1080,int(gesture_cords[8][1]*1080*1.4)))))

        # Calculate FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        # Press esc to exit
        key = cv.waitKey(10)

        if key != -1:
            # decrease current gesture to record counter
            if (key == 49): # 1 key
                current_gesture_to_record = current_gesture_to_record - 1
                if (current_gesture_to_record < 0):
                    current_gesture_to_record = len(gesture_labels) - 1

            # increase current gesture to record counter
            if (key == 50): # 2 key
                current_gesture_to_record = current_gesture_to_record + 1
                if (current_gesture_to_record >= len(gesture_labels)):
                    current_gesture_to_record = 0

            # record current gesture to csv
            if (key == 51): # 3 key
                with open(gesture_csv_path, 'a', newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(np.append([current_gesture_to_record,left_or_right], normalized_points))

            # decrease current motion to record counter
            if (key == 52): # 4 key
                current_motion_to_record = current_motion_to_record - 1
                if (current_motion_to_record < 0):
                    current_motion_to_record = len(motion_labels) - 1

            # increase current motion to record counter
            if (key == 53): # 5 key
                current_motion_to_record = current_motion_to_record + 1
                if (current_motion_to_record >= len(motion_labels)):
                    current_motion_to_record = 0

            # record current motion to csv
            if (key == 54): # 6 key
                with open(motion_csv_path, 'a', newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(np.append([current_motion_to_record,left_or_right], np.array(point_history).flatten()))

            

        if key == 27:  # ESC key
            break

        # Display Image
        cv.putText(debug_image, "fps: " + str(int(fps)), (10, 700), cv.FONT_HERSHEY_PLAIN, 1.5, (182, 236, 249), 2) # bot left

        cv.putText(debug_image, "Predicted Gesture: " + current_predict_gesture, (10, 30), cv.FONT_HERSHEY_PLAIN, 1.5, (182, 236, 249), 2) # top left
        cv.putText(debug_image, "Record Gesture: " + gesture_labels[current_gesture_to_record], (10, 60), cv.FONT_HERSHEY_PLAIN, 1.5, (182, 236, 249), 2) # top left

        cv.putText(debug_image, "Predicted Motion: " + current_predict_motion, (10, 90), cv.FONT_HERSHEY_PLAIN, 1.5, (182, 236, 249), 2) # top left
        cv.putText(debug_image, "Record Motion: " + motion_labels[current_motion_to_record], (10, 120), cv.FONT_HERSHEY_PLAIN, 1.5, (182, 236, 249), 2) # top left

        cv.imshow('Hand Gesture Recognition', debug_image)

    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
