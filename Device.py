import cv2
import subprocess
import numpy as np
import tempfile
import os
import time
from PIL import Image,ImageTk
import threading
import tkinter as tk
from tkinter import ttk
# Path to the ADB executable
class Scheduler:
    previous_frame_time = 0
import tkinter as tk

class HollowCircleProgressBar(tk.Canvas):
    def __init__(self, parent, width, height, thickness=10):
        super().__init__(parent, width=width, height=height)
        self.width = width
        self.height = height
        self.thickness = thickness
        self.circle_progress = None
        self.progress = 0

    def update_progress(self, percentage):
        if self.circle_progress:
            self.delete(self.circle_progress)

        start_angle = 0
        end_angle = 360

        x0 = (self.width / 2) - (self.width / 2) * 0.8
        y0 = (self.height / 2) - (self.height / 2) * 0.8
        x1 = (self.width / 2) + (self.width / 2) * 0.8
        y1 = (self.height / 2) + (self.height / 2) * 0.8

        extent_angle = percentage * 360 / 100

        self.circle_progress = self.create_arc(x0, y0, x1, y1, start=start_angle, extent=extent_angle,
                                               outline="blue", width=self.thickness, style=tk.ARC)



#root.mainloop()

class ScrollableFrame(ttk.Frame):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        canvas = tk.Canvas(self)
        canvas.pack(side="left", fill="both", expand=True)
        ttk.Frame.__init__(self, canvas)
        canvas.create_window((0, 0), window=self, anchor="nw")
        #scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        #scrollbar.pack(side="right", fill="y")
        #canvas.configure(yscrollcommand=scrollbar.set)
        #canvas.bind("<Configure>", self.set_scrollregion)
