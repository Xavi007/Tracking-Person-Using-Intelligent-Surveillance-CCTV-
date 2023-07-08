import cv2
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps, ImageDraw
from mtcnn import MTCNN

import cv2
import numpy as np

def person_recognition_model(face_roi, img):
    # Convert face_roi to grayscale
    face_roi_gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)

    # Convert img to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Resize face_roi_gray to the same size as img_gray
    face_roi_gray = cv2.resize(face_roi_gray, (img_gray.shape[1], img_gray.shape[0]))

    # Calculate Mean Squared Error (MSE) between face_roi_gray and img_gray
    mse = np.mean((face_roi_gray - img_gray) ** 2)
    
    # Define a threshold for person recognition
    threshold = 1000

    # If MSE is below threshold, consider it a match
    if mse < threshold:
        return True
    else:
        return False


# Create Tkinter window
root = tk.Tk()
root.title("Person Detection")

# Create canvas for displaying video frames
canvas = tk.Canvas(root, width=640, height=480)
canvas.pack()

# Load pre-trained face detection model
face_detector = MTCNN()

# Variable to store detected person's name
person_name = ""

# Folder path for images to compare
images_folder = "C://Users//Asus//Desktop//front//Images"

# Load images from the images folder
image_files = os.listdir(images_folder)
images = []
for file in image_files:
    if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
        img = cv2.imread(os.path.join(images_folder, file))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        images.append(img)

# Function to browse for video file
def browse_file():
    global video_file
    video_file = filedialog.askopenfilename()

# Function to start person detection
def start_detection():
    global person_name
    cap = cv2.VideoCapture(video_file)

    while cap.isOpened():
        # Read video frame
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_detector.detect_faces(frame)

        # Draw bounding boxes around detected faces
        for face in faces:
            x, y, w, h = face['box']
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Extract face region from the frame
            face_roi = frame[y:y + h, x:x + w]

            # Perform person recognition on the extracted face region
            recognized = False
            for i, img in enumerate(images):
                # Perform face recognition on each image in the images folder
                # (You can replace this with your own person recognition model)
                if person_recognition_model(face_roi, img):
                    person_name = image_files[i].split(".")[0]
                    recognized = True
                    break

            if recognized:
                # Stop video playback
                cap.release()

                # Display the person's name on the prompt
                print("Person Recognized: ", person_name)

                # Draw person's name on the frame
                cv2.putText(frame, person_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Convert frame to RGB for displaying in Tkinter canvas
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert frame to ImageTk format
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(frame)

        # Update canvas with the new frame
        canvas.create_image(0, 0, anchor=tk.NW, image=frame)

        # Update Tkinter window
        root.update()

# Browse button
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack()

# Start detection button
start_button = tk.Button(root, text="Start Detection", command=start_detection)
start_button.pack()

# Run Tkinter event loop
root.mainloop()
