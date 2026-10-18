import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import random

# locates the first 2 folders outside of this one
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
dir = os.path.join(root_dir, "database")  # locates the files within the folder

# Replace later with right file names
patient_path = os.path.join(dir, "Patient_data.json")
appointment_path = os.path.join(dir, "Patient_data.json")
Equipment_path = os.path.join(dir, "Patient_data.json")
Medical_path = os.path.join(dir, "Patient_data.json")
guest_path = os.path.join(dir, "Patient_data.json")

# Patient Info
sex = ["Male", "Female"]
blood_type = ["A", "A-", "B", "B-", "AB", "AB-", "O", "O-"]

# Load/Save data


def load(path):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return []
    try:
        with open(path, 'r') as file:
            data = json.load(file)
    except json.JSONDecodeError, OSError:
        return []
    return data if isinstance(data, list) else []


def save(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, 'w') as file:
        json.dump(data, file, indent=4)
    os.replace(tmp, path)

# ID generation


def new_id(records, low, high):
    while True:
        number = random.randint(low, high)
        if all(record["I.D."] != number for record in records):
            return number

# window guides


def clear(title_text):
    for widget in root.winfo_children():
        widget.destroy()
    tk.Label(root, text=title_text, font=("Arial", 16, "bold")).pack(pady=15)


def button(text, command):
    tk.Button(root, text=text, command=command, width=34).pack(pady=4)


def label(text):
    tk.Label(root, text=text).pack()


def entry(label_text, show=""):
    """A label with a text box under it. Returns the text box."""
    tk.Label(root, text=label_text).pack()
    box = tk.Entry(root, show=show, width=30)
    box.pack(pady=(0, 8))
    return box


def dropdown(label_text, values):
    """A label with a pick-one list under it. Returns the dropdown."""
    tk.Label(root, text=label_text).pack()
    box = ttk.Combobox(root, values=values, state="readonly", width=27)
    box.pack(pady=(0, 8))
    return box

# Billing Services


def billing():
    clear("Billing")
    id = entry(patient_path)

    def find():
        for p in load("Patient_data.json"):
            if str(p["I.D."]) == id.get().strip():
                return payment_screen(p)
            messagebox.showerror("Not found", "No matching patient found.")
    id.bind("<Return>", lambda event: find())
    button("Find Patient", find)
    button("Back", user_menu)
    id.focus_set()

# Main GUI


def payment_screen():
    pass


# TK starting
root = tk.Tk()
root.geometry("300x300")
root.title("Patient Information System")

# Admin options/login


def admin():
    window = tk.Toplevel(root)
    window.title("Admin Login")
    window.geometry("300x300")

    admin_login = tk.Entry(window)
    admin_login.pack()

    admin_login2 = tk.Entry(window)
    admin_login2.pack()


def login(window=root):
    login_admin = tk.Button(window, text="ADMIN", command=login.destroy)
    login_admin.pack()


hi = tk.Button(root, text="ADMIN", command=admin)
hi.pack()

# User options/login


def user_menu():
    window = tk.Toplevel(root)


hii = tk.Button(root, text="USER", command=user_menu)
hii.pack()


root.mainloop()
