from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk

def open_file_dialog():
    image_filename = filedialog.askopenfilename(initialdir = "../../",title = "Select Image to Edit",filetypes = (("jpeg files","*.jpg"),("png files","*.png")))
    # image_copy = crop_image(imagefilename)
    return image_filename

def show_image_info_dialog(image):
    """method to show image info in a dialog"""
    image_info = "Format: {}\nSize: {}\nMode: {}".format(image.format,image.size,image.mode)
    messagebox.showinfo(message=image_info)

def show_error_edit_image_first():
    error = "Please edit image first!!" 
    messagebox.showinfo(message=error)

# def crop_image(image_file_name):
#     image = Image.open(image_file_name)
#     image_copy = image.copy()
#     image_copy = image_copy.resize((800, 500), Image.ANTIALIAS)
#     return image_copy