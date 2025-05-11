import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import pandas as pd
from datetime import datetime

# GUI window setup
root = tk.Tk()
root.title("Face Recognition Attendance System")
root.geometry("400x400")

# Function to add a new face
def add_face():
    name = name_entry.get()
    if not name:
        messagebox.showerror("Error", "Please enter a name.")
        return
    env = os.environ.copy()
    env["USER_NAME"] = name
    subprocess.run(
        ["python", "C:\\Users\\ashay\\OneDrive\\Desktop\\Face Recognition Attendance System\\add_faces.py"],
        env=env,
        shell=True
    )

# Function to take attendance
def take_attendance():
    subprocess.run(
        ["python", "C:\\Users\\ashay\\OneDrive\\Desktop\\Face Recognition Attendance System\\test.py"],
        shell=True
    )

# Function to view today's attendance
def view_attendance():
    today = datetime.now().strftime("%d-%m-%Y")
    
    # Build absolute path to the attendance file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    attendance_dir = os.path.join(base_dir, "Attendance")
    file_path = os.path.join(attendance_dir, f"Attendance_{today}.csv")
    
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        
        # Create a new popup window to display the attendance
        top = tk.Toplevel(root)
        top.title(f"Attendance for {today}")
        text = tk.Text(top, wrap='none')
        text.pack(expand=1, fill='both')
        text.insert(tk.END, df.to_string(index=False))
    else:
        messagebox.showinfo("No Data", f"No attendance file found for today ({today}).")

# Exit the app
def quit_app():
    root.destroy()

# GUI layout
tk.Label(root, text="Enter Name for Registration").pack(pady=5)
name_entry = tk.Entry(root)
name_entry.pack(pady=5)

tk.Button(root, text="Add New Face", command=add_face, width=30).pack(pady=10)
tk.Button(root, text="Take Attendance", command=take_attendance, width=30).pack(pady=10)
tk.Button(root, text="View Today's Attendance", command=view_attendance, width=30).pack(pady=10)
tk.Button(root, text="Exit", command=quit_app, width=30).pack(pady=10)

# Run the app
root.mainloop()
