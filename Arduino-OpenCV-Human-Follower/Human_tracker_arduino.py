import numpy as np
import sys
import time
import serial
import cv2

arduino = serial.Serial('COM6', 9600)
time.sleep(2)  # Wait for initialization
print("Initialized")

directions = {
    1: "Left Back",
    2: "Backward",
    3: "Backward Right",
    4: "Left",
    5: "Stay Still",
    6: "Right",
    7: "Forward Left",
    8: "Forward",
    9: "Forward Right"
}

def send_direction(direction):
    print("Direction:", directions[direction])
    arduino.write(bytes([direction]))

def compute_direction(bound, init_area=40000):
    center = (320, 240)
    curr = (bound[0] + bound[2] / 2, bound[1] + bound[3] / 2)
    out = 5  # Stay still by default

    if bound[2] * bound[3] > init_area + 5000 or bound[1] < 50:
        out = 2  # Move backward if object is approaching or too close
    elif bound[2] * bound[3] < init_area - 5000 or (bound[1] + bound[3]) > 430:
        out = 8  # Move forward if object is moving away or too far
    elif curr[0] > center[0] + 100:
        out = 6  # Move right if object is to the right of the center
    elif curr[0] < center[0] - 100:
        out = 4  # Move left if object is to the left of the center
    elif curr[1] < center[1] - 50:
        out = 7  # Move forward-left if object is above the center
    elif curr[1] > center[1] + 50:
        out = 9  # Move forward-right if object is below the center

    return out



def detect_and_display(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30), maxSize=(500, 500))

    if len(faces) > 0:
        max_area = -1
        max_area_idx = 0
        for i, (x, y, w, h) in enumerate(faces):
            if w * h > max_area:
                max_area = w * h
                max_area_idx = i

        rect = faces[max_area_idx]
        cv2.rectangle(frame, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 2)
        cv2.putText(frame, f'x: {rect[0] + rect[2] / 2} y: {rect[1] + rect[3] / 2} size: {rect[2] * rect[3]}',
                    (rect[0], rect[1] + rect[3]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))

        direction = compute_direction(rect)
        send_direction(direction)
    else:
        print('Search...')
        send_direction(5)  # No face detected, stay still

    cv2.imshow('frame', frame)

cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

try:
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        raise IOError("Failed to open camera")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to retrieve frame")
            break

        detect_and_display(frame)

        if cv2.waitKey(1) == 27:  # ESC key
            break

except Exception as e:
    print("Error:", e)

finally:
    cap.release()
    cv2.destroyAllWindows()
    arduino.close()
