
from tkinter import ttk
import tkinter as tk
import platform
from memory import Memory
from CreateProject.select_python import SelectPython
from tkinter import filedialog
from tkinter import messagebox
import os

class CreateProject():

    def handle_project_name(entry):
        os_name = platform.system()

        default_text="default_project"
        def on_entry_click(event):

            if entry.get() == Memory.project_name:
                entry.delete(0, "end")
                entry.config(fg='orange')  # Change text color to black

        def on_focus_out(event):
            if entry.get() == "":
                entry.insert(0, Memory.project_name)
                entry.config(fg='grey')  # Change text color to grey

        # Set the entry widget with default text and grey text color
        entry.config(fg='grey')  # Set text color to grey
        entry.insert(0, Memory.project_name)

        # Bind events to handle placeholder behavior
        entry.bind('<FocusIn>', on_entry_click)
        entry.bind('<FocusOut>', on_focus_out)
 
    
    def create_project_window(root,sl):
            
    
            label_alias = tk.Label(root, text="Python Version",padx=10)
            
            # Create a combobox to display Python versions
            python_versions = SelectPython.get_python_versions()
            version_combobox = ttk.Combobox(root, values=python_versions)
            
            version_combobox.set("Select a Python Version")

            # Bind a function to the combobox selection event
            def on_version_select(event):
                Memory.python_alias = version_combobox.get()
                
                
            version_combobox.bind("<<ComboboxSelected>>", on_version_select)

            label_project_name = tk.Label(root, text="Project Name",padx=10)
            
            entry_project_name = tk.Entry(root)
            CreateProject.handle_project_name(entry_project_name)

            custom_button_style = ttk.Style()
            custom_button_style.configure(
                "Custom.TButton",
                foreground="orange",  # Text color

    )
            # Create a button
            def browse_button():
                
                Memory.project_path = filedialog.askdirectory()
                #if Memory.project_path:
                    #messagebox.showinfo("Project Created", f"Project created in: {Memory.project_path}")
                    
            button_location = ttk.Button(root, text="Browse",style="Custom.TButton",command=browse_button)

            # Create horizontal frame for Cancel and Create buttons
            button_frame = tk.Frame(root)
            def close_button():
                root.destroy()
            button_cancel = ttk.Button(button_frame, text="Cancel",style="Custom.TButton",command=close_button)
            def create_button():
                Memory.python_alias=version_combobox.get()
                Memory.project_name=entry_project_name.get()
                
                CreateProject.create_project_architecture()
                sl.populate_solution_explorer()
                root.destroy()
                
                
            button_create = ttk.Button(button_frame, text="Create",style="Custom.TButton",command=create_button)
                

            # Pack widgets in the window
            label_alias.grid(column=0,row=0)
            version_combobox.grid(column=1,row=0)

            label_project_name.grid(column=0,row=1)
            entry_project_name.grid(column=1,row=1)

            button_location.grid(column=2,row=1,padx=5)

            button_frame.grid(column=0,row=2)
            button_cancel.grid(column=3,row=3,pady=30,padx=10)
            button_create.grid(column=4,row=3,pady=30,padx=10)
        
    def create_project_architecture():
        # Create the project directory
        Memory.project_path = os.path.join(Memory.project_path, Memory.project_name)
        os.makedirs(Memory.project_path)

        subfolders = ['src', 'build', 'assets', 'android', 'ios']

        # Create "main.py" and "main.kv" in the root directory
        main_path = os.path.join(Memory.project_path, "main.py")
        main_kv_path = os.path.join(Memory.project_path, "main.kv")
        open(main_path, 'w').close()
        open(main_kv_path, 'w').close()

        for folder in subfolders:
            folder_path = os.path.join(Memory.project_path, folder)
            os.makedirs(folder_path)

            if folder in ['android', 'ios']:
                # Create an empty "requirements.txt" file in the folder
                requirements_path = os.path.join(folder_path, "requirements.txt")
                open(requirements_path, 'w').close()

                if folder == 'android':
                    # Create an empty "build.spec" file in the android folder
                    build_spec_path = os.path.join(folder_path, "build.spec")
                    open(build_spec_path, 'w').close()

                if folder == 'ios':
                    # Create an empty "info.plist" file in the ios folder
                    info_plist_path = os.path.join(folder_path, "info.plist")
                    open(info_plist_path, 'w').close()
            