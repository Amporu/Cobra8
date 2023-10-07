import os
from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from menu import Menu
from create_project import CreateProject
from memory import Memory
class SolutionExplorer:
    def __init__(self,main_frame,editor,root):
        self.solution_explorer_pane = ttk.Frame(main_frame)
        self.editor=editor
        self.root=root
        #create_file_button = ttk.Button(self.solution_explorer_pane, text="Create File", command=editor.open_file)
        main_frame.add(self.solution_explorer_pane)
        self.solution_tree = ttk.Treeview(self.solution_explorer_pane, columns=("Name"))
        self.solution_tree.column("#0", width=0)
        self.solution_tree.pack(fill="both", expand=True)
        self.solution_tree.bind("<Double-1>", self.on_solution_tree_double_click)  # Bind double-click event
        #self.solution_tree.bind("<Button-1>", self.on_solution_tree_click)  # Bind single-click event
        Menu(editor,self,root)
    
    
    def on_solution_tree_double_click(self,event):
        
        try:
            item = self.solution_tree.selection()[0]
            selected_item_text = self.solution_tree.item(item, "values")[0]
        
            self.solution_tree.tag_configure("folder", foreground="green")
            self.solution_tree.tag_configure("python_file", foreground="orange")
            self.solution_tree.tag_configure("kivy_file",foreground="orange")
            self.solution_tree.tag_configure("..", foreground="red")
            # Handle the "Go Up" item
            if selected_item_text == "..":
                # Navigate to the parent directory
                Memory.project_path = os.path.dirname(Memory.project_path)
                self.populate_solution_explorer()
            else:
                file_path = os.path.join(Memory.project_path, selected_item_text)
                if os.path.isdir(file_path):
                    Memory.project_path = file_path
                    self.populate_solution_explorer()
                elif os.path.isfile(file_path):
                    self.editor.open_text_editor(file_path)
        except:
            pass
    def populate_solution_explorer(self):
        # Clear the solution explorer
        self.solution_tree.delete(*self.solution_tree.get_children())
        self.solution_tree.insert("", "end", values=("..",), tags=("..",))
        if not os.path.exists(Memory.project_path):
            return
        self.solution_tree.tag_configure("folder", foreground="green")
        self.solution_tree.tag_configure("ios_folder", foreground="#00FF00")
        self.solution_tree.tag_configure("android_folder", foreground="white",background="green")
        self.solution_tree.tag_configure("assets_folder", foreground="white",background="orange")
        self.solution_tree.tag_configure("build_folder", foreground="white",background="blue")
        self.solution_tree.tag_configure("python_file", foreground="yellow")
        self.solution_tree.tag_configure("kivy_file",foreground="orange")
        self.solution_tree.tag_configure("..", foreground="green")
        
        # Lists to hold folders and files
        folders = []
        python_files = []
        kivy_files = []
        other_files = []
        
        # Add a "Go Up" item to navigate to the parent directory
        for item in os.listdir(Memory.project_path):
            item_path = os.path.join(Memory.project_path, item)
            if os.path.isdir(item_path):
                folders.append(item)
            elif item.endswith(".py"):
                python_files.append(item)
            elif item.endswith(".kv"):
                kivy_files.append(item)
            else:
                other_files.append(item)

        # Sort the lists
        folders.sort()
        python_files.sort()
        kivy_files.sort()
        other_files.sort()

        # Insert folders and files into the solution explorer
        for item in folders:
            if item=="ios":
                self.solution_tree.insert("", "end", values=(item,), tags=("ios_folder",))
            elif item=="android":
                self.solution_tree.insert("", "end", values=(item,), tags=("ios_folder",))
            elif item=="build":
                self.solution_tree.insert("", "end", values=(item,), tags=("ios_folder",))
            elif item=="assets":
                self.solution_tree.insert("", "end", values=(item,), tags=("ios_folder",))
            else:
                self.solution_tree.insert("", "end", values=(item,), tags=("ios_folder",))
        for item in python_files:
            self.solution_tree.insert("", "end", values=(item,), tags=("python_file",))
        for item in kivy_files:
            self.solution_tree.insert("", "end", values=(item,), tags=("kivy_file",))
        for item in other_files:
            self.solution_tree.insert("", "end", values=(item,))
        
    def create_project(self):
        
        cp=tk.Tk()
        CreateProject.create_project_window(cp,self)
        
 
    
    def open_folder(self):

        Memory.project_path = filedialog.askdirectory()
        #root.attributes("-topmost", True)
        if Memory.project_path:
            self.populate_solution_explorer()