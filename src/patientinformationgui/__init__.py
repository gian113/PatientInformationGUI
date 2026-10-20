'''
MINIMAL ORDER CHECKLIST 
[/] = done
[o] = in progress
-----------------------
  [/ gian] database.py with load/save
  [/ all of us] all feature functions
  [ ] test script confirms database.py works
  [/ xian] App + RoleSelect + AdminLogin
  [xian] AdminMenu, DoctorsPage, EquipmentPage
  [xian] UserMenu + RegistrationMenu + ServicesMenu
  [xian] PatientForm (pattern for all forms)
  [aira] GuestForm, AppointmentForm
  [aira] SearchPage
  [o gian] BillingPage
  [o gian] Bug list above fixed
  [o gian] Full test pass (Step 6)
  [o gian] Polish
'''

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

# ---------------------------------------------------------------- DESIGN
# Change colors/fonts here and the whole app updates.
THEME = {
    "bg":        "#161128",   # window background
    "header":    "#1F6FB2",   # top title bar
    "header_fg": "#FFFFFF",
    "text":      "#1E2A35",   # most text
    "muted":     "#6B7A89",
    "primary":   "#1F6FB2",   # main buttons
    "primary_h": "#17598F",   # primary hover
    "secondary": "#E1E8EF",   # back / secondary buttons
    "secondary_h": "#CFD9E3",
    "danger":    "#C0392B",
    "field":     "#FFFFFF",
    "border":    "#C5D0DB",
}
FONT = "Segoe UI"   # change nyo nalang
FONT_TITLE = (FONT, 16, "bold")
FONT_BODY = (FONT, 10)
FONT_BUTTON = (FONT, 10, "bold")

# Load/Save data


def load(path):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return []
    try:
        with open(path, 'r') as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
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


# TK starting
root = tk.Tk()
root.geometry("420x520")
root.minsize(380, 460)
root.title("Patient Information System")
root.configure(bg=THEME["bg"])

# ttk widgets (dropdowns) styling
style = ttk.Style(root)
style.theme_use("clam")
style.configure("TCombobox",
                fieldbackground=THEME["field"], background=THEME["field"],
                foreground=THEME["text"], bordercolor=THEME["border"],
                arrowcolor=THEME["primary"], padding=6)
style.map("TCombobox", fieldbackground=[("readonly", THEME["field"])])

# window guides


def hover(widget, normal, over):
    widget.bind("<Enter>", lambda e: widget.config(bg=over))
    widget.bind("<Leave>", lambda e: widget.config(bg=normal))


def clear(title_text):
    """Wipes the window and draws the header bar + a fresh content area."""
    global content
    for widget in root.winfo_children():
        widget.destroy()

    bar = tk.Frame(root, bg=THEME["header"], height=64)
    bar.pack(fill="x")
    bar.pack_propagate(False)
    tk.Label(bar, text=title_text, font=FONT_TITLE,
             bg=THEME["header"], fg=THEME["header_fg"]).pack(expand=True)

    content = tk.Frame(root, bg=THEME["bg"])
    content.pack(fill="both", expand=True, padx=30, pady=20)


def button(text, command, kind="primary"):
    """kind: 'primary' (blue), 'secondary' (grey, for Back) or 'danger'."""
    colors = {
        "primary":   (THEME["primary"], THEME["primary_h"], "#FFFFFF"),
        "secondary": (THEME["secondary"], THEME["secondary_h"], THEME["text"]),
        "danger":    (THEME["danger"], "#A02F23", "#FFFFFF"),
    }
    bg, bg_hover, fg = colors[kind]
    b = tk.Button(content, text=text, command=command, font=FONT_BUTTON,
                  bg=bg, fg=fg, activebackground=bg_hover, activeforeground=fg,
                  relief="flat", bd=0, cursor="hand2", pady=8)
    b.pack(fill="x", pady=5)
    hover(b, bg, bg_hover)
    return b


def label(text):
    tk.Label(content, text=text, font=FONT_BODY, bg=THEME["bg"],
             fg=THEME["muted"], wraplength=340, justify="left").pack(anchor="w")


def entry(label_text, show=""):
    """A label with a text box under it. Returns the text box."""
    tk.Label(content, text=label_text, font=FONT_BODY, bg=THEME["bg"],
             fg=THEME["text"]).pack(anchor="w")
    box = tk.Entry(content, show=show, font=FONT_BODY, bg=THEME["field"],
                   fg=THEME["text"], relief="flat", highlightthickness=1,
                   highlightbackground=THEME["border"],
                   highlightcolor=THEME["primary"])
    box.pack(fill="x", pady=(2, 12), ipady=6)
    return box


