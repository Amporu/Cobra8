from tkinter import ttk
import tkinter as tk
import threading
import subprocess
import time
class LogcatLabel:
    def __init__(self, root):
        self.frame = ttk.Frame(root)
        self.frame.pack(fill="both", expand=True)
        self.text_widget = tk.Text(self.frame, wrap=tk.WORD)
        self.text_widget.pack(fill="both", expand=True)
        self.scrollbar = ttk.Scrollbar(self.frame, command=self.text_widget.yview)
    def start_logcat(self):
        
        logcat_process = subprocess.Popen(['adb', 'logcat', '*:E'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)        
        def update_log(text):
            try:
                for line in logcat_process.stdout:
                    text.insert(tk.END, line)
                    text.see(tk.END)
                    time.sleep(1)
            except:
                pass
        
        logcat_thread = threading.Thread(target=update_log,args=(self.text_widget,))
        logcat_thread.daemon = True
        logcat_thread.start()
        #self.scrollbar.pack(side="right", fill="y")
        #self.text_widget.config(yscrollcommand=self.scrollbar.set)
class LogcatThread(threading.Thread):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
        self.stop_event = threading.Event()

    def run(self):
        try:
            adb_process = subprocess.Popen(
                ["adb", "logcat"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            while not self.stop_event.is_set():
                line = adb_process.stdout.readline()
                if not line:
                    break
                self.text_widget.insert(tk.END, line)
                self.text_widget.see(tk.END)

            adb_process.terminate()
            adb_process.wait()

        except subprocess.CalledProcessError as e:
            print("Error running adb logcat:", e)
            pass

    def stop(self):
        self.stop_event.set()
class ScrollableFrame(ttk.Frame):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        canvas = tk.Canvas(self)
        canvas.pack(side="left", fill="both", expand=True)
        ttk.Frame.__init__(self, canvas)
        canvas.create_window((0, 0), window=self, anchor="nw")
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", self.set_scrollregion)

    def set_scrollregion(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
