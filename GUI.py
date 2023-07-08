import subprocess
import tkinter as tk
from tkinter import filedialog, Entry, Label
import shutil
from tkinter import *
from PIL import Image, ImageTk

# Create the main root window
root = tk.Tk()
root.geometry("800x600")  # Set the size of the interface to 800x600
root.title("File Selector")  # Set the title of the window

# Function to open the register interface
def open_register_interface():
    global register_window
    global entry_person
    global entry_mail
    global entry_age
    global entry_phone

    # Create a new window for registering missing persons
    register_window = Toplevel(root)
    register_window.geometry("800x600")

    # Add background image
    background_image = Image.open("C:\\Users\\Asus\\OneDrive\\Desktop\\Tracking Person\\back.png")
    background_image = background_image.resize((800, 600), Image.ANTIALIAS)
    background_render = ImageTk.PhotoImage(background_image)

    # Create a label to hold the background image
    background_label = tk.Label(register_window, image=background_render)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Button to select a file
    button_select = tk.Button(register_window, text="Select File", command=select_file)
    button_select.pack()
    button_select.place(x=640, y=240)

    # Label and entry field for entering the missing person's name
    label_person = Label(register_window, text="Enter missing person name:")
    label_person.config(height=3, width=20)
    label_person.pack(pady=20)
    entry_person = Entry(register_window)
    entry_person.pack()

    # Label and entry field for entering the missing person's age
    label_age = Label(register_window, text="Enter missing person age:")
    label_age.config(height=3, width=20)
    label_age.pack(pady=20)
    entry_age = Entry(register_window)
    entry_age.pack()

    # Label and entry field for entering the user's mail ID
    label_mail = Label(register_window, text="Enter your Mail_ID:")
    label_mail.config(height=3, width=30)
    label_mail.pack(pady=20)
    entry_mail = Entry(register_window, width=40)  # Increase width to 40
    entry_mail.pack()

    # Label and entry field for entering the user's phone number
    label_phone = Label(register_window, text="Enter your Phone_Number:")
    label_phone.config(height=3, width=20)
    label_phone.pack(pady=20)
    entry_phone = Entry(register_window)
    entry_phone.pack()

    # Button to submit the file
    button_submit = tk.Button(register_window, text="Submit", command=submit_file)
    button_submit.place(x=130, y=240)


def open_file():
    file_path = tk.filedialog.askopenfilename()
   

# Load the background image
background_image = Image.open("C:\\Users\\Asus\\OneDrive\\Desktop\\Tracking Person\\back.png")
background_image = background_image.resize((800, 600), Image.ANTIALIAS)
background_render = ImageTk.PhotoImage(background_image)

# Create a label to hold the background image
background_label = tk.Label(root, image=background_render)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


def select_file():
    global file_path
    global label_image
    file_path = filedialog.askopenfilename()
    
    load = Image.open(file_path)
   
    # Resize the loaded image to 200x200 pixels
    load = load.resize((200, 200), Image.Resampling.LANCZOS)
    render = ImageTk.PhotoImage(load)
    
    label_image = tk.Label(register_window, image=render)
    label_image.image = render
    label_image.pack()
    label_image.place(x=580, y=10)  # Place the image at the top right


def submit_file():
    destination = "C://Users//Asus//OneDrive//Desktop//Tracking Person//Database_Images//"
    missing_person = entry_person.get()
    missing_person_age = entry_age.get()
    missing_person_phone = entry_phone.get()
    missing_person_mail = entry_mail.get()
    
    
    # Print the gathered information
    print("Missing Person:", missing_person)
    print("Age:", missing_person_age)
    print("Phone Number:", missing_person_phone)
    print("Mail ID:", missing_person_mail)


    # Copy the selected file to a new location with a modified file name
    new_file_path = destination + missing_person + "_" + str(missing_person_age) + "_" + str(missing_person_phone) + "_" + str(missing_person_mail) + ".jpg"
    shutil.copy(file_path, new_file_path)

    # Append the file information to a text file
    with open("missing_persons.txt", "a") as f:
        f.write("{} {} {} {} {}\n".format(new_file_path, missing_person, missing_person_age, missing_person_phone, missing_person_mail))

    # Print the path of the submitted file
    print("File submitted to:", new_file_path)

    # Extract the mail ID from the file path and print it
    mail_id = new_file_path.split("_")[4].split(".jpg")[0]
    print("Mail ID:", mail_id)

    # Clear the entry fields, remove the displayed image, and reset the image label
    entry_person.delete(0, 'end')
    entry_age.delete(0, 'end')
    entry_phone.delete(0, 'end')
    entry_mail.delete(0, 'end')
    label_image.config(image='')
    label_image.image = None


# Function to start surveillance
def start_surveillance():
    subprocess.call(["python", "main.py"])


# Function for face recognition
def face_recognition():
    subprocess.call(["python", "Face_recognition.py"])


# Button to open the register interface
button_register = tk.Button(root, text="Register", command=open_register_interface)
button_register.pack()
button_register.place(x=130, y=200)

# Button to start surveillance
button_submit = tk.Button(root, text="Surveillance", command=start_surveillance)
button_submit.place(x=130, y=240)

# Button for face recognition
button_submit = tk.Button(root, text="Face_Recognition", command=face_recognition)
button_submit.place(x=130, y=280)

# Run the main GUI loop
root.mainloop()
