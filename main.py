import json
import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import time
import subprocess
import threading
import datetime
import os


CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")


def load_config():
    with open(CONFIG_PATH, "r") as file:
        return json.load(file)


def save_config(data):
    with open(CONFIG_PATH, "w") as file:
        json.dump(data, file, indent=4)


def update_config():
    config["meeting_id"] = meeting_id_var.get()
    config["meeting_passcode"] = meeting_passcode_var.get()
    config["zoom_path"] = zoom_path_var.get()
    config["schedule"]["time"] = schedule_time_var.get()
    config["schedule"]["days"] = schedule_days_var.get().split(",")
    config["show_guide"] = show_guide_var.get()
    config["record_duration"] = int(record_duration_var.get())
   
    config["coordinates"]["join_a_meeting_x"] = int(join_a_meeting_x_var.get())
    config["coordinates"]["join_a_meeting_y"] = int(join_a_meeting_y_var.get())
   
    save_config(config)
    messagebox.showinfo("Success", "Settings updated successfully!")


def locate_join_button():
    def capture_position():
        messagebox.showinfo("Locate Join Button", "Move your mouse over the 'Join a Meeting' button. Capturing in 5 seconds...")
        time.sleep(5)
        x, y = pyautogui.position()
        join_a_meeting_x_var.set(str(x))
        join_a_meeting_y_var.set(str(y))
        update_config()
        messagebox.showinfo("Success", f"Coordinates saved! X: {x}, Y: {y}")
   
    threading.Thread(target=capture_position, daemon=True).start()


def log_status(message):
    status_box.insert(tk.END, message + "\n")
    status_box.yview(tk.END)


def join_meeting():
    log_status("Starting Zoom...")
    subprocess.Popen(config["zoom_path"], shell=True)
    time.sleep(5)
   
    log_status("Clicking 'Join a Meeting' button...")
    pyautogui.click(config["coordinates"]["join_a_meeting_x"], config["coordinates"]["join_a_meeting_y"])
    time.sleep(2)
   
    log_status("Typing Meeting ID...")
    pyautogui.write(config["meeting_id"])
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(2)
   
    log_status("Typing Passcode...")
    pyautogui.write(config["meeting_passcode"])
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(2)
   
    log_status("Confirming Join...")
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(2)
   
    log_status("Meeting Joined! Starting recording in 5 seconds...")
    time.sleep(5)
    pyautogui.hotkey('alt', 'f9')
    log_status(f"Recording started! Duration: {config['record_duration']} seconds")
   
    time.sleep(config["record_duration"])
    pyautogui.hotkey('alt', 'f9')
    log_status("Recording stopped!")


def scheduled_meeting():
    while True:
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")
        current_day = now.strftime("%A")
        log_status(f"Checking schedule: {current_day}, {current_time}")
       
        if current_time == config["schedule"]["time"] and current_day in config["schedule"]["days"]:
            log_status(f"Scheduled time reached ({current_time} on {current_day}). Joining meeting...")
            join_meeting()
       
        time.sleep(5)  # Check every 5 seconds


def start_scheduled_bot():
    log_status("Bot is now monitoring scheduled meeting times...")
    threading.Thread(target=scheduled_meeting, daemon=True).start()


def start_manual_meeting():
    log_status("Manually joining meeting now...")
    threading.Thread(target=join_meeting, daemon=True).start()


config = load_config()


root = tk.Tk()
root.title("ZoomRec 1.2.0")
root.geometry("600x600")


notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")


status_frame = ttk.Frame(notebook)
notebook.add(status_frame, text="Status")


status_box = tk.Text(status_frame, height=15, wrap=tk.WORD)
status_box.pack(expand=True, fill="both", padx=10, pady=10)


default_status = "Bot status will appear here..."
log_status(default_status)


settings_frame = ttk.Frame(notebook)
notebook.add(settings_frame, text="Settings")


meeting_id_var = tk.StringVar(value=config["meeting_id"])
meeting_passcode_var = tk.StringVar(value=config["meeting_passcode"])
zoom_path_var = tk.StringVar(value=config["zoom_path"])
schedule_time_var = tk.StringVar(value=config["schedule"]["time"])
schedule_days_var = tk.StringVar(value=",".join(config["schedule"]["days"]))
show_guide_var = tk.BooleanVar(value=config["show_guide"])
record_duration_var = tk.StringVar(value=str(config.get("record_duration", 600)))
join_a_meeting_x_var = tk.StringVar(value=str(config["coordinates"]["join_a_meeting_x"]))
join_a_meeting_y_var = tk.StringVar(value=str(config["coordinates"]["join_a_meeting_y"]))


fields = [
    ("Meeting ID:", meeting_id_var),
    ("Meeting Passcode:", meeting_passcode_var),
    ("Zoom Path:", zoom_path_var),
    ("Schedule Time:", schedule_time_var),
    ("Schedule Days (comma-separated):", schedule_days_var),
    ("Recording Duration (seconds):", record_duration_var),
    ("Join Button X:", join_a_meeting_x_var),
    ("Join Button Y:", join_a_meeting_y_var)
]


for i, (label_text, var) in enumerate(fields):
    ttk.Label(settings_frame, text=label_text).grid(row=i, column=0, padx=10, pady=5, sticky="w")
    ttk.Entry(settings_frame, textvariable=var, width=40).grid(row=i, column=1, padx=10, pady=5)


ttk.Button(settings_frame, text="Locate Join Button", command=locate_join_button).grid(row=len(fields), column=0, columnspan=2, pady=10)


ttk.Checkbutton(settings_frame, text="Show Guide", variable=show_guide_var).grid(row=len(fields) + 1, column=0, padx=10, pady=5, sticky="w")


save_button = ttk.Button(settings_frame, text="Save Settings", command=update_config)
save_button.grid(row=len(fields) + 2, column=0, columnspan=2, pady=20)


ttk.Button(status_frame, text="Start Scheduled Bot", command=start_scheduled_bot).pack(pady=5)


ttk.Button(status_frame, text="Join Meeting Now", command=start_manual_meeting).pack(pady=5)


root.mainloop()


