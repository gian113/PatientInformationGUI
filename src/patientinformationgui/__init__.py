'''
MINIMAL ORDER CHECKLIST 
[/] = done
[o] = in progress
-----------------------
  [/ gian] database.py with load/save
  [/ all of us] all feature functions
  [ ] test script confirms database.py works
  [/ xian] App + RoleSelect + AdminLogin
  [o xian] AdminMenu, DoctorsPage, EquipmentPage
  [o xian] UserMenu + RegistrationMenu + ServicesMenu
  [/ aira] PatientForm (pattern for all forms)
  [/ aira] GuestForm, AppointmentForm
  [/ aira] SearchPage
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
from datetime import datetime

# locates the first 2 folders outside of this one
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
dir = os.path.join(root_dir, "database")  # locates the files within the folder

# Replace later with right file names
patient_path = os.path.join(dir, "Patient_data.json")
appointment_path = os.path.join(dir, "appointments.json")
Equipment_path = os.path.join(dir, "Equipment.json")
Medical_path = os.path.join(dir, "Medical_personel.json")
guest_path = os.path.join(dir, "guest_data.json")
billing_path = os.path.join(dir, "billing.json")

ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

# Patient Info
sex = ["Male", "Female"]
blood_type = ["A", "A-", "B", "B-", "AB", "AB-", "O", "O-"]

SERVICES = {
    "Consultation": 500,
    "Blood Test": 800,
    "X-Ray": 1200,
    "Medicine Pack": 350,
    "Room (per day)": 1500,
}
PAYMENT_METHODS = ["Cash", "Credit/Debit Card", "GCash", "Insurance"]

# ---------------------------------------------------------------- DESIGN
# Change colors/fonts here and the whole app updates.
THEME = {
    "bg":        "#FFFFFF",   # window background
    "header":    "#1F6FB2",   # top title bar
    "header_fg": "#FFFFFF",
    "text":      "#141515",   # most text
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
        if all(record.get("I.D.") != number for record in records):
            return number


# TK starting
root = tk.Tk()
root.geometry("420x620")
root.minsize(380, 560)
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


def listing(lines, height=10):
    """A scrollable list of text lines."""
    frame = tk.Frame(content, bg=THEME["bg"])
    frame.pack(fill="both", expand=True, pady=(5, 10))
    bar = tk.Scrollbar(frame)
    bar.pack(side="right", fill="y")
    box = tk.Listbox(frame, font=FONT_BODY, height=height, relief="flat",
                     highlightthickness=1, highlightbackground=THEME["border"],
                     activestyle="none", yscrollcommand=bar.set)
    box.pack(side="left", fill="both", expand=True)
    bar.config(command=box.yview)
    for line in lines:
        box.insert("end", line)
    if not lines:
        box.insert("end", "No records found.")
    return box


def record_text(record):
    return " ".join(str(value) for value in record.values()).lower()


def record_name(record):
    return record.get("Full Name") or record.get("Name") or "N/A"


def find_patient(patient_id):
    for p in load(patient_path):
        if isinstance(p, dict) and str(p.get("I.D.")) == str(patient_id).strip():
            return p
    return None

# Billing Services


def billing():
    clear("Billing")
    id = entry("Patient I.D.")

    def find():
        p = find_patient(id.get())
        if p:
            return payment_screen(p)
        messagebox.showerror("Not found", "No matching patient found.")
    id.bind("<Return>", lambda event: find())
    button("Find Patient", find)
    button("Back", user_menu, "secondary")
    id.focus_set()


def payment_screen(patient=None):
    clear("Payment")
    label(f"Patient: {record_name(patient)}   (I.D. {patient.get('I.D.')})")

    chosen = {}
    total_text = tk.StringVar(value="Total: PHP 0.00")

    def update_total():
        total = sum(price for name, price in SERVICES.items()
                    if chosen[name].get())
        total_text.set(f"Total: PHP {total:,.2f}")
        return total

    for name, price in SERVICES.items():
        chosen[name] = tk.IntVar(value=0)
        tk.Checkbutton(content, text=f"{name} - PHP {price:,.2f}",
                       variable=chosen[name], command=update_total,
                       font=FONT_BODY, bg=THEME["bg"], fg=THEME["text"],
                       activebackground=THEME["bg"], anchor="w",
                       selectcolor=THEME["field"]).pack(fill="x", pady=2)

    tk.Label(content, textvariable=total_text, font=FONT_BUTTON,
             bg=THEME["bg"], fg=THEME["text"]).pack(anchor="w", pady=(10, 6))
    method = dropdown("Payment Method", PAYMENT_METHODS)
    method.current(0)

    def pay():
        picked = [name for name in SERVICES if chosen[name].get()]
        if not picked:
            messagebox.showwarning("Warning", "Please select at least one service.")
            return
        total = update_total()
        records = load(billing_path)
        records.append({"I.D.": new_id(records, 100000, 999999),
                        "Patient I.D.": patient.get("I.D."),
                        "Patient": record_name(patient),
                        "Services": picked,
                        "Total": total,
                        "Method": method.get(),
                        "Date": datetime.now().strftime("%Y-%m-%d %H:%M")})
        save(billing_path, records)
        messagebox.showinfo("Payment received",
                            f"Paid PHP {total:,.2f} via {method.get()}.")
        billing()

    button("Pay", pay)
    button("Back", billing, "secondary")

# Admin options/login


def admin():
    clear("Admin Login")
    user = entry("Username")
    pw = entry("Password", show="*")

    def login():
        if user.get().strip() == ADMIN_USER and pw.get() == ADMIN_PASS:
            admin_menu()
        else:
            messagebox.showerror("Login failed", "Incorrect username or password.")
    pw.bind("<Return>", lambda event: login())
    button("Log In", login)
    button("Back", main_menu, "secondary")
    user.focus_set()

# admin user menu


def admin_menu():
    clear("Admin Menu")
    label("Welcome, Admin! Choose!")
    button("Clinical Support Services", clinical_services, "primary")
    button("Medicine & Equipment", medicine_equipment, "primary")
    button("Patient Tracking", patient_tracking, "primary")
    button("Appointments and Schedules", appointments_schedule, "primary")
    button("Logout", main_menu, "danger")

# clinical support services


def clinical_services():
    clear("Clinical Services")
    label("CLINIC SERVICES")
    button("Doctors Appointment",
           lambda: appointment_form(clinical_services, "Doctor Appointment"),
           "primary")
    button("Blood Test",
           lambda: appointment_form(clinical_services, "Blood Test"),
           "primary")
    button("Doctors", doctors_page, "primary")
    button("Back", admin_menu, "danger")


def doctors_page():
    clear("Doctors")
    label("MEDICAL PERSONNEL")
    lines = [f"{d.get('I.D.')} | Dr. {d.get('Name', 'N/A')} | {d.get('Specialty', 'N/A')}"
             for d in load(Medical_path) if isinstance(d, dict)]
    listing(lines)
    button("Add Doctor", add_doctor, "primary")
    button("Back", clinical_services, "danger")


def add_doctor():
    clear("Add Doctor")
    name = entry("Doctor's Full Name")
    specialty = entry("Specialty")

    def add():
        if not name.get().strip() or not specialty.get().strip():
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return
        records = load(Medical_path)
        records.append({"I.D.": new_id(records, 1000, 9999),
                        "Name": name.get().strip().title(),
                        "Specialty": specialty.get().strip().title()})
        save(Medical_path, records)
        messagebox.showinfo("Success!", "Doctor added successfully!")
        doctors_page()
    button("Add", add)
    button("Back", doctors_page, "secondary")
    name.focus_set()

# medicine and equipment


def medicine_equipment():
    clear("Medicine and Equipment")
    label("MEDICINE & EQUIPMENTS")
    label("Available EQUIPMENTS in The Clinic:")

    lines = [f"{e.get('Name', 'N/A')}  (Qty: {e.get('Quantity', 'N/A')})"
             for e in load(Equipment_path) if isinstance(e, dict)]
    listing(lines)
    button("Add Equipment", add_equipment, "primary")
    button("Back", admin_menu, "danger")


def add_equipment():
    clear("Add Equipment")
    name = entry("Equipment Name")
    qty = entry("Quantity")

    def add():
        if not name.get().strip() or not qty.get().strip().isdigit():
            messagebox.showwarning(
                "Warning", "Enter a name and a whole-number quantity.")
            return
        records = load(Equipment_path)
        records.append({"I.D.": new_id(records, 1000, 9999),
                        "Name": name.get().strip().title(),
                        "Quantity": int(qty.get().strip())})
        save(Equipment_path, records)
        messagebox.showinfo("Success!", "Equipment added successfully!")
        medicine_equipment()
    button("Add", add)
    button("Back", medicine_equipment, "secondary")
    name.focus_set()

# patient tracking


def search_page(title, back):
    clear(title)
    label("PATIENT TRACKER")
    box = entry("Search (I.D., name, or anything in the record)")

    def search():
        query = box.get().strip().lower()
        if not query:
            messagebox.showwarning("Warning", "Please enter something to search.")
            return
        matches = [p for p in load(patient_path)
                   if isinstance(p, dict) and query in record_text(p)]
        if not matches:
            messagebox.showwarning(
                "Not found",
                "This patient is not in the list.\nPlease register through Patient Registration.")
            return
        search_results(title, matches, lambda: search_page(title, back))

    box.bind("<Return>", lambda event: search())
    button("Search", search)
    button("Back", back, "danger")
    box.focus_set()


def search_results(title, matches, again):
    clear(title)
    label("PATIENT INFORMATION")
    lines = []
    for p in matches:
        lines.append(f"Patient ID: {p.get('I.D.', 'N/A')}")
        lines.append(f"Name: {record_name(p)}")
        lines.append(f"Age: {p.get('Age', 'N/A')}")
        lines.append(f"Sex: {p.get('Sex', 'N/A')}")
        lines.append(f"Blood Type: {p.get('Blood Type', 'N/A')}")
        lines.append(f"Contact: {p.get('Contact', 'N/A')}")
        lines.append("-" * 30)
    listing(lines, 14)
    button("Back", again, "danger")


def patient_tracking():
    search_page("Patient Tracking", admin_menu)

# appointments and schedule


def appointments_schedule():
    clear("Appointments and Schedule")
    label("APPOINTMENT & SCHEDULES")
    label("Scheduled :")
    records = [a for a in load(appointment_path) if isinstance(a, dict)]
    records.sort(key=lambda a: (a.get("Date", ""), a.get("Time", "")))
    lines = [f"{a.get('Date')} {a.get('Time')} | {a.get('Patient')} | "
             f"{a.get('Service')} | {a.get('Doctor')}" for a in records]
    listing(lines, 12)
    button("Back", admin_menu, "danger")


def appointment_form(back, service="Doctor Appointment"):
    clear(service)
    pid = entry("Patient I.D.")
    doctor = None
    if service == "Doctor Appointment":
        names = [f"Dr. {d.get('Name')} ({d.get('Specialty')})"
                 for d in load(Medical_path) if isinstance(d, dict)]
        doctor = dropdown("Doctor", names)
    date = entry("Date (YYYY-MM-DD)")
    time = entry("Time (HH:MM, 24-hour)")

    def book():
        patient = find_patient(pid.get())
        if not patient:
            messagebox.showerror("Not found", "No matching patient found.")
            return
        if doctor is not None and not doctor.get():
            messagebox.showwarning("Warning", "Please choose a doctor.")
            return
        try:
            datetime.strptime(date.get().strip(), "%Y-%m-%d")
            datetime.strptime(time.get().strip(), "%H:%M")
        except ValueError:
            messagebox.showwarning(
                "Warning", "Use the date format YYYY-MM-DD and time format HH:MM.")
            return
        records = load(appointment_path)
        records.append({"I.D.": new_id(records, 100000, 999999),
                        "Patient I.D.": patient.get("I.D."),
                        "Patient": record_name(patient),
                        "Service": service,
                        "Doctor": doctor.get() if doctor is not None else "Laboratory",
                        "Date": date.get().strip(),
                        "Time": time.get().strip()})
        save(appointment_path, records)
        messagebox.showinfo("Success!", "Appointment booked successfully!")
        back()

    button("Book", book)
    button("Back", back, "secondary")
    pid.focus_set()


def user_menu():
    clear("Guest and Patient Registration")

    label("Welcome, User!")
    button("Patient Management system", patient_management)
    button("Registration Application", registration_application)
    button("Billing Page", billing)
    button("Back", main_menu, "danger")


# patient management system
def patient_management():
    clear("Patient Management System")
    label("Patient Management System")
    button("Search Patient",
           lambda: search_page("Search Patient", patient_management))
    button("Book Appointment",
           lambda: appointment_form(patient_management, "Doctor Appointment"))
    button("Book Blood Test",
           lambda: appointment_form(patient_management, "Blood Test"))
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
    pget_name = entry("Full Name")
    pget_age = entry("Age")
    pget_contact = entry("Contact Number")
    pget_sex = dropdown("Sex", sex)
    pget_blood = dropdown("Blood Type", blood_type)

    def pregister():
        pfull_name = pget_name.get().strip()

        if not pfull_name:
            messagebox.showwarning(
                "Warning", "Please enter the patient's full name.")
            return
        if not pget_age.get().strip().isdigit():
            messagebox.showwarning("Warning", "Please enter a valid age.")
            return
        if not pget_sex.get() or not pget_blood.get():
            messagebox.showwarning(
                "Warning", "Please choose the sex and blood type.")
            return

        precords = load(patient_path)
        patient = {"I.D.": new_id(precords, 100000, 999999),
                   "Full Name": pfull_name.title(),
                   "Age": int(pget_age.get().strip()),
                   "Contact": pget_contact.get().strip(),
                   "Sex": pget_sex.get(),
                   "Blood Type": pget_blood.get()}
        precords.append(patient)
        save(patient_path, precords)

        messagebox.showinfo(
            "Success!", f"Patient registered succesfully!\nPatient I.D.: {patient['I.D.']}")
        patient_registration()
    button("REGISTER", pregister)
    button("Close", user_menu, "danger")


# GUEST application
def guest_registration():
    clear("Guest Registration")

    label("Guest Applcant")
    gget_name = entry("Full Name")
    gget_contact = entry("Contact Number")
    gget_purpose = entry("Purpose of Visit")

    def gregister():
        gfull_name = gget_name.get().strip()

        if not gfull_name:
            messagebox.showwarning(
                "Warning", "Please enter the guest's full name.")
            return

        grecords = load(guest_path)
        guest = {"I.D.": new_id(grecords, 100000, 999999),
                 "Full Name": gfull_name.title(),
                 "Contact": gget_contact.get().strip(),
                 "Purpose": gget_purpose.get().strip(),
                 "Date": datetime.now().strftime("%Y-%m-%d %H:%M")}
        grecords.append(guest)
        save(guest_path, grecords)

        messagebox.showinfo(
            "Success!", f"Guest registered succesfully!\nGuest I.D.: {guest['I.D.']}")
        guest_registration()
    button("REGISTER", gregister)
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