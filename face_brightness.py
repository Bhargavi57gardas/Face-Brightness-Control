import cv2
import numpy as np
import screen_brightness_control as sbc

# Load the Haar cascade face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Open the default webcam
cap = cv2.VideoCapture(0)

# Reference face width (in pixels) when at a known distance (you may need to calibrate this)
reference_face_width = 150  # Change based on your setup
min_brightness = 20
max_brightness = 100

def get_brightness_from_distance(face_width):
    if face_width == 0:
        return min_brightness
    distance_ratio = reference_face_width / face_width
    brightness = max(min(int(max_brightness * distance_ratio), max_brightness), min_brightness)
    return brightness

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        # If faces are detected
        if len(faces) > 0:
            # Use the largest detected face (closest to camera)
            largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
            x, y, w, h = largest_face

            # Draw rectangle around the face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Estimate brightness
            brightness = get_brightness_from_distance(w)
            sbc.set_brightness(brightness)
            cv2.putText(frame, f'Brightness: {brightness}%', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Show the result
        cv2.imshow('Face Brightness Control', frame)

        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
            break

finally:
    cap.release()
    cv2.destroyAllWindows()