import numpy as np
import sys
import time
import serial
import cv2
import requests
import urllib
import face_recognition
import os

# ESP32-CAM IP address
esp32cam_url = 'http://192.168.1.101/640x480.jpg'
arduino = serial.Serial('/dev/cu.usbmodem1101', 9600)
time.sleep(2)  # Wait for initialization
print("Initialized")

# Function to fetch images from ESP32-CAM
def get_esp32cam_image():
    try:
        response = requests.get(esp32cam_url, timeout=10)
        if response.status_code == 200:
            img_array = np.array(bytearray(response.content), dtype=np.uint8)
            img = cv2.imdecode(img_array, -1)
            return img
    except Exception as e:
        print(f"Error fetching image from ESP32-CAM: {str(e)}")
    return None

# Path to the directory containing Muskan's images
path = '/Users/muskanshomef/Desktop/Face Recognition Car/ImagesBasic'
images = []
classNames = []
mylist = os.listdir(path)
print(mylist)
for cl in mylist:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

# Function to compute face encodings
def find_encodings(images):
    encodeList = []
    i = 0
    for img in images:
        # Check if the image is empty
        if img is None:
            print(f"Failed to read image {i + 1}/{len(images)}")
            continue
        
        # Convert the image to RGB format
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Find face encodings in the image
        face_encodings = face_recognition.face_encodings(img)
        
        # Check if any face encodings are found
        if len(face_encodings) > 0:
            encode = face_encodings[0]  # Take the first face encoding
            encodeList.append(encode)
        else:
            print(f"No face found in image {i + 1}/{len(images)}")
        
        # Print progress
        print(f'Encoding {i + 1}/{len(images)} done!')
        i += 1
    return encodeList

encodelistknown = find_encodings(images)
print('Encoding Complete!')

# Directions dictionary
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

# Function to send direction to Arduino via serial port
def send_direction(direction):
    print("Direction:", directions[direction])
    arduino.write(bytes([direction]))

# Function to compute direction based on the detected face
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

# Function to detect and display Muskan's face from ESP32-CAM
def detect_and_display_esp32cam(frame):
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

        # Check if the detected face matches Muskan's face
        muskan_encodings = face_recognition.face_encodings(frame, [(rect[1], rect[0], rect[1] + rect[3], rect[0] + rect[2])])
        if len(muskan_encodings) > 0:
            match = face_recognition.compare_faces(encodelistknown, muskan_encodings[0])
            if match[0]:  # Muskan's face is detected
                direction = compute_direction(rect)
                send_direction(direction)

                # Draw rectangle and display the face
                cv2.rectangle(frame, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 2)
                cv2.putText(frame, "Muskan", (rect[0] + 6, rect[1] - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        cv2.imshow('ESP32-CAM', frame)

# Fetch images from ESP32-CAM
while True:
    # Capture an image from ESP32-CAM
    img = get_esp32cam_image()

    if img is not None:
        detect_and_display_esp32cam(img)
        
        if cv2.waitKey(1) == 27:  # ESC key
            break

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
