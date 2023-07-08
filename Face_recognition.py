from email import encoders
import tkinter as tk
import tkinter.filedialog
import subprocess
import sys
import face_recognition
import cv2
import os
import numpy as np
from PIL import Image, ImageTk
from tkinter import filedialog
import datetime
import pywhatkit
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

# Directory containing the images
path = 'Database_Images'

# Lists to store images and their class names
images = []
classNames = []

# Get the list of files in the directory
myList = os.listdir(path)
print(myList)

# Loop through the files
for cl in myList:
    # Read the image
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    # Get the class name by removing the file extension
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

# Extract mail IDs from file names
mail_ids = []
for name in myList:
    mail_id = name.split("_")[3][:-4]
    mail_ids.append(mail_id)

family_mail_ID = print(*mail_ids, sep=", ")
family_mail_ID = ", ".join(mail_ids)

# Extract phone numbers from file names
phone =[]
for name1 in myList:
    phone1 = name.split("_")[2]
    phone.append(phone1)
family_phone = print(*phone, sep=', ')
family_phone = ", ".join(phone)
phone = "+91" + phone1

# Function to read an image
def read_img(path):
    img = cv2.imread(path)
    (h, w) = img.shape[:2]
    width = 500
    ratio = width / float(w)
    height = int(h * ratio)
    return cv2.resize(img, (width, height))

# Lists to store known encodings and names
Known_encodings = []
known_names = []

known_dir = 'C:\\Users\\Asus\\OneDrive\\Desktop\\Tracking Person\\Database_Images'

# Loop through the files in the known directory
for file in os.listdir(known_dir):
    if file.endswith(('.png', '.jpg', '.jpeg', 'tiff')):
        # Read the image
        img = read_img(known_dir + '/' + file)
        # Get the face encoding of the image
        img_enc = face_recognition.face_encodings(img)
        if len(img_enc) == 0:
            print("Could not detect face in image " + file)
        else:
            # Append the encoding and name to the respective lists
            Known_encodings.append(img_enc[0])
            known_names.append(file.split('.')[0])

def is_blurry(img):
    # Calculate the variance of Laplacian of the image
    variance = cv2.Laplacian(img, cv2.CV_64F).var()
    # Return True if the variance is less than 100 (indicating blur)
    return variance < 100

def display_image(path, label):
    # Open and resize the image
    img = Image.open(path)
    img = img.resize((250, 250), Image.ANTIALIAS)
    # Convert the image to PhotoImage format
    img = ImageTk.PhotoImage(img)
    try:
        # Update the label with the new image
        label.config(image=img)
        label.image = img
    except:
        # If the label doesn't exist, create a new label and display the image
        label = tk.Label(root, bg='black', image=img)
        label.image = img
        label.pack(side="right")


def mail():
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import smtplib

    fromaddr = "ENTER THE MAIL_ID YOU WANT TO USE TO SEND THE MAIL"
    toaddr = f"{family_mail_ID}"

    msg = MIMEMultipart()
    msg["from"] = "ENTER THE MAIL_ID YOU WANT TO USE TO SEND THE MAIL"
    msg["to"] = f"{family_mail_ID}"
    msg["subject"] = "Mail from Tracking Person Using Intelligent Surveillance System"
    body = "The person on whom you had filed a missing case has been detected. Please contact the nearby police station for further inquiry."

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "ENTER THE MAIL_APP ID ") # ITS MAIL APP ID NOT MAIL_ID PASSWORD
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

    with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login("ENTER MAIL_ID FROM WHICH YOU WANT TO SEND MAIL", "ENTER MAIL APP ID")
        smtp.send_message(msg)
        print("Sent...")

def compare_faces():
    global unknown_image_label
    global known_image_label
    global Known_encodings, known_names
    global details_label
    global phone1

    flag = False
    flag = False

    # Ask the user to select an image from the Unknown directory
    unknown_path = tk.filedialog.askopenfilename(title="Select an image from Unknown directory")
    img = read_img(unknown_path)

    # Check if the image is blurry
    if is_blurry(img):
        unknown_image_label = tk.Label(root, bg='black')
        unknown_image_label.pack(side="left")
        display_image(unknown_path, unknown_image_label)
        label.config(text="Sorry, the image is too blurry to detect the face.")
    else:
        img_enc = face_recognition.face_encodings(img)
        unknown_image_label = tk.Label(root, bg='black')
        unknown_image_label.pack(side="left")
        display_image(unknown_path, unknown_image_label)

        if len(img_enc) == 0:
            label.config(text="Could not detect face in image.")
        else:
            try:
                unknown_image_label.destroy()
            except:
                pass

            try:
                known_image_label.destroy()
            except:
                pass

            unknown_image_label = tk.Label(root, bg='black')
            unknown_image_label.pack(side="left")
            display_image(unknown_path, unknown_image_label)

            # Compare the unknown face with known faces
            results = face_recognition.compare_faces(Known_encodings, img_enc[0], tolerance=0.47)

            for i in range(len(results)):
                if results[i]:
                    label.config(text=known_names[i])
                    known_image_label = tk.Label(root, bg='black')
                    known_image_label.pack(side="right")
                    display_image(known_dir + '\\' + known_names[i] + '.com.jpg', known_image_label)
                    flag = True

                    # Extract details from the file name
                    file_name = known_names[i] + ".com"
                    missing_person, age, phone, email = file_name.split("_")
                    missing_person = missing_person.replace(".com.jpg", "")
                    age = age.replace(".jpg", "")
                    print("Matching Face found!")
                    print("Missing person:", missing_person)
                    print("Age:", age)
                    print("Phone:", phone)
                    print("Email:", email)
                    phone1 = "+91" + phone

            if not flag:
                label.config(text="Sorry, no match found.")
            else:
                details_text = "Matching Face found!\nMissing person: " + missing_person + "\nAge: " + age + "\nPhone: " + phone + "\nEmail: " + email
                label.config(text=details_text)
                details_label = tk.Label(root, text=details_text, bg='black')
                details_label.pack()
                mail()
                whatsapp()


def whatsapp():
    # Get the current time
    now = datetime.datetime.now()

    # Add 1 minute to the current time
    send_time = datetime.time(now.hour, now.minute + 2)

    # Send the message using pywhatkit
    pywhatkit.sendwhatmsg(phone1, "This is from Tracking Person using Intelligent Surveillance... The report you had registered for a missing person has been located... Please check your Registered Mail_ID for more details.", send_time.hour, send_time.minute)



def compare_new_image():
    try:
        unknown_image_label.destroy()
        known_image_label.destroy()
    except:
        pass

    try:
        known_image_label.destroy()
    except:
        pass

    label.config(text="")


root = tk.Tk()
root.title("Facial Recognition")
root.geometry("800x600")
root['bg'] = 'black'

frame = tk.Frame(root, bg='black')
frame.pack(pady=10, padx=20)

compare_button = tk.Button(frame, text="Compare Faces", command=compare_faces)
compare_button.pack()

compare_button = tk.Button(frame, text="Compare New Image", command=compare_new_image)
compare_button.pack(pady=20)

label = tk.Label(root, text="", bg='black', fg='white')
label.pack(pady=10, side="left")

root.mainloop()
