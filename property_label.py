import tkinter as tk
from tkinter import ttk
from Properties.general import General
from Properties.android import Android
from Properties.ios import Ios
from Properties.permissions import Permissions
class PropertiesLabel:
    
            #self.device_label.pack()
    def on_mouse_wheel(self,event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        # Icon section
        
        self.canvas = tk.Canvas(self.frame,width=200)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Create a Scrollbar for the Canvas
        self.scrollbar = ttk.Scrollbar(
            self.frame,
            orient="vertical",
            command=self.canvas.yview,
            style="Custom.Vertical.TScrollbar"  # Custom scrollbar style
        )
        self.scrollbar.pack(side="left", fill="y")
        
        # Configure the Canvas to use the Scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.content_frame = ttk.Frame(self.canvas,width=200)
        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        self.content_frame.bind("<Configure>", self.update_scrollregion)
        self.content_frame.bind("<MouseWheel>", self.on_mouse_wheel)
        general=General(self.content_frame)
        android=Android(self.content_frame)
        ios=Ios(self.content_frame)
        permissions=Permissions(self.content_frame)
    def update_scrollregion(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        # Permissions section
        

        


    