def dropdown(label_text, values):
    """A label with a pick-one list under it. Returns the dropdown."""
    tk.Label(content, text=label_text, font=FONT_BODY, bg=THEME["bg"],
             fg=THEME["text"]).pack(anchor="w")
    box = ttk.Combobox(content, values=values, state="readonly",
                       font=FONT_BODY)
    box.pack(fill="x", pady=(2, 12))
    return box

# Billing Services


def billing():
    clear("Billing")
    id = entry("Patient I.D.")

    def find():
        for p in load(patient_path):
            if str(p["I.D."]) == id.get().strip():
                return payment_screen(p)
        messagebox.showerror("Not found", "No matching patient found.")
    id.bind("<Return>", lambda event: find())
    button("Find Patient", find)
    button("Back", user_menu, "secondary")
    id.focus_set()


def payment_screen(patient=None):
    clear("Payment")
    label("Payment screen coming soon.")
    button("Back", billing, "secondary")

# Admin options/login
def admin():
    clear("Admin Login")
    user = entry("Username")
    pw = entry("Password", show="*")
    button("Log In", admin_menu, "secondary")
    button("Back", main_menu, "secondary")
    user.focus_set()

# User options/login
def user_menu():
    clear("User Menu")
    button("Billing", billing)
    button("Back", main_menu, "secondary")

# admin user menu
def admin_menu():
    clear("Admin Menu")
    label("Welcome, Admin! Choose!")
    button("Clinical Support Services", clinical_services, "primary")
    button("Medicine & Equipment", medicine_equipment, "primary")
    button("Patient tracking", patient_tracking, "primary")
    button("Appointments and Schedules", appointments_schedule, "primary")
    button("Logout", main_menu, "danger")

# clinical support services
def clinical_services():
    clear("Clinical Services")
    label("CLINIC SERVICES")
    button("Back", admin_menu, "danger")

# medicine and equipment
def medicine_equipment():
    clear("Medicine and Equipment")
    label("MEDICINE & EQUIPMENTS")

    def medicine_equipment():  # buti di ka gumamit ng for-loop
        clear("Medicine and Equipment")
        label("MEDICINE & EQUIPMENTS")
        label("Available MEDICINES in The Clinic:")
        label("Paracetamol")
        label("Biogesic")
        label("BioFlu")
        label("Tuseran Forte")
        label("Loperamide")
        label("Amlodipine")
        label("Losartan")
        label("Amoxicillin")

        label("Available EQUIPMENTS in The Clinic:")
        label("Stethoscope")
        label("Thermometer")
        label("Ventilator")
        label("Defibrillator")
        label("Glucometer")
        label("Scalpel Blades & Handles")
        label("Surgical Forceps")
        label("First Aid Kit")
        label("Thermometer")
        label("Syringe")
        label("Resuscitator")
        label("Blood Pressure Monitor")
        label("Gurney")

    button("Back", admin_menu, "danger").pack(pady=30)

# patient tracking
def patient_tracking():
    clear("Patient Tracking")
    label("PATIENT TRACKER")

    search_box = entry("Insert Patient's Name")
    button("Search", patient_path, "primary")
    button("Back", admin_menu, "danger")

# appointments and schedule
def appointments_schedule():
    clear("Appointments and Schedule")
    label("APPOINTMENT & SCHEDULES")
    label("Available :")
    button("Back", admin_menu, "danger")

def user_menu():
    clear("Guest and Patient Registration")

    label("Welcome, User!")
    button("Patient Management system", patient_management)
    button("Registration Application", registration_application)
    # Put billing code here!
    button("Back", main_menu, "danger")

# patient management system


def patient_management():
    clear("Patient Management System")
    label("Patient Management System")
    button("Back", user_menu, "danger")

# registration application


def registration_application():
    clear("Registration Application")

    label("REGISTRATION APPLICATION")
    button("Patient Registration", patient_registration)
    button("Guest Registration", guest_registration)
    button("Back", user_menu, "danger")

# PATIENT application


def patient_registration():
    clear("Patient Registration")

    label("Register Applicant")
    first_name = entry("First Name")
    last_name = entry("Lastname")

    button("REGISTER", patient_registration)
    button("Close", user_menu, "danger")

# GUEST application
def guest_registration():
    clear("Guest Registration")
    first_name = entry("first_name")
    last_name = entry("last_name")

    tk.Button("Register", guest_registration)
    button("Close", user_menu, "danger")

# Main GUI
def main_menu():
    clear("Patient Information System")
    label("Choose how you want to sign in.")
    tk.Frame(content, bg=THEME["bg"], height=10).pack()
    button("ADMIN", admin)
    button("USER", user_menu)


main_menu()
root.mainloop()
