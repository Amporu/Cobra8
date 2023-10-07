from tkinter import ttk
import tkinter as tk
import subprocess
import time

import threading
class MonitorLabel:
    messages=[]
    levels=[]
    def __init__(self, root):
        self.frame = ttk.Frame(root)
        
        self.frame.pack()

        self.text_widget = tk.Text(self.frame, wrap=tk.WORD)
        self.frame1=tk.Frame(self.frame)
        self.text_widget.pack(fill="both",expand=True)
        
        
        self.scrollbar = ttk.Scrollbar(self.frame, command=self.text_widget.yview)
    def start_monitor(self):
        
        #logcat_process = subprocess.Popen(['adb', 'logcat', '*:E'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)        
        def update_log(text):
            while(True):
                if len(MonitorLabel.messages)>0:
                    for mesage in MonitorLabel.messages:
                        text.insert(tk.END, mesage)
                        MonitorLabel.messages.remove(mesage)
                        text.see(tk.END)
                        time.sleep(1)
            
        
        logcat_thread = threading.Thread(target=update_log,args=(self.text_widget,))
        logcat_thread.daemon = True
        logcat_thread.start()
        #self.scrollbar.pack(side="right", fill="y")
        #self.text_widget.config(yscrollcommand=self.scrollbar.set)

