from tkinter import ttk
import tkinter as tk
class Ios:

    def __init__(self,frame):
        self.frame=frame
        #self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.android_state_var = tk.IntVar()
        self.android_state_var.set(0)  # Default to "Hidden"
        self.toggle_device = ttk.Label(
            self.frame,
            #width=200,
            text="IOS ►",  # Show a right arrow initially
            cursor="hand2",  # Change cursor on hover
            anchor="w",
            background="black",
            foreground="#00FF00"
            
        )
        self.toggle_device.grid(sticky="w",column=0,row=20)
        self.toggle_device.bind("<Button-1>", self.toggle_android_visibility)
        # Create labels and entry fields for app properties
        self.deployment_target=self.create_android_label("Deployment Target:",c=0,r=21)
        self.deployment_target_entry = self.create_android_entry("12",c=0,r=22)



        self.target_sdk=self.create_android_label("SDK Version:",c=0,r=23)
        self.target_sdk_entry = self.create_android_entry("15",c=0,r=24)
    def toggle_android_visibility(self, event):
        if self.android_state_var.get() == 1:  # Currently visible
           # self.device_content_frame.grid_remove()  # Hide the device content frame
            self.toggle_device.config(text="IOS ►")  # Show a right arrow
            self.android_state_var.set(0)  # Set state to "Hidden"
            self.delete_item(self.deployment_target_entry)
            self.delete_item(self.deployment_target)

            self.delete_item(self.target_sdk_entry)
            self.delete_item(self.target_sdk)
        else:
            self.deployment_target=self.put_android_label("Deployment Target:",c=0,r=21)
            self.deployment_target_entry = self.put_android_entry("12",c=0,r=22)

            self.target_sdk=self.put_android_label("SDK Version:",c=0,r=23)
            self.target_sdk_entry = self.put_android_entry("15",c=0,r=24)
           # self.device_content_frame.grid()  # Show the device content frame
            self.toggle_device.config(text="IOS ▼")  # Show a down arrow
            self.android_state_var.set(1)  # Set state to "Visible"
            # Add additional properties as needed


    def create_android_label(self, text,c,r):
        label = ttk.Label(self.frame, text=text)
        #label.grid(sticky="w")
        return label
    
    
    def create_android_entry(self, default_value,c,r):
       # entry.tag_configure("color_tag", foreground="green")
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