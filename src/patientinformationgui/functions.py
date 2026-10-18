"""
functions.py - the whole Patient Information System, as simply as possible.

How it works
------------
There is ONE window. Every screen is a function that wipes the window and
draws new widgets. To go to another screen, call that screen's function.

    home()      -> admin_login() -> admin_menu() -> doctors_screen() / equipment_screen()
    home()      -> user_menu()   -> registration_menu() -> patient_form() / guest_form()
                                 -> services_menu()     -> appointment_form() / search_screen()
                                 -> billing_screen()    -> payment_screen()

Data is saved as lists of dictionaries in the JSON files inside database/.

Run it with:   uv run patientinformationgui
"""

import json
import os
import random
import tkinter as tk
from tkinter import messagebox, ttk

# ---------------------------------------------------------------- settings ---
# class project only - don't reuse a real password
ADMIN_PASSWORD = "adminroot123"
BLOOD_TYPES = ["A", "A-", "B", "B-", "AB", "AB-", "O", "O-"]

# This file is in <project>/src/patientinformationgui/ and the JSON files are in
# <project>/database/, so go up two folders.
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DB_DIR = os.path.join(ROOT_DIR, "database")


# ------------------------------------------------------- saving and loading ---
def load(filename):
    """Return the list saved in database/<filename> ([] if missing or empty)."""
    path = os.path.join(DB_DIR, filename)
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return []
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except ValueError:
        return []


