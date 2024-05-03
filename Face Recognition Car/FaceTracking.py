import cv2
import serial
import time
import requests
import numpy as np

# Variables
x, y, h, w = 0, 0, 0, 0
DISTANCE = 0

# Known distance and width
Known_distance = 31.5  # Inches
Known_width = 5.7  # Inches

# Colors in BGR format
GREEN = (0, 255, 0)
RED = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (0, 255, 255)
PURPLE = (255, 0, 255)
WHITE = (255, 255, 255)

# Font styles
fonts = cv2.FONT_HERSHEY_COMPLEX
fonts2 = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
fonts3 = cv2.FONT_HERSHEY_COMPLEX_SMALL
fonts4 = cv2.FONT_HERSHEY_TRIPLEX

# Face detector object
face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Focal length finder function
def FocalLength(measured_distance, real_width, width_in_rf_image):
    focal_length = (width_in_rf_image * measured_distance) / real_width
    return focal_length

# Distance estimation function
def Distance_finder(Focal_Length, real_face_width, face_width_in_frame):
    distance = (real_face_width * Focal_Length) / face_width_in_frame
    return distance

# Face detection function

def face_data(image, CallOut, Distance_level):
    face_width = 0
    face_x, face_y = 0, 0
    face_center_x = 0
    face_center_y = 0
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    scaleFactor = 1.3
    minNeighbors = 5
    minSize = (30, 30)
    faces = face_detector.detectMultiScale(gray_image, scaleFactor=1.301, minNeighbors=5, minSize=(10, 10))
    
    # Check if Distance_level is None, and set a default value if so
    if Distance_level is None:
        Distance_level = float('inf')  # Set to infinity
    
    for (x, y, h, w) in faces:
        face_width = w
        face_center_x = int(w/2) + x
        face_center_y = int(h/2) + y
    

        # if CallOut:
            # Draw bounding box and distance indicator
            # cv2.rectangle(image, (x, y), (x+w, y+h), GREEN, 2)
            # cv2.line(image, (x, y-11), (x+210, y-11), YELLOW, 25)
            # # cv2.line(image, (x, y-11), (x+Distance_level, y-11), GREEN, 25)
            # cv2.line(image, (x, y-11), (x+(Distance_level), y-11), GREEN, 25)
            # pass
    return face_width, faces, face_center_x, face_center_y


# Function to fetch image from ESP32-CAM
def fetch_image(url):
    try:
        response = requests.get(url)
        img_array = np.array(bytearray(response.content), dtype=np.uint8)
        img = cv2.imdecode(img_array, -1)
        return img
    except Exception as e:
        print("Error fetching image:", e)
        return None

# Main function
def main():
    # URL of the ESP32-CAM serving the image
    esp32_cam_url = "http://10.100.156.148/640x480.jpg"
    ref_image = cv2.imread(r"/Users/pulkitbatra/Desktop/FaceRecognitionCar/ImagesBasic/Muskan.png")
    DISTANCE = None

    # Find the focal length
    ref_image_face_width, _, _, _ = face_data(ref_image, False, DISTANCE)
    Focal_length_found = FocalLength(Known_distance, Known_width, ref_image_face_width)

    # Connect to the Arduino
    # Arduino = serial.Serial(baudrate=9600, port='cu.usbmodem1401')
    Arduino = serial.Serial('/dev/cu.usbmodem101', 9600)
    Direction = 0
    Motor1_Speed = 0
    Motor2_Speed = 0
    Truing_Speed = 110
    net_Speed = 180

    while True:
        # Fetch image from ESP32-CAM
        frame = fetch_image(esp32_cam_url)
        frame_height, frame_width = 640,480
        RightBound = 200
        Left_Bound = 200

        # Detect face and estimate distance
        face_width_in_frame, Faces, FC_X, FC_Y = face_data(frame, True, DISTANCE)
        for (face_x, face_y, face_w, face_h) in Faces:
            if face_width_in_frame != 0:
                Distance = Distance_finder(Focal_length_found, Known_width, face_width_in_frame)
                Distance = round(Distance, 2)
                DISTANCE = int(Distance)
                print("Distance:", DISTANCE, "Direction:",Direction)

                # Control the car based on face position and distance
                if FC_X < Left_Bound:
                    Motor1_Speed = Truing_Speed
                    Motor2_Speed = Truing_Speed
                    Direction = 3
                elif FC_X > RightBound:
                    Motor1_Speed = Truing_Speed
                    Motor2_Speed = Truing_Speed
                    Direction = 4
                elif DISTANCE > 70 and DISTANCE <= 200:
                    Motor1_Speed = net_Speed
                    Motor2_Speed = net_Speed
                    Direction = 2
                elif DISTANCE > 20 and DISTANCE <= 70:
                    Motor1_Speed = net_Speed
                    Motor2_Speed = net_Speed
                    Direction = 1
                else:
                    Motor1_Speed = 0
                    Motor2_Speed = 0
                    Direction = 0

                # Display distance information and send control data to Arduino
                cv2.putText(frame, f"Distance {DISTANCE} CMs", (face_x-6, face_y-6), fonts, 0.6, BLACK, 2)
                data = f"A{Motor1_Speed}B{Motor2_Speed}D{Direction}"
                print(DISTANCE)
                Arduino.write(data.encode())
                time.sleep(0.002)
                Arduino.flushInput()

        # Draw reference lines
        # cv2.line(frame, (Left_Bound, 80), (Left_Bound, 480-80), YELLOW, 2)
        # cv2.line(frame, (RightBound, 90), (RightBound, 480-280), YELLOW, 2)
        cv2.line(frame, (160, 80), (160, 360), YELLOW, 2)
        cv2.line(frame, (320, 90), (320, 360), YELLOW, 2)
        cv2.imshow("frame", frame)

        # Exit the loop on 'q' key press
        if cv2.waitKey(1) == ord("q"):
            break

    Arduino.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

# How to run this nigga???
# /usr/local/bin/python3 /Users/pulkitbatra/Desktop/FaceRecognitionCar/main2.py
