import tkinter as tk
from tkinter import ttk
import os

def populate_tree(tree, node):
    path = tree.item(node, 'text')
    tree.delete(*tree.get_children(node))
    try:
        with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_dir():
                    child = tree.insert(node, 'end', text=entry.path, open= True)
                    populate_tree(tree, child)
                else:
                    tree.insert(node, 'end', text=entry.name)
    except FileNotFoundError:
        return

def open_folder(event):
    item = tree.selection()
    tree.tag_configure("folder", foreground="green")
    tree.tag_configure("ios_folder", foreground="#00FF00")
    tree.tag_configure("android_folder", foreground="white",background="green")
    tree.tag_configure("assets_folder", foreground="white",background="orange")
    tree.tag_configure("build_folder", foreground="white",background="blue")
    tree.tag_configure("python_file", foreground="yellow")
    tree.tag_configure("kivy_file",foreground="orange")
    tree.tag_configure("..", foreground="green")
    if item:
        node = item[0]
        folders = []
        python_files = []
        kivy_files = []
        other_files = []
        for item in os.listdir(item):
            item_path = os.path.join(item, item)
            if os.path.isdir(item_path):
                folders.append(item)
            elif item.endswith(".py"):
                python_files.append(item)
            elif item.endswith(".kv"):
                kivy_files.append(item)
            else:
                other_files.append(item)
        folders.sort()
        python_files.sort()
        kivy_files.sort()
        other_files.sort()

        # Insert folders and files into the solution explorer
        for item in folders:
            if item=="ios":
                tree.insert("", node, values=(item,), tags=("ios_folder",))
            elif item=="android":
                tree.insert("", node, values=(item,), tags=("ios_folder",))
            elif item=="build":
                tree.insert("", node, values=(item,), tags=("ios_folder",))
            elif item=="assets":
                tree.insert("", node, values=(item,), tags=("ios_folder",))
            else:
                tree.insert("", node, values=(item,), tags=("ios_folder",))
        for item in python_files:
            tree.insert("", node, values=(item,), tags=("python_file",))
        for item in kivy_files:
            tree.insert("", "end", values=(item,), tags=("kivy_file",))
        for item in other_files:
            tree.insert("", "end", values=(item,))
        if not tree.get_children(node):
            populate_tree(tree, node)
        tree.item(node, open=not tree.item(node, 'open'))

# Create the main window
root = tk.Tk()
root.title("Solution Explorer")

# Create a Treeview widget to display the directory structure
tree = ttk.Treeview(root)
tree.pack(fill=tk.BOTH, expand=True)

# Add a root item for the current directory
current_path = os.getcwd()
root_item = tree.insert('', 'end', text=current_path, open=True)

# Populate the Treeview with the contents of the root directory
populate_tree(tree, root_item)

# Bind single-click event to open folders and display files
tree.bind("<Button-1>", open_folder)

# Create a scrollbar for the Treeview
scrollbar = ttk.Scrollbar(tree)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=tree.yview)

# Run the Tkinter main loop
root.mainloop()
