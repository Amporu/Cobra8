import tkinter as tk
class Menu:
    def __init__(self,editor,solution,root):
        self.editor=editor
        self.solution=solution
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        # Create a "File" menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Create Project",command=solution.create_project)
        file_menu.add_command(label="Open Folder", command=solution.open_folder)
        file_menu.add_command(label="Open File", command=editor.open_file)
        file_menu.add_command(label="Exit", command=root.quit)
        run_menu = tk.Menu(menubar, tearoff=0)
        run_menu.add_command(label="build apk", command=editor.open_file)

        run_menu.add_command(label="Build & Run", command=root.quit)
        project_menu=tk.Menu(menubar,tearoff=0)
        project_menu.add_command(label="Project Settings", command=editor.open_file)
        project_menu.add_command(label="Build Settings", command=editor.open_file)
        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Project",menu=project_menu)
        menubar.add_cascade(label="Run",menu=run_menu)
        