def save(filename, data):
    """Save a list into database/<filename> (makes the folder if needed)."""
    os.makedirs(DB_DIR, exist_ok=True)
    with open(os.path.join(DB_DIR, filename), "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def new_id(records, low, high):
    """A random I.D. that no record in `records` is using yet."""
    while True:
        number = random.randint(low, high)
        if all(record["I.D."] != number for record in records):
            return number


# ----------------------------------------------------------------- checking ---
def good_name(text):
    cleaned = text.replace(" ", "").replace("-", "").replace("'", "")
    return cleaned.isalpha()


def good_age(text):
    text = text.strip()
    return text.isdecimal() and int(text) <= 130


def good_phone(text):
    digits = text.replace(" ", "").replace("-", "").lstrip("+")
    return digits.isdecimal() and 7 <= len(digits) <= 15


def card_problem(card, cvv, expiry):
    """Return a message if the card details are wrong, or "" if they are fine."""
    card = card.replace(" ", "")
    cvv = cvv.strip()
    expiry = expiry.strip()
    if not (card.isdecimal() and len(card) == 16):
        return "Card number must be exactly 16 digits."
    if not (cvv.isdecimal() and 3 <= len(cvv) <= 4):
        return "CVV must be 3 or 4 digits."
    month_ok = expiry[:2].isdecimal() and 1 <= int(expiry[:2]) <= 12
    if not (len(expiry) == 5 and expiry[2] == "/" and expiry[3:].isdecimal() and month_ok):
        return "Expiration date must look like MM/YY (month 01-12)."
    return ""


def full_name(first, last):
    return f"{first.strip().capitalize()} {last.strip().capitalize()}"


def error(message):
    messagebox.showerror("Invalid input", message)


# ----------------------------------------------------------- window helpers ---
window = tk.Tk()
window.title("Patient Information System")
window.geometry("560x560")


def clear(title_text):
    """Wipe the window and put a new title at the top."""
    for widget in window.winfo_children():
        widget.destroy()
    tk.Label(window, text=title_text, font=("Arial", 16, "bold")).pack(pady=15)


def button(text, command):
    tk.Button(window, text=text, command=command, width=34).pack(pady=4)


def label(text):
    tk.Label(window, text=text).pack()


def entry(label_text, show=""):
    """A label with a text box under it. Returns the text box."""
    tk.Label(window, text=label_text).pack()
    box = tk.Entry(window, show=show, width=30)
    box.pack(pady=(0, 8))
    return box


def dropdown(label_text, values):
    """A label with a pick-one list under it. Returns the dropdown."""
    tk.Label(window, text=label_text).pack()
    box = ttk.Combobox(window, values=values, state="readonly", width=27)
    box.pack(pady=(0, 8))
    return box


# ----------------------------------------------------------- start + admin ---
def home():
    clear("PATIENT INFORMATION SYSTEM")
    button("Admin", admin_login)
    button("User Mode", user_menu)
    button("Exit", window.destroy)


def admin_login():
    clear("Admin Login")
    password = entry("Enter Password:", show="*")

    def login():
        if password.get() == ADMIN_PASSWORD:
            admin_menu()
        else:
            messagebox.showerror("Login failed", "INVALID PASSWORD!")
            password.delete(0, "end")

    password.bind("<Return>", lambda event: login())
    button("Login", login)
    button("Back", home)
    password.focus_set()


def admin_menu():
    clear("Welcome Admin!")
    button("Doctors Working Today", doctors_screen)
    button("Equipment On Stock", equipment_screen)
    button("Log out", home)


def show_list(heading, items, nothing_text):
    """Used by the two admin pages: a heading, a list, and a Back button."""
    clear(heading)
    if items:
        box = tk.Listbox(window, width=45, height=12)
        for item in items:
            box.insert("end", item)
        box.pack()
    else:
        label(nothing_text)
    button("Back", admin_menu)


def doctors_screen():
    names = [d["Name"]
             for d in load("Medical_personel.json") if "Clocked in" in d["Status"]]
    show_list("Doctors working today", names, "No doctors are clocked in.")


def equipment_screen():
    names = [e["Name"]
             for e in load("Equipment.json") if "On stock" in e["Status"]]
    show_list("Equipment (ONLY ON STOCK)", names, "No equipment is on stock.")


# --------------------------------------------------------------- user menus ---
def user_menu():
    clear("PATIENT INFORMATION SYSTEM")
    button("Patient Registration Application", registration_menu)
    button("Resources & Services Management", services_menu)
    button("Billing Services", billing_screen)
    button("Back", home)


def registration_menu():
    clear("Registration Application")
    button("Patient Registration", patient_form)
    button("Guest Registration", guest_form)
    button("Back", user_menu)


def services_menu():
    clear("Resources & Services Management")
    button("Schedule an Appointment", appointment_form)
    button("Search for Patient", search_screen)
    button("Back", user_menu)


# ------------------------------------------------------------------- forms ---
def patient_form():
    clear("Patient Registration")
    first = entry("First Name:")
    last = entry("Last Name:")
    sex = dropdown("Sex:", ["Male", "Female"])
    age = entry("Age:")
    blood = dropdown("Blood Type:", BLOOD_TYPES)

    def register():
        if not good_name(first.get()) or not good_name(last.get()):
            return error("Names may only contain letters, spaces and hyphens.")
        if sex.get() == "":
            return error("Please choose a sex.")
        if not good_age(age.get()):
            return error("Age must be a whole number from 0 to 130.")
        if blood.get() == "":
            return error("Please choose a blood type.")

        name = full_name(first.get(), last.get())
        record = {"Name": name, "Sex": sex.get(), "Age": int(
            age.get()), "Blood Type": blood.get()}

        patients = load("Patient_data.json")
        found = False
        for i, old in enumerate(patients):
            # same name AND same age = same patient
            if old["Name"] == name and old["Age"] == record["Age"]:
                found = True
                if not messagebox.askyesno(
                        "Patient already exists",
                        f"{name} (age {record['Age']}) is already registered.\n\n"
                        "Overwrite the existing record?"):
                    return
                record["I.D."] = old["I.D."]
                record["Room Number"] = old["Room Number"]
                patients[i] = record
        if not found:
            record["I.D."] = new_id(patients, 100000, 999999)
            record["Room Number"] = random.randint(10, 30)
            patients.append(record)

        save("Patient_data.json", patients)
        messagebox.showinfo(
            "Success",
            f"{name} has been registered.\n\n"
            f"I.D.: {record['I.D.']}\nRoom Number: {record['Room Number']}")
        registration_menu()

    button("Register Patient", register)
    button("Back", registration_menu)
    first.focus_set()


def guest_form():
    clear("Guest Registration")
    first = entry("First Name:")
    last = entry("Last Name:")

    def register():
        if not good_name(first.get()) or not good_name(last.get()):
            return error("Names may only contain letters, spaces and hyphens.")

        guests = load("guest_data.json")
        record = {"Name": full_name(
            first.get(), last.get()), "I.D.": new_id(guests, 1000, 9999)}
        guests.append(record)
        save("guest_data.json", guests)
        messagebox.showinfo(
            "Success", f"Guest {record['Name']} has been registered.\n\nI.D.: {record['I.D.']}")
        registration_menu()

    button("Register Guest", register)
    button("Back", registration_menu)
    first.focus_set()


def appointment_form():
    clear("Schedule an Appointment")
    first = entry("First Name:")
    last = entry("Last Name:")
    age = entry("Age:")
    phone = entry("Phone Number:")

    def book():
        if not good_name(first.get()) or not good_name(last.get()):
            return error("Names may only contain letters, spaces and hyphens.")
        if not good_age(age.get()):
            return error("Age must be a whole number from 0 to 130.")
        if not good_phone(phone.get()):
            return error("Phone number must have 7-15 digits.")

        appointments = load("appointments.json")
        record = {
            "Name": full_name(first.get(), last.get()),
            "Age": int(age.get()),
            "I.D.": new_id(appointments, 1000, 9999),
            "Phone Number": phone.get().strip(),   # text, so a leading 0 is kept
        }
        appointments.append(record)
        save("appointments.json", appointments)
        messagebox.showinfo(
            "Appointment booked",
            f"Appointment saved for {record['Name']}.\n\nI.D.: {record['I.D.']}")
        services_menu()

    button("Book Appointment", book)
    button("Back", services_menu)
    first.focus_set()


# ------------------------------------------------------------------ search ---
def search_screen():
    clear("Search for Patient")
    name_box = entry("Patient name (leave empty to list everyone):")
    results = tk.Listbox(window, width=70, height=12)
    message = tk.Label(window, text="")

    def run_search():
        results.delete(0, "end")
        text = name_box.get().strip().lower()
        count = 0
        for p in load("Patient_data.json"):
            if text in p["Name"].lower():
                results.insert(
                    "end",
                    f"{p['Name']}  |  I.D. {p['I.D.']}  |  Age {p['Age']}  |  {p['Sex']}  |  "
                    f"{p['Blood Type']}  |  Room {p['Room Number']}")
                count += 1
        message.config(
            text=f"{count} patient(s) found." if count else "No matching patient found.")

    name_box.bind("<Return>", lambda event: run_search())
    button("Search", run_search)
    results.pack(pady=8)
    message.pack()
    button("Back", services_menu)
    name_box.focus_set()


# ----------------------------------------------------------------- billing ---
def billing_screen():
    clear("Billing")
    id_box = entry("Patient I.D.:")

    def find():
        for p in load("Patient_data.json"):       # loaded fresh, so new patients show up
            if str(p["I.D."]) == id_box.get().strip():
                return payment_screen(p)
        messagebox.showerror("Not found", "No matching patient found.")

    id_box.bind("<Return>", lambda event: find())
    button("Find Patient", find)
    button("Back", user_menu)
    id_box.focus_set()


def payment_screen(patient):
    total = random.randrange(1000, 20000)
    receipt_no = random.randint(1000000000000, 9999999999999)

    clear("Payment")
    label(f"Patient: {patient['Name']}      I.D.: {patient['I.D.']}")
    label(f"Total Amount: ${total:,}")
    label(f"Receipt No.: {receipt_no}")

    mode = tk.StringVar(value="Cash")
    tk.Label(window, text="\nMode of payment:").pack()
    for choice in ["Cash", "Card", "Bank Transfer"]:
        tk.Radiobutton(window, text=choice, value=choice, variable=mode).pack()

    tk.Label(window, text="\nCard details (only if paying by card):").pack()
    card = entry("Card number (16 digits):")
    cvv = entry("CVV (3-4 digits):", show="*")
    expiry = entry("Expiration (MM/YY):")

    def pay():
        if mode.get() == "Card":
            problem = card_problem(card.get(), cvv.get(), expiry.get())
            if problem:
                return messagebox.showerror("Invalid card details", problem)
            result = "Card payment processed successfully."   # card details are never saved
        elif mode.get() == "Bank Transfer":
            result = "Please transfer to Bank Account: XXXX-XXXX-XXXX and show the confirmation."
        else:
            result = "Payment recorded as Cash."
        messagebox.showinfo(
            "Payment",
            f"{result}\n\nReceipt No.: {receipt_no}\n"
            "Please present this receipt number to the counter after printing.")
        user_menu()

    button("Confirm Payment", pay)
    button("Back", billing_screen)


# --------------------------------------------------------------------- run ---
def start():
    home()
    window.mainloop()


if __name__ == "__main__":
    start()
