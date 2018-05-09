"""
    Date: 07 May 2018
    Author: Kartik Sharma
"""

from UI.dialogs import UIdialog 
from lib import grayscale, flip, _filter, _rotation
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import copy
import datetime
#from multiprocessing.pool import ThreadPool
from random import choice

#constants
FILTERS = ("BLUR","CONTOUR","DETAIL","EDGE_ENHANCE","EDGE_ENHANCE_MORE","EMBOSS","FIND_EDGES","SHARPEN","SMOOTH","SMOOTH_MORE")
DEGREES = ("ROTATE_30","ROTATE_45","ROTATE_90","ROTATE_135","ROTATE_180","ROTATE_225","ROTATE_270")

class KedClient:
    
    def __init__(self):
        self.root = Tk()

        #stack to store every edit so users can undo
        self.stack = []

        self.default_image = None
        self.default_image_copy = None

        self.init_default_image()
        print(self.stack)

        #widgets textVariables
        self.filter_var = StringVar()
        self.rotation_var = StringVar()

        #initializing tkinter widgets
        self.init_widgets(self.default_image_copy)
        #adding widgets to grid
        self.add_widgets_to_frame()
        
        #setting root window title
        self.root.title("K Editor")
        #fixing root window size
        self.root.resizable(width=False, height=False)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def init_default_image(self):
        self.setDefaultImage("./test_images/touka.png")
        self.default_image_copy = self.make_image_copy(self.default_image,None)
        #resizing image to fit picture panel
        self.default_image_copy = self.resize_image(self.default_image_copy,800,500)

    def setDefaultImage(self,path):
        """method to set default image in picture panel """
        self.default_image = Image.open(path)
        self.stack.append(self.default_image)

    def make_image_copy(self,image,image_filename):
        """method to make image copy"""
        if image == None:
            image_copy = Image.open(image_filename).copy()
        else:
            image_copy = image.copy()

        return image_copy

    def resize_image(self,image,*args):
        """method to resize image
           param - args : (width,height) 
        """
        # print(args)
        resized_image = image.resize(args, Image.ANTIALIAS)
        return resized_image

    def init_widgets(self,image):
        """function to initialize Ked widgets"""
        self.content = ttk.Frame(self.root)

        #widgets for picture preview
        self.picture           = ImageTk.PhotoImage(image)
        self.picture_container = ttk.Frame(self.content, width=800, height=500, borderwidth=2,relief="sunken")
        self.picture_panel     = ttk.Label(self.picture_container, image=self.picture)
        
        #menu widgets
        self.menu_frame        = ttk.Frame(self.content)
        self.grayscale_button  = ttk.Button(self.menu_frame, text="Grayscale",command=lambda:self.grayscale_button_handler())
        self.flip_button       = ttk.Button(self.menu_frame, text="Flip", command=lambda:self.flip_button_handler())
        
        #comboboxes
        self.filter_label      = ttk.Label(self.menu_frame, text="Filters: ")
        self.filter_combobox   = ttk.Combobox(self.menu_frame, textvariable=self.filter_var, state='readonly')
        self.filter_combobox.bind('<<ComboboxSelected>>',lambda e: self.filter_combobox_event_handler())
        self.filter_combobox['values'] = FILTERS
        self.rotation_label      = ttk.Label(self.menu_frame, text="Rotate: ")
        self.rotation_combobox   = ttk.Combobox(self.menu_frame, textvariable=self.rotation_var, state='readonly')
        self.rotation_combobox.bind('<<ComboboxSelected>>',lambda e1: self.rotation_combobox_event_handler())
        self.rotation_combobox['values'] = DEGREES
        
        self.image_info_button = ttk.Button(self.menu_frame, text="Image Info", command=lambda:self.image_info_button_handler())
        self.undo_button       = ttk.Button(self.menu_frame, text="Undo",command=lambda:self.undo_button_handler())
        self.open_file_button  = ttk.Button(self.menu_frame, text="Open", command=lambda: self.file_dialog_handler())
        self.save_file_button  = ttk.Button(self.menu_frame, text="Save", command=lambda: self.save_file_handler())
        #message labels
        self.message_label = ttk.Label(self.picture_container, text="Converting...")

    def add_widgets_to_frame(self):
        """method to add widgets in grid format"""
        self.content.grid(column=0, row=0)
        self.picture_container.grid(column=0, row=0, padx=5, pady=5)
        self.picture_panel.grid(column=0, row=0, padx=2, pady=2, sticky="nsew")
        self.menu_frame.grid(column=0, row=1, padx=5, pady=5, sticky="w")
        self.grayscale_button.grid(column=0, row=0, padx=5, pady=5)
        self.flip_button.grid(column=1, row=0, padx=5, pady=5)
        self.filter_label.grid(column=2, row=0, pady=5)
        self.filter_combobox.grid(column=3, row=0, padx=5, pady=5)
        self.rotation_label.grid(column=4, row=0, pady=5)
        self.rotation_combobox.grid(column=5, row=0, padx=5, pady=5)
        self.image_info_button.grid(column=6, row=0, padx=5, pady=5)
        self.undo_button.grid(column=7, row=0, padx=5, pady=5)
        self.open_file_button.grid(row=1,column=0,padx=5,pady=5) 
        self.save_file_button.grid(row=1,column=1,padx=5,pady=5)
        self.message_label.grid(row=0,column=0)      
        self.message_label.grid_forget()

    def grayscale_button_handler(self):
        def callback():
            self.message_label.grid()
            image = self.stack[len(self.stack)-1]
            image_copy = self.make_image_copy(image, None)
            image_copy = grayscale.convert_to_grayscale(image_copy)
            # print(image_copy)
            self.stack.append(image_copy)
            image_copy = self.resize_image(image_copy,800,500)
            self.update_picture_panel(image_copy)
            self.message_label.grid_forget()
            print("After converting to grayscale")
            print(str(self.stack))
        thread = threading.Thread(target=callback)
        thread.start()
            
    
    def flip_button_handler(self):
        image = self.stack[len(self.stack)-1]
        image_copy = self.make_image_copy(image, None)
        image_copy = flip.flip_image(image_copy)
        self.stack.append(image_copy)
        image_copy = self.resize_image(image_copy,800,500)
        self.update_picture_panel(image_copy)
        print("After Flipping")
        print(str(self.stack))    

    def filter_combobox_event_handler(self):
        def callback():
            self.message_label.grid()
            filter_name = str(self.filter_combobox.get())
            image       = self.stack[len(self.stack)-1]
            image_copy  = self.make_image_copy(image, None)   
            image_copy  = _filter.apply_filter(image_copy,filter_name)
            self.stack.append(image_copy)
            image_copy  = self.resize_image(image_copy,800,500)
            self.update_picture_panel(image_copy)
            print("After applying filter")
            print(str(self.stack))
            self.message_label.grid_forget()

        thread = threading.Thread(target=callback)
        thread.start()    
        

    def rotation_combobox_event_handler(self):
        degrees = str(self.rotation_combobox.get())
        image   = self.stack[len(self.stack)-1]
        image_copy = self.make_image_copy(image,None)
        image_copy = _rotation.apply_rotation(image_copy,degrees)
        self.stack.append(image_copy)
        image_copy  = self.resize_image(image_copy,800,500) 
        self.update_picture_panel(image_copy)
        print("After Rotating")
        print(str(self.stack))

    def image_info_button_handler(self):
        UIdialog.show_image_info_dialog(self.stack[len(self.stack)-1])

    def undo_button_handler(self):
        """method to undo changes done to image"""
        if(len(self.stack) > 1):
            self.stack.pop()
            print(str(self.stack))
            image = self.stack[len(self.stack)-1]
            image_copy = self.make_image_copy(image,None)
            image_copy = self.resize_image(image_copy,800,500)
            self.update_picture_panel(image_copy)
            print("After Undoing")
            print(str(self.stack))
        else:
            UIdialog.show_error_edit_image_first()
        # print("undo clicked")
    
    def file_dialog_handler(self):
        """method to handle open image dialog"""
        #opening image
        image_filename = UIdialog.open_file_dialog()
        #making image copy
        image_copy     = self.make_image_copy(None,image_filename)
        #appending newly opened image to stack
        self.stack.append(image_copy)
        #resizing image to fit picture panel
        image_copy     = self.resize_image(image_copy,800,500)
        #updating picture panel
        self.update_picture_panel(image_copy)


    def save_file_handler(self):
        """method for saving file"""
        def callback():
            image = self.stack[len(self.stack)-1]
            timestamp = str(int(datetime.datetime.now().timestamp()))
            file  = "./test_images/IMG" + timestamp 
            image.save(file + ".png")
            print("File save successfully!")
        thread = threading.Thread(target=callback)
        thread.start()

    def update_picture_panel(self,image):
        """method to update picture in picture panel"""
        self.picture = ImageTk.PhotoImage(image)        
        self.picture_panel.configure(image=self.picture)
        self.picture_panel.photo = self.picture

    def on_closing(self):
        """method to clear stack when window is closed"""
        self.stack.clear()
        print(self.stack)
        del self.stack[:]
        self.root.destroy()

if __name__ == "__main__":
    # thread = threading.Thread(target=KedClient())
    # thread.start()
    client = KedClient()

