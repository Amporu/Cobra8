import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import time
from Device import Device,DeviceThread,DeviceLabel  # Import your Device class (assuming it contains capture logic)
from text_editor import Editor
from solution_explorer import SolutionExplorer
from property_label import PropertiesLabel
from logcat_label import LogcatLabel
from android_data import DataThread
#from test import SolutionExplorer
import queue
from monitor import MonitorLabel

class PandoraIDE:
    def __init__(self):
        
        self.root = tk.Tk()
        self.root.title("Simple IDE")
        self.root.geometry("1400x600")
        
        buttons =ttk.PanedWindow(self.root,orient="horizontal",width=self.root.winfo_width())
        
        buttons.pack()
        create_project_button=ttk.Button(buttons,text="\u271A Create Project")
        create_project_button.grid(column=0,row=0)#pack(side=tk.LEFT,padx=30)
        style = ttk.Style()
        style.configure('Run.TButton', background='#FF0000')
        run_on_nutton=ttk.Button(buttons,text="\u25B6 Run on")
        run_on_nutton.grid(column=1,row=0)#pack(side=tk.LEFT)
        options = ["    \U0001F4BB    ", "    \U0001F4F1    "]
        

        # Create a Combobox widget
        self.dropdown = ttk.Combobox(buttons, values=options,state="readonly",width=1,background="blue",foreground="red")
        self.dropdown.set(options[0])
        self.dropdown.grid(column=2,row=0)#pack(side=tk.LEFT)
        style = ttk.Style()
        style.configure("NoArrow.TButton", arrowcolor=style.lookup("TButton", "background"),anchor="center")
        style.configure("NoArrow.TButton", selectbackground=("active", "lightblue"))

# Apply the custom style to the combobox
        self.dropdown.configure(style="NoArrow.TButton")
        #style.configure("Centered.TCombobox", padding=[5, 0, 0, 0], anchor="center")

        # Apply the centered text style to the combobox
        #self.dropdown.configure(style="Centered.TCombobox")
        main_pane = ttk.Panedwindow(self.root, orient="horizontal")
        main_pane.pack(fill="both", expand=True)
        
        self.device_label = DeviceLabel(self.root)
        self.debug_label = LogcatLabel(self.root)
        self.properties_label=PropertiesLabel(self.root)
        
        
        editor = Editor(main_pane, self.root)
        SolutionExplorer(main_pane, editor, self.root)
        self.device_pane = ttk.Notebook(main_pane)
        self.device_pane.add(self.device_label.frame, text="Device")
        self.device_pane.add(self.debug_label.frame, text="Debug")
        self.device_pane.add(self.properties_label.frame,text="Properties")
        main_pane.add(editor.editor_notebook)
        main_pane.add(self.device_pane)
        self.monitor_label=MonitorLabel(self.root)
       # self.monitor_label.pack()
        project_path = ""
        self.capture_threads = []

        #if self.get_active_tab() == "Device":
        if Device.is_usb_device_connected():
            #message_queue = queue.Queue()
            Device.connected=True
            data_thread=DataThread(self.device_label)
            data_thread.daemon=True
            data_thread.start()
            capture_thread = DeviceThread(self.device_label.device_label)
            capture_thread.daemon = True
            capture_thread.start()
            self.capture_threads.append(capture_thread)
            self.capture_threads.append(data_thread)
            #else:
            self.debug_label.start_logcat()
            self.monitor_label.start_monitor()
        else: 
            pass
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    def on_select(self,event):
        selected_option = self.dropdown.get()
        #self.dropdown.set(selected_option)
        #sellabel.config(text=f"Selected: {selected_option}")
    def get_active_tab(self):
        try:
            return self.device_pane.tab(self.device_pane.select(), "text")
        except tk.TclError:
            return None

    def on_close(self):
        for thread in self.capture_threads:
            thread.stop()
        self.root.destroy()



    






if __name__ == "__main__":
    #capture_thread = threading.Thread(target=Device.enable_screen_record)
    #capture_thread.start()
    #capture_thread.join()
    pan = PandoraIDE()
    pan.root.mainloop()