class DeviceLabel:
    data_flag = 0
    def update_scrollregion(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    def __init__(self, root):
        self.frame = ttk.LabelFrame(root)

        # Create a Canvas widget for scrolling
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

        # Create a frame to hold the content
        self.content_frame = ttk.Frame(self.canvas,width=200)
        
        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        self.content_frame.bind("<Configure>", self.update_scrollregion)
        # Create a variable to hold the state of Device ► (0 for "Hidden", 1 for "Visible")
        self.device_state_var = tk.IntVar()
        self.device_state_var.set(0)  # Default to "Hidden"

        # Create a variable to hold the state of Info ► (0 for "Hidden", 1 for "Visible")
        self.info_state_var = tk.IntVar()
        self.info_state_var.set(0)  # Default to "Hidden"

        # Create a button-like label for "Device ►"
        self.toggle_device = ttk.Label(
            self.content_frame,
            width=200,
            text="Device ►",  # Show a right arrow initially
            cursor="hand2",  # Change cursor on hover
            anchor="w",
            background="black",
            foreground="#00FF00"
            
        )

        self.toggle_device.grid(row=0, column=0, sticky="w")
        self.toggle_device.bind("<Button-1>", self.toggle_device_visibility)

        # Create a frame for the device content
        self.device_content_frame = ttk.Frame(self.content_frame)

        # Initially, the device content frame is hidden
        self.device_content_frame.grid(row=1, column=0, sticky="w")

        # Add content to the device content frame
        self.device_label = tk.Label(self.device_content_frame,background="black")
        #self.device_label.pack()

        # Create a button-like label for "Info ►"
        self.toggle_info = ttk.Label(
            self.content_frame,
            width=200,
            text="Info ►",  # Show a right arrow initially
            cursor="hand2",  # Change cursor on hover
            anchor="w",
            foreground="#00FF00"
        )

        self.toggle_info.grid(row=2, column=0, sticky="w")
        self.toggle_info.bind("<Button-1>", self.toggle_info_visibility)

        # Create a frame for the info content
        self.info_content_frame = ttk.Frame(self.content_frame)

        # Initially, the info content frame is hidden
        self.info_content_frame.grid(row=3, column=0, sticky="w")
        #--------------------------------------
        self.info_id_label = tk.Label(self.info_content_frame, text="ID:",compound=tk.LEFT)
        self.id_data_label = tk.Label(self.info_content_frame, foreground="#00CC00",background="white")
        #--------------------------------------
        self.info_ram_label = tk.Label(self.info_content_frame, text="RAM:")
        self.ram_data_label = tk.Label(self.info_content_frame, foreground="#00CC00")
        #--------------------------------------
        self.info_cpu_label = tk.Label(self.info_content_frame, text="CPU%:")
        self.cpu_data_label = tk.Label(self.info_content_frame, foreground="#00CC00")
        #--------------------------------------
        self.info_os_label = tk.Label(self.info_content_frame, text="OS:")
        self.os_data_label = tk.Label(self.info_content_frame, foreground="#00CC00",text="Android")
        #--------------------------------------
        self.info_arch_label = tk.Label(self.info_content_frame, text="ARCH:")
        self.arch_data_label = tk.Label(self.info_content_frame, foreground="#00CC00")
        # Add content to the info content frame
        

        # Update the scroll region of the Canvas
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def toggle_device_visibility(self, event):
        if self.device_state_var.get() == 1:  # Currently visible
            self.device_content_frame.grid_remove()  # Hide the device content frame
            self.toggle_device.config(text="Device ►")  # Show a right arrow
            self.device_state_var.set(0)  # Set state to "Hidden"
        else:

            self.device_content_frame.grid()  # Show the device content frame
            self.toggle_device.config(text="Device ▼")  # Show a down arrow
            self.device_state_var.set(1)  # Set state to "Visible"
            self.device_label.pack()

    def toggle_info_visibility(self, event):
        if self.info_state_var.get() == 1:  # Currently visible
            self.info_content_frame.grid_remove()  # Hide the info content frame
            self.toggle_info.config(text="Info ►")  # Show a right arrow
            self.info_state_var.set(0)  # Set state to "Hidden"
            self.info_id_label.grid_remove()
            self.info_ram_label.grid_remove()
            self.info_cpu_label.grid_remove()
            self.info_os_label.grid_remove()
            self.info_arch_label.grid_remove()




        else:
            
            self.info_content_frame.grid()  # Show the info content frame
            self.info_id_label = tk.Label(self.info_content_frame, text="ID:")
            self.id_data_label = tk.Label(self.info_content_frame, foreground="#00CC00")

            self.info_id_label.grid(column=0,row=0)
            self.id_data_label.grid(column=1,row=0)

            self.info_ram_label = tk.Label(self.info_content_frame, text="RAM:")
            self.ram_data_label = tk.Label(self.info_content_frame, foreground="#00CC00")
            self.info_ram_label.grid(column=0,row=1)
            self.ram_data_label.grid(column=1,row=1)
            
            self.info_cpu_label = tk.Label(self.info_content_frame, text="CPU%:")
            self.cpu_data_label = tk.Label(self.info_content_frame, foreground="#00CC00")
            self.info_cpu_label.grid(column=0,row=2)
            self.cpu_data_label.grid(column=1,row=2)

            self.info_os_label = tk.Label(self.info_content_frame, text="OS:")
            self.os_data_label = tk.Label(self.info_content_frame, foreground="#00CC00",text="Android")
            self.info_os_label.grid(column=0,row=3)
            self.os_data_label.grid(column=1,row=3)
            self.info_arch_label = tk.Label(self.info_content_frame, text="ARCH:")
            self.arch_data_label = tk.Label(self.info_content_frame, foreground="#00CC00")
            self.info_arch_label.grid(column=0,row=4)
            self.arch_data_label.grid(column=1,row=4)

            self.toggle_info.config(text="Info ▼")  # Show a down arrow
            self.info_state_var.set(1)  # Set state to "Visible"


class DeviceThread(threading.Thread):
    def __init__(self, label):
        super().__init__()
        self.start_x=0
        self.end_x=0
        self.end_time=0
        self.start_time=0
        self.label = label
        self.stop_event = threading.Event()
    def on_mouse_press(self,event):
    #global start_x, start_time
        x_scale_factor = Device.p_width / Device.width
        y_scale_factor = Device.p_height / Device.height
        self.start_x = int(event.x*x_scale_factor)
        self.start_y=int(event.y*y_scale_factor)
        adb_command = f'adb shell input tap {self.start_x} {self.start_y}'
        print(adb_command)
        subprocess.run(adb_command, shell=True)
        #print(event.x)
        #self.start_time = event.time



    def run(self):
        try:
            adb_command = [
             "adb", "shell", "screenrecord", "--output-format=h264","--size=200x400", "-"
]
            capture_process = subprocess.Popen(adb_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=Device.width * Device.height * 3)
            ffmpeg_process = subprocess.Popen(Device.ffmpeg_command, stdin=capture_process.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.label.bind("<ButtonPress-1>", self.on_mouse_press)
            #self.label.bind("<ButtonRelease-1>", self.on_mouse_release)
            while not self.stop_event.is_set():
                
                    #current_time = time.time()
                    #if current_time - Scheduler.previous_frame_time >= 0.1:
                    
                        Device.capture_device_screen(self.label,capture_process,ffmpeg_process)
                        time.sleep(0.01)
        except KeyboardInterrupt:
            pass

    def stop(self):
        self.stop_event.set()
class Device:
    connected=False
    #mutex = threading.Lock()
    ok=0
    adb_path = "adb"
    screenshot_dir =tempfile.mkdtemp()
    width=200
    height=400
    p_width=0
    p_height=0
    # FFmpeg command to decode the H.264 stream and output raw video frames
    ffmpeg_command = [
    "ffmpeg",
    "-loglevel", "error",
    "-f", "h264",   # Input format is H.264
    "-i", "-",       # Input from stdin
    "-f", "rawvideo",  # Output format is raw video
    "-framerate", "60",
    "-pix_fmt", "bgr24",  # Pixel format for output (BGR24)
    "-",
    ]
    
    def is_usb_device_connected():
        try:
            # Run the "adb devices" command and capture the output
            result = subprocess.run(["adb", "devices"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output = result.stdout

            # Split the output into lines
            lines = output.strip().split('\n')

            # Check if there are any connected devices (excluding the header)
            for line in lines[1:]:
                if "device" in line:
                    return True

            # If no connected devices are found, return False
            return False

        except Exception as e:
            pass
            # Handle any exceptions that may occur during the execution of the command
            ##print("Error:", e)
            return False
    def check(connection):
        subprocess.Popen([Device.adb_path, "connect", "DEVICE_IP:5555"])
    @staticmethod
    def capture_device_screen(label,capture_process,ffmpeg_process):

        last_frame = np.ones((Device.height, Device.width,3), dtype=np.uint8)*255
        first_frame_flag=0
        if Device.connected:
                    if Device.ok==0:
                        output = subprocess.check_output(['adb', 'shell', 'wm', 'size']).decode('utf-8')
                        Device.ok=1
            
                    
                    screen_size = output.strip().split(': ')[1]
                    Device.p_width, Device.p_height = map(int, screen_size.split('x'))
                    print(Device.p_width,Device.p_height)
       # start=time.Time()
        #end=time=Time
        while(True):
                #capture_process = subprocess.Popen(["adb", "exec-out", "screencap", "-p"], stdout=subprocess.PIPE)
                #with Device.mutex:
                #     pass
                start=time.time()
                frame_data_binary = ffmpeg_process.stdout.read(Device.width * Device.height * 3)
                #screen_data = capture_process.stdout.read(Device.width*Device.height*3)
                if not frame_data_binary:
                    break
                frame_array = np.frombuffer(frame_data_binary, dtype=np.uint8)
                #print(frame_array.shape)
                #print(screen_data.shape)
                if frame_array.shape == (Device.height * Device.width * 3,):
                    
                    frame = frame_array.reshape((Device.height, Device.width, 3))  # Assuming (height, width, channels)
                    last_frame=frame
                else:
                    frame = None
         
                if frame is not None and frame.shape[0] > 0 and frame.shape[1] > 0:
                    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                    image = Image.fromarray(frame)
                else:
                    last_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                    image=Image.fromarray(last_frame)
                
                photo = ImageTk.PhotoImage(image=image)
                end=time.time()
                print(end-start)
            # Update the label's image
                label.config(image=photo)
                label.image = photo
                
                #key = cv2.waitKey(1)
                #if key == ord("q"):
                    #exit()
                #label.after(10, Device.capture_device_screen(label=label))

    def release_device():
        cv2.destroyAllWindows()
        subprocess.Popen([Device.adb_path, "disconnect", "DEVICE_IP:5555"])


