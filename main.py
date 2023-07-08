import csv
import smtplib
import zipfile
from bs4 import BeautifulSoup
import cv2
import idna
import numpy as np
import face_recognition
import os
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import COMMASPACE
import pywhatkit
import requests
import json
from bs4 import BeautifulSoup


path = 'Database_Images'  # Setting the path variable to the 'Database_Images' directory


def extract_mail_id(file_name):
    """
    Extracts the mail ID from the given file name.

    Args:
        file_name (str): The file name.

    Returns:
        str: The extracted mail ID.
    """
    return file_name.split("_")[3][:-4]


def extract_phone_number(file_name):
    """
    Extracts the phone number from the given file name.

    Args:
        file_name (str): The file name.

    Returns:
        str: The extracted phone number.
    """
    phone_number = file_name.split("_")[2]
    return "+91" + phone_number


def extract_data_from_images(path):
    """
    Extracts data from images in the given path.

    Args:
        path (str): The path to the directory containing the images.

    Returns:
        tuple: A tuple containing the extracted images, class names, family mail ID, and family phone numbers.
    """
    images = []  # List to store the extracted images
    classNames = []  # List to store the class names
    myList = os.listdir(path)  # Get the list of files in the given path
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')  # Read the image using OpenCV
        images.append(curImg)  # Append the image to the list
        classNames.append(os.path.splitext(cl)[0])  # Append the class name (file name without extension)
    
    mail_ids = [extract_mail_id(name) for name in myList]  # Extract mail IDs from file names
    family_mail_ID = ", ".join(mail_ids)  # Join mail IDs into a string
    
    phone_numbers = [extract_phone_number(name) for name in myList]  # Extract phone numbers from file names
    family_phone = ", ".join(phone_numbers)  # Join phone numbers into a string
    
    return images, classNames, family_mail_ID, family_phone


path = 'Database_Images'  # Set the path to the 'Database_Images' directory
images, classNames, family_mail_ID, family_phone = extract_data_from_images(path)  # Extract data from images
def location():
    """
    Function for getting location using web scraping and making HTTP requests.
    """
    from bs4 import BeautifulSoup  # Importing BeautifulSoup for HTML parsing
    import requests  # Importing the requests library for making HTTP requests
    import json  # Importing the JSON library for working with JSON data


def whatsapp(phone):
    """
    Function for sending a WhatsApp message using the pywhatkit library.

    Args:
        phone (str): The phone number to send the message to.
    """
    # Get current time
    time_now = datetime.datetime.now().time()

    # Set time to send message (2 minutes after current time)
    send_time = datetime.time(time_now.hour, (time_now.minute + 2) % 60)

    # Send the message
    pywhatkit.sendwhatmsg(phone, "This is from Tracking Person using Intelligent Surveillance... The report you had registered for a missing person has been located... Please check your Registered Mail_ID for more details.", send_time.hour, send_time.minute)




def mail(family_mail_ID, location):
    """
    Function for sending an email with attachments.

    Args:
        family_mail_ID (str): The family mail ID to send the email to.
        location: The location data.
    """
    fromaddr = "Type your Mail_id"
    toaddr = family_mail_ID
    
    msg = MIMEMultipart()
    msg["From"] = "Type your Mail_id"
    msg["To"] = COMMASPACE.join(toaddr)
    msg["Subject"] = "Mail from Tracking Person Using Intelligent Surveillance System"
    body = "Location data attached."

    msg.attach(MIMEText(body, "plain"))

    # Attach the CSV file
    filename = "location.csv"
    with open("location.csv", "rb") as f:
        part = MIMEApplication(f.read(), Name=filename)
    part["Content-Disposition"] = f'attachment; filename="{filename}"'
    msg.attach(part)

    # Attach the directory as a zip file
    dir_name = "surveillance_images"
    zip_name = f"{dir_name}.zip"
    with open(zip_name, "wb") as f:
        zip_file = zipfile.ZipFile(f, mode="w")
        for file_name in os.listdir(dir_name):
            file_path = os.path.join(dir_name, file_name)
            if os.path.isfile(file_path):
                zip_file.write(file_path, arcname=file_name)
        zip_file.close()
    with open(zip_name, "rb") as f:
        part = MIMEApplication(f.read(), Name=zip_name)
    part["Content-Disposition"] = f'attachment; filename="{zip_name}"'
    msg.attach(part)

    # Send the email
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(fromaddr, "CREATE YOUR Mail_APP ID AND PASTE HERE") #not the mail_id password but mail app id
        smtp.sendmail(fromaddr, toaddr, msg.as_string())
        print("Sent...")

def findEncodings(images):
    """
    Function to find face encodings from a list of images.

    Args:
        images (list): List of images.

    Returns:
        list: List of face encodings.
    """
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

import requests

# Get location information
response = requests.get(url='ENTER YOUR IPSTACK API ID') #create a free account on ipstack and paste your id 
info = response.json()

# Extract latitude, longitude, and city from info dictionary
latitude = info[0].get('Latitude')
longitude = info[0].get('Longitude')
city = info[0].get('city')
pin = info[0].get('pin')


# Define function to save screenshot
def save_screenshot(img, name):
    """
    Function to save a screenshot image.

    Args:
        img: The screenshot image.
        name (str): The name to be used for the saved image.
    """
    # Create directory for surveillance images if it does not exist
    if not os.path.exists('surveillance_images'):
        os.mkdir('surveillance_images')

    # Generate unique filename for screenshot
    filename = f'surveillance_images/{name}_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg'

    # Save screenshot to file
    cv2.imwrite(filename, img)


def markAttendance(name, info):
    """
    Function to mark attendance and write the details to a CSV file.

    Args:
        name (str): The name of the person.
        info (dict): The location information.
    """
    # Split the name and extract the desired part
    name_parts = name.split('_')
    first_name = name_parts[0]

    with open('location.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([first_name, datetime.datetime.now().strftime('%H:%M:%S'), datetime.datetime.now().strftime('%Y-%m-%d'), info['city'], info['pin'], info['Latitude'], info['Longitude']])

    with open('location.csv', 'r') as f:
        myDataList = f.readlines()

encodeListKnown = findEncodings(images)
print('Encoding Complete')

# Open the webcam
cap = cv2.VideoCapture(0)

while True:
    # Read frame from the webcam
    success, img = cap.read()

    # Resize the frame for faster processing
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Detect faces in the frame
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        # Compare the detected face with known faces
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            # Get the name of the matched person
            name = classNames[matchIndex]
            print(name)
            
            # Extract phone number and email from name
            name_parts = name.split('_')
            phone = "+91" + name_parts[-2]
            email = name_parts[-1]
            print("Phone:", phone)
            print("Email:", email)

            # Draw a rectangle around the detected face
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 250, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            # Get location information
            response = requests.get(f'ENTER YOUR IPSTACK API ID') #create a free account on ipstack and paste your id
            info = response.json()[0]

            # Print the info dictionary
            print(info)

            # Mark attendance and save screenshot
            markAttendance(name, info)


            save_screenshot(img, name)

            # Send email with location details
            mail(email, location)

            # Send WhatsApp message
            whatsapp(phone)

    # Display the image with detections
    cv2.imshow('webcam', img)

    # Break the loop if 'Enter' key is pressed
    if cv2.waitKey(10) == 13:
        break

# Release the webcam and destroy all windows
cap.release()
cv2.destroyAllWindows()

