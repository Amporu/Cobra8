import tkinter as tk

def toggle_permission(event):
    permission_var.set(not permission_var.get())
    update_toggle_pill()

def update_toggle_pill():
    color = "green" if permission_var.get() else "red"
    canvas.itemconfig(pill, fill=color)

# Create a Tkinter window
window = tk.Tk()
window.title("Elliptical Toggle Pill")

# Create a BooleanVar to track the permission state
permission_var = tk.BooleanVar()
permission_var.set(False)  # Initial state: Denied

# Create a canvas for the toggle pill
canvas = tk.Canvas(window, width=100, height=50, highlightthickness=0)
canvas.pack()

# Create an elliptical-shaped toggle pill
pill = canvas.create_oval(10, 10, 90, 40, fill="red")

# Bind a click event to toggle the permission
canvas.bind("<Button-1>", toggle_permission)

# Start the Tkinter event loop
window.mainloop()