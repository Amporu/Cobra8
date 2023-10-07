import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import time
import re
import keyword
from tkinter.scrolledtext import ScrolledText
import inspect
import builtins
import threading
import subprocess
#builtin_functions = [name for name in dir(builtins) if callable(getattr(builtins, name))]
#builtin_classes = [name for name in dir(builtins) if isinstance(getattr(builtins, name), type)]
#builtin_function_pattern = r'\b(' + '|'.join(re.escape(name) for name in builtin_functions) + r')\b'

# Compile the regular expression
#builtin_function_regex = re.compile(builtin_function_pattern)


class Editor:
    error_flag=False
    error_line=-1
    start_error=""
    end_error=""
    def __init__(self, main_pane, root):
        self.editor_notebook = ttk.Notebook(main_pane, width=800,height=650)
        self.root = root
        self.strings=[]
        self.colors=[]

            # Apply the custom style to the scrollbar
        
    def close_tab(self):
        selected_tab = self.editor_notebook.select()
        if selected_tab:
            self.editor_notebook.forget(selected_tab)

    def delete_tab(self):
        selected_tab = self.editor_notebook.index(self.editor_notebook.select())
        self.editor_notebook.forget(selected_tab)

    def highlight_nested(self,event=None):
        code = self.text.get("1.0", "end")
        if len(self.strings)!=0:
            for i, string in enumerate(self.strings):
                self.highlight_string(string, self.colors[i])
    def highlight_string(self, string, tag):
        start = "1.0"
        while True:
            start = self.text.search(rf'\y{re.escape(string)}\y', start, stopindex=tk.END, regexp=True)
            if not start:
                break
            end = f"{start}+{len(string)}c"
            self.text.tag_add(tag, start, end)
            start = end
    def clear_error_highlight(self):
        self.text.tag_remove("error", "1.0", "end")
    def highlight_error_line(self, line_number):
        start_index = f"{line_number}.0"
        end_index = f"{line_number + 1}.0"
        self.text.tag_configure("error", background="red")  # Customize the error highlight color here
        self.text.tag_add("error", start_index, end_index)
    def compile_code(self, event=None):
        code = self.text.get("1.0", "end-1c")  # Get the text from the Text widget
        try:
            Editor.error_flag=False
            # Clear any previous error highlighting
            self.text.tag_remove("error", "1.0", "end")
            #self.line_number_widget.tag_remove("error_count", "1.0", "end")
            compiled_code = compile(code, '<string>', 'exec')
            exec(compiled_code)
            #command = ["python", self.file]
            
            # Code executed successfully
        except SyntaxError as e:
            # Display the error message
            error_message = str(e)
           # print(1)

            # Use regular expressions to extract the line number from the error message
            line_match = re.search(r"line (\d+)", error_message)
            #print(2)
            if line_match:
                error_line = int(line_match.group(1))
            else:
                error_line = 1  # Default to line 1 if line number cannot be extracted

            # Calculate the start and end indices of the error line
            start_index = f"{error_line}.0"
            end_index = f"{error_line}.end"
            Editor.start_error=start_index
            Editor.end_error=end_index
            Editor.error_flag=True
            #print(3)
            # Configure a red underline tag for the error line
            self.text.tag_configure("error", underline=True, foreground="red")
            #self.line_number_widget.tag_configure("error_count",  foreground="green")
            self.line_number_widget.tag_add("error_count",start_index,end_index)
            # Apply the "error" tag to the error line
            self.text.tag_add("error", start_index, end_index)# the self.line_number_widget doesn't get the tag (colored)

    


        

    def open_text_editor(self, file_path):
        file_name = os.path.basename(file_path)
        tab = ttk.Frame(self.editor_notebook,width=800)
        tab.pack()
        self.file=file_path
        popup_menu = tk.Menu(self.root, tearoff=0)
        popup_menu.add_command(label="Delete Tab", command=self.delete_tab)
        #close_button = ttk.Button(tab, text="x", command=self.close_tab)
        #close_button.grid(column=0, row=0)

        def show_popup(event):
            popup_menu.post(event.x_root, event.y_root)

        self.editor_notebook.bind("<Button-2>", show_popup)

        

        self.editor_notebook.add(tab, text=file_name,underline=1)

        text_frame = tk.Frame(tab)
        text_frame.pack()
        self.line_number_widget = tk.Text(text_frame, width=4, wrap=tk.WORD)
        self.line_number_widget.pack(fill=tk.Y, side=tk.LEFT)

        # Configure line number widget
        #self.line_number_widget.tag_configure("error_line",  foreground="red")
        self.line_number_widget.tag_configure("center", justify="center")
        self.line_number_widget.config(state=tk.DISABLED)

        # Create the main Text widget for editing
        #self.text = ScrolledText(text_frame, wrap=tk.WORD)
       # self.text.pack(fill=tk.BOTH, expand=True)
        self.text = tk.Text(text_frame, wrap=tk.WORD,width=800,height=1000)
        #self.text.configure(slidercolor="black")
        #self.text.vsb.configure(style="Custom.Vertical.TScrollbar")
        self.text.pack(fill=tk.BOTH, expand=True)
        
        # Syntax highlighting
        self.line_number_widget.tag_configure("error_count", background="red",foreground="white")
        self.text.tag_configure("keyword", foreground="orange")
        self.text.tag_configure("string", foreground="#a9fa9b")
        self.text.tag_configure("comment", foreground="gray")
        self.text.tag_configure("number", foreground="lightblue")
        self.text.tag_configure("class", foreground="#f89bfa")
        self.text.tag_configure("function", foreground="#9bacfa")
        self.text.tag_configure("variable", foreground="#D0AA00")
        self.text.tag_configure("operator", foreground="#ff0DE0")
        self.text.tag_configure("paranteze", foreground="#fdff91")
        self.text.tag_configure("import", foreground="#ff9191")
        self.text.tag_configure("as",foreground="#88c28c")
        
        #self.text.bind("<KeyRelease>", self.highlight_nested)
        def save(event=None):
            #time.sleep(1)
            if file_path:
                with open(file_path, "w") as file:
                    file.write(self.text.get("1.0", tk.END))
                tab.modified = False
                self.update_tab_title(tab)

        
        self.text.bind("<KeyRelease>", self.update_line_numbers_and_highlight)
        #self.text.bind("<KeyRelease>", mark_as_modified)
        self.text.bind("<space>", save)
        self.text.bind("<Return>", self.compile_code)
        
        
        #self.text.bind("<Return>", self.compile_code)
       # self.execute_code()
        
        
        save_button = ttk.Button(text_frame, text="Save", command=save)
        save_button.pack()

        with open(file_path, "r") as file:
            content = file.read()
            self.text.insert(tk.END, content)

        tab.modified = False
        self.update_tab_title(tab)
        #s#elf.highlight_python_syntax(self.text)

    def update_tab_title(self, tab):
        tab_title = self.editor_notebook.tab(tab, "text")
        if tab.modified:
            if not tab_title.endswith("*"):
                self.editor_notebook.tab(tab, text=tab_title + "*")
        else:
            if tab_title.endswith("*"):
                self.editor_notebook.tab(tab, text=tab_title[:-1])

    def change_selected_tab_text_color(self, new_color):
        style = ttk.Style()
        style.map("TNotebook.Tab", foreground=[("selected", new_color)])

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.open_text_editor(file_path)
    def update_line_numbers_and_highlight(self, event=None):
        # Update line numbers
        self.update_line_numbers()
        #print(self.strings)
        #print(self.colors)
        # Clear existing tags
        self.text.tag_remove("keyword", "1.0", tk.END)
        self.text.tag_remove("string", "1.0", tk.END)
        self.text.tag_remove("comment", "1.0", tk.END)
        self.text.tag_remove("number", "1.0", tk.END)
        self.text.tag_remove("function", "1.0", tk.END)
        self.text.tag_remove("class", "1.0", tk.END)
        self.text.tag_remove("variable", "1.0", tk.END)
        self.text.tag_remove("operator", "1.0", tk.END)
        self.text.tag_remove("import", "1.0", tk.END)
        self.text.tag_remove("as", "1.0", tk.END)

        code = self.text.get("1.0", tk.END)
        lines = code.split("\n")

        # Initialize stack to track nested classes and functions
        stack = []
        self.strings.append("self")
        self.strings.append("super")
        self.colors.append("class")
        self.colors.append("class")
        for i, line in enumerate(lines):
            
            # Find single-quoted strings
            string_start = line.find("'")
            search_start = 0
            while True:
                # Find the next single-quoted string
                string_start = line.find("'", search_start)
                if string_start != -1:
                    string_end = line[string_start + 1:].find("'")
                    if string_end != -1:
                        # Adjust indices for the substring
                        string_start += 1
                        string_end += string_start + 1
                        self.text.tag_add("string", f"{i + 1}.{string_start-1}", f"{i + 1}.{string_end}")

                        # Update the search start position to continue searching
                        search_start = string_end + 1
                    else:
                        # If the string isn't closed on the same line, exit the loop
                        break
                else:
                    # No more single-quoted strings found on this line, exit the loop
                    break
            search_start = 0
            while True:
                # Find the next single-quoted string
                string_start = line.find('"', search_start)
                if string_start != -1:
                    string_end = line[string_start + 1:].find('"')
                    if string_end != -1:
                        # Adjust indices for the substring
                        string_start += 1
                        string_end += string_start + 1
                        self.text.tag_add("string", f"{i + 1}.{string_start-1}", f"{i + 1}.{string_end}")

                        # Update the search start position to continue searching
                        search_start = string_end + 1
                    else:
                        # If the string isn't closed on the same line, exit the loop
                        break
                else:
                    # No more single-quoted strings found on this line, exit the loop
                    break
            # Split the line into words
            tokens = re.findall(r'\b\w+\b|[-=+*/^&|<>]', line)
            for token in tokens:
                start = f"{i + 1}.{line.index(token)}"
                end = f"{i + 1}.{line.index(token) + len(token)}"

                # Check if the token is a keyword
                if token in keyword.kwlist:
                    self.text.tag_add("keyword", start, end)
            search_start = 0

            while True:
                # Define a list of operators to search for
                operators = ["=", "+", "-", "*", "/", "^", "&", "|", "<", ">", ":"]

                # Find the next operator
                next_operator = None
                for operator in operators:
                    operator_start = line.find(operator, search_start)
                    if operator_start != -1:
                        if next_operator is None or operator_start < next_operator[1]:
                            next_operator = (operator, operator_start)

                if next_operator is not None:
                    operator, operator_start = next_operator

                    # Calculate the operator's end position
                    operator_end = operator_start + len(operator)

                    self.text.tag_add("operator", f"{i + 1}.{operator_start}", f"{i + 1}.{operator_end}")

                    # Update the search start position to continue searching
                    search_start = operator_end
                else:
                    # No more operators found on this line, exit the loop
                    break
                    

            search_start = 0

            while True:
                # Define a list of operators to search for
                operators = ["[", "]", "{", "}", "(", ")"]

                # Find the next operator
                next_operator = None
                for operator in operators:
                    operator_start = line.find(operator, search_start)
                    if operator_start != -1:
                        if next_operator is None or operator_start < next_operator[1]:
                            next_operator = (operator, operator_start)

                if next_operator is not None:
                    operator, operator_start = next_operator

                    # Calculate the operator's end position
                    operator_end = operator_start + len(operator)

                    self.text.tag_add("paranteze", f"{i + 1}.{operator_start}", f"{i + 1}.{operator_end}")

                    # Update the search start position to continue searching
                    search_start = operator_end
                else:
                    # No more operators found on this line, exit the loop
                    break

                    

            

            # Handle nested class and function definitions
            if re.match(r'^\s*class\s+[A-Za-z_]\w*:', line) or re.match(r'^\s*class\s+[A-Za-z_]\w*\(.*\):', line):
                stack.append(("class", i))
                if re.match(r'^\s*class\s+[A-Za-z_]\w*:', line):
                    class_name = re.match(r'^\s*class\s+[A-Za-z_]\w*:', line).group(0)
                    id_end = class_name.find(":")
                    id_start = class_name.find("class ")
                    self.text.tag_add("class", f"{i + 1}.{id_start + 6}", f"{i + 1}.{id_end}")
                    if class_name[id_start+6:id_end] not in self.strings:
                        self.strings.append(class_name[id_start+6:id_end])
                        self.colors.append("class")
                else:
                    class_name = re.match(r'^\s*class\s+[A-Za-z_]\w*\(.*\):', line).group(0)
                    id_start = class_name.find("class ")
                    id_end = class_name.find("(")
                    self.text.tag_add("class", f"{i + 1}.{id_start + 6}", f"{i + 1}.{id_end}")
                    if class_name[id_start+6:id_end] not in self.strings:
                        self.strings.append(class_name[id_start+6:id_end])
                        self.colors.append("class")
            if re.match(r'^\s*def\s+[A-Za-z_]', line):
                function_name = re.match(r'^\s*def\s+[A-Za-z_]\w*\(.*\):', line).group(0)
                stack.append(("function", i))
                id_start = function_name.find("def ") + 4
                id_end = function_name.find("(")
                self.text.tag_add("function", f"{i + 1}.{id_start}", f"{i + 1}.{id_end}")
                if function_name[id_start:id_end] not in self.strings:
                    self.strings.append(function_name[id_start:id_end])
                    self.colors.append("function")
            if re.match(r'^\s*import\s+([A-Za-z0-9_.]+)',line):
                match=re.match(r'^\s*import\s+([A-Za-z0-9_.]+)',line)
                if match:
                    package_name = match.group(1)
                    id_start = line.find(package_name)
                    id_end = id_start + len(package_name)
                    self.text.tag_add("import", f"{i + 1}.{id_start}", f"{i + 1}.{id_end}")
                    if package_name not in self.strings:
                        self.strings.append(package_name)
                        self.colors.append("import")
            match = re.search(r'\bas\s+([A-Za-z_]+)', line)
            if match:
                package_nicknameeee = match.group(1)
                id_start = line.find("as") + 3  # Find the position after "as"
                id_end = id_start + len(package_nicknameeee)
                self.text.tag_add("import", f"{i + 1}.{id_start}", f"{i + 1}.{id_end}")
                if package_nicknameeee not in self.strings:
                    self.strings.append(package_nicknameeee)
                    self.colors.append("import")
            match = re.match(r'^\s*from\s+([A-Za-z_][A-Za-z0-9_.]*)\s+import\s+([A-Za-z_][A-Za-z0-9_.]*)', line)
            if match:
                imported_module = match.group(1)
                imported_name = match.group(2)
                
                # Highlight the imported module (x)
                id_start_module = line.find(imported_module)
                id_end_module = id_start_module + len(imported_module)
                self.text.tag_add("import", f"{i + 1}.{id_start_module}", f"{i + 1}.{id_end_module}")
                
                # Highlight the imported name (y)
                id_start_name = line.find(imported_name)
                id_end_name = id_start_name + len(imported_name)
                self.text.tag_add("import", f"{i + 1}.{id_start_name}", f"{i + 1}.{id_end_name}")
                
                if imported_module not in self.strings:
                    self.strings.append(imported_module)
                    self.colors.append("import")
                if imported_name not in self.strings:
                    self.strings.append(imported_name)
                    self.colors.append("import")
            
            # Check for comments
            comment_start = line.find("#")
            if comment_start != -1:
                self.text.tag_add("comment", f"{i + 1}.{comment_start}", f"{i + 1}.end")
            # Check for the end of nested class and function definitions
            if re.match(r'^\s*\w+\s+=\s+[A-Za-z_]\w*\(.*\)', line) or re.match(r'^\s*\w+\s+=\s+class\s+[A-Za-z_]\w*:', line):
                stack.pop()
            if len(self.strings)!=0:
                for i, string in enumerate(self.strings):
                    self.highlight_string(string, self.colors[i])
            
            
        
        self.strings.clear()
        self.colors.clear()
    def update_line_numbers(self):
        
        line_count = int(self.text.index(tk.END).split('.')[0])
        line_number_text = '\n'.join(str(i)+"        " for i in range(1, line_count))
        #self.line_number_widget.tag_add("comment", "1.0", str(line_count) + ".end")
        self.line_number_widget.config(state=tk.NORMAL)
        self.line_number_widget.delete(1.0, tk.END)
        self.line_number_widget.insert(tk.END, line_number_text)
        self.line_number_widget.config(state=tk.DISABLED)
        if Editor.error_flag:
            self.line_number_widget.tag_add("error_count",Editor.start_error,Editor.end_error)