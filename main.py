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
from multiprocessing.pool import ThreadPool
from random import choice

FILTERS = ("BLUR","CONTOUR","DETAIL","EDGE_ENHANCE","EDGE_ENHANCE_MORE","EMBOSS","FIND_EDGES","SHARPEN","SMOOTH","SMOOTH_MORE")
DEGREES = ("ROTATE_45","ROTATE_90","ROTATE_135")

class KedClient:
    
    def __init__(self):
        self.root = Tk()

        self.image = Image.open("./test_images/quote.png")
        self.image_copy = self.image.copy()
        self.image_copy = self.image_copy.resize((800, 500), Image.ANTIALIAS)
        self.filter_var = StringVar()
        self.rotation_var = StringVar()
        self.stack = [self.image_copy]
        #initializing tkinter widgets
        self.init_widgets(self.image_copy)
        #adding widgets to grid
        self.add_widgets_to_frame()
        
        #setting root window title
        self.root.title("K Editor")
        #fixing root window size
        self.root.resizable(width=False, height=False)

        self.root.mainloop()

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
        self.open_file_button  = ttk.Button(self.menu_frame, text="Open Image", command=lambda: self.file_dialog_handler())
        
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
        self.message_label.grid(row=0,column=0)      
        self.message_label.grid_forget()

    def file_dialog_handler(self):
        """method to handle open image dialog"""
        image = UIdialog.open_file_dialog()
        self.image_copy = image
        self.update_picture_panel(self.image_copy)

    def grayscale_button_handler(self):
        def callback():
            self.message_label.grid()
            self.image_copy = grayscale.convert_to_grayscale(self.image_copy)
            self.update_picture_panel(self.image_copy)
            self.message_label.grid_forget()
        thread = threading.Thread(target=callback)
        thread.start()
        self.stack.append(self.image_copy)
        print(str(self.stack))    
    
    def flip_button_handler(self):
        self.image_copy = flip.flip_image(self.image_copy)
        self.update_picture_panel(self.image_copy)
        self.stack.append(self.image_copy)     
        print(str(self.stack))    

    def filter_combobox_event_handler(self):
        self.rotation_combobox.set("")
        filter_name = str(self.filter_combobox.get())
        image_copy  = _filter.apply_filter(self.image_copy,filter_name)
        self.update_picture_panel(image_copy)

    def rotation_combobox_event_handler(self):
        self.filter_combobox.set("")
        degrees = str(self.rotation_combobox.get())
        image_copy = _rotation.apply_rotation(self.image_copy,degrees)
        self.update_picture_panel(image_copy)

    def image_info_button_handler(self):
        UIdialog.show_image_info_dialog(self.image_copy)

    def undo_button_handler(self):
        self.stack.pop()
        print(str(self.stack))    
        # self.update_picture_panel(self.stack[len(self.stack)-1])
        # print("undo clicked")
        
    def update_picture_panel(self,image_copy):
        """method to update picture in picture panel"""
        self.picture = ImageTk.PhotoImage(image_copy)        
        self.picture_panel.configure(image=self.picture)
        self.picture_panel.photo = self.picture


if __name__ == "__main__":
    # thread = threading.Thread(target=KedClient())
    # thread.start()
    client = KedClient()
   