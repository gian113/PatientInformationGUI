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
    "bg":        "#F4F7FA",   # window background
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
    button("Log In", lambda: None)
    button("Back", main_menu, "secondary")
    user.focus_set()

# User options/login


def user_menu():
    clear("User Menu")
    button("Billing", billing)
    button("Back", main_menu, "secondary")

# Main GUI


def main_menu():
    clear("Patient Information System")
    label("Choose how you want to sign in.")
    tk.Frame(content, bg=THEME["bg"], height=10).pack()
    button("ADMIN", admin)
    button("USER", user_menu)


main_menu()
root.mainloop()
