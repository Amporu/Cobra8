import tkinter as tk
from tkinter import ttk
class General:
    def __init__(self,frame):
        self.frame=frame
        #self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.android_state_var = tk.IntVar()
        self.android_state_var.set(0)  # Default to "Hidden"
        self.toggle_device = ttk.Label(
            self.frame,
            width=200,
            text="General ►",  # Show a right arrow initially
            cursor="hand2",  # Change cursor on hover
            anchor="w",
            background="black",
            foreground="#00FF00"
            
        )
        self.toggle_device.grid(sticky="w",column=0,row=1)
        self.toggle_device.bind("<Button-1>", self.toggle_android_visibility)
        # Create labels and entry fields for app properties
        self.app_name=self.create_android_label("App Name:")
        self.app_name_entry = self.create_android_entry("default_app")

        self.icon_name=self.create_android_label("Icon:")
        self.icon_name_entry = self.create_android_entry("icon.png")

        self.version_code=self.create_android_label("Version Code:")
        self.version_code_entry = self.create_android_entry("30")
    def toggle_android_visibility(self, event):
        if self.android_state_var.get() == 1:  # Currently visible
           # self.device_content_frame.grid_remove()  # Hide the device content frame
            self.toggle_device.config(text="General ►")  # Show a right arrow
            self.android_state_var.set(0)  # Set state to "Hidden"
            self.delete_item(self.app_name_entry)
            self.delete_item(self.app_name)
            self.delete_item(self.icon_name_entry)
            self.delete_item(self.icon_name)
            self.delete_item(self.version_code_entry)
            self.delete_item(self.version_code)
        else:
            self.app_name=self.put_android_label("App Name:",c=0,r=2)
            self.app_name_entry = self.put_android_entry("default_app",c=0,r=3)

            self.icon_name=self.put_android_label("Icon",c=0,r=4)
            self.icon_name_entry = self.put_android_entry("com.example.appname",c=0,r=5)

            self.version_code=self.put_android_label("Version Code",c=0,r=6)
            self.version_code_entry = self.put_android_entry("1.0",c=0,r=7)
           # self.device_content_frame.grid()  # Show the device content frame
            self.toggle_device.config(text="General ▼")  # Show a down arrow
            self.android_state_var.set(1)  # Set state to "Visible"
            # Add additional properties as needed


    def create_android_label(self, text):
        label = ttk.Label(self.frame, text=text)
        #label.grid(sticky="w")
        return label
    
    
    def create_android_entry(self, default_value):
        entry = ttk.Entry(self.frame)
        entry.insert(0, default_value)
        #entry.grid(sticky="ew")
        return entry
    def put_android_label(self, text,c,r):
        label = ttk.Label(self.frame, text=text)
        label.grid(sticky="w",column=c,row=r)
        return label
    def put_android_entry(self, default_value,c,r):
        entry = ttk.Entry(self.frame)
        entry.insert(0, default_value)
        entry.grid(sticky="ew",column=c,row=r)
        return entry
    def delete_item(self,label):
        label.grid_remove()