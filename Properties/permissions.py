from tkinter import ttk
import tkinter as tk
class Permissions:
    p_list=["INTERNET",
            "CAMERA",
            "STORAGE",
            "BLUETOOTH",
            "FLASHLIGHT",
            "VIBRATE"]
    p_var=[]
    cb=[]
    def __init__(self,frame):
        self.frame=frame
        #self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.permissions_state_var = tk.IntVar()
        self.permissions_state_var.set(0)  # Default to "Hidden"
        self.toggle_device = ttk.Label(
            self.frame,
           # width=200,
            text="Permissions ►",  # Show a right arrow initially
            cursor="hand2",  # Change cursor on hover
            anchor="w",
            background="black",
            foreground="#00FF00"

        )
        self.toggle_device.grid(sticky="w",column=0,row=30)
        self.toggle_device.bind("<Button-1>", self.toggle_permissions_visibility)
        for i,permission in enumerate(Permissions.p_list):
            a=tk.BooleanVar
            Permissions.p_var.append(a)
            c1 = tk.Checkbutton(self.frame, text=str(permission),variable=Permissions.p_var[i], onvalue=True, offvalue=False)
            Permissions.cb.append(c1)
       
        #self.permissions=['INTERNET','STORAGE','CAMERA']
        


        
    def toggle_permissions_visibility(self, event):
        if self.permissions_state_var.get() == 1:  # Currently visible
           # self.device_content_frame.grid_remove()  # Hide the device content frame
            self.toggle_device.config(text="Permissions ►")  # Show a right arrow
            self.permissions_state_var.set(0)  # Set state to "Hidden"
            for c in Permissions.cb:
                c.grid_remove()



        else:
            for i,c in enumerate(Permissions.cb):
                c.grid(sticky="w",column=0,row=31+i)
           # self.device_content_frame.grid()  # Show the device content frame
            self.toggle_device.config(text="Permissions ▼")  # Show a down arrow
            self.permissions_state_var.set(1)  # Set state to "Visible"
            # Add additional properties as needed


    
    
