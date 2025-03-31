import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import daily

def starte_bot():
    """Startet den Daily-Bot mit den ausgewählten Werten."""
    gate_keys = gate_keys_var.get()
    replay_keys = replay_keys_var.get()
    hunter_keys = hunter_keys_var.get()
    chaos_keys = chaos_keys_var.get()
    gate_auswahl = [gate_name for gate_name, var in gate_vars.items() if var.get()]
    category = category_var.get()
    equipment = equipment_var.get()
    hunter_level = hunter_level_var.get()
    chaos_selection = chaos_selection_var.get()
    daily.daily_bot(gate_keys, replay_keys, hunter_keys, chaos_keys, gate_auswahl, category, equipment, hunter_level, chaos_selection, aktualisiere_status)

def aktualisiere_status(status):
    """Aktualisiert die Statusanzeige in der UI."""
    status_label.config(text=status)

# UI-Setup
root = tk.Tk()
root.title("Daily Bot")
root.configure(bg="#282828")

# Header-Bild
try:
    head_image = Image.open("head.png")
    head_photo = ImageTk.PhotoImage(head_image)
    head_label = tk.Label(root, image=head_photo, bg="#282828")
    head_label.pack(pady=10)
except FileNotFoundError:
    print("head.png nicht gefunden.")

# Titel
title_label = tk.Label(root, text="Wie viele Keys möchtest du kaufen?", font=("Helvetica", 16, "bold"), fg="white", bg="#282828")
title_label.pack(pady=10)

# Frame für Dropdowns
dropdown_frame = tk.Frame(root, bg="#282828")
dropdown_frame.pack(pady=10)

# Dropdown-Menüs
gate_keys_var = tk.IntVar(value=0)
replay_keys_var = tk.IntVar(value=0)
hunter_keys_var = tk.IntVar(value=0)
chaos_keys_var = tk.IntVar(value=0)

# Stil für Dropdowns
style = ttk.Style()
style.theme_use("clam")

style.configure("TCombobox",
                fieldbackground="#282828",
                foreground="white",
                font=("Helvetica", 12, "bold"),
                bordercolor="blue",
                borderwidth=1,
                padding=5,
                arrowcolor="blue")

style.map("TCombobox",
          fieldbackground=[("readonly", "#282828")],
          foreground=[("readonly", "white")],
          selectbackground=[("readonly", "#282828")],
          selectforeground=[("readonly", "white")],
          arrowcolor=[("readonly", "blue")])

# Gate-Keys
gate_label = tk.Label(dropdown_frame, text="Gate-Keys:", fg="white", bg="#282828")
gate_label.grid(row=0, column=0, padx=5)
gate_dropdown = ttk.Combobox(dropdown_frame, textvariable=gate_keys_var, values=list(range(11)), width=5, style="TCombobox", state="readonly")
gate_dropdown.grid(row=1, column=0, padx=5)
gate_dropdown.config(font=("Helvetica", 12))

# Replay-Keys
replay_label = tk.Label(dropdown_frame, text="Replay-Keys:", fg="white", bg="#282828")
replay_label.grid(row=0, column=1, padx=5)
replay_dropdown = ttk.Combobox(dropdown_frame, textvariable=replay_keys_var, values=list(range(21)), width=5, style="TCombobox", state="readonly")
replay_dropdown.grid(row=1, column=1, padx=5)
replay_dropdown.config(font=("Helvetica", 12))

# Hunter-Archiv-Keys
hunter_label = tk.Label(dropdown_frame, text="Hunter-Archiv-Keys:", fg="white", bg="#282828")
hunter_label.grid(row=0, column=2, padx=5)
hunter_dropdown = ttk.Combobox(dropdown_frame, textvariable=hunter_keys_var, values=list(range(6)), width=5, style="TCombobox", state="readonly")
hunter_dropdown.grid(row=1, column=2, padx=5)
hunter_dropdown.config(font=("Helvetica", 12))

# Chaos-Keys
chaos_label = tk.Label(dropdown_frame, text="Chaos-Keys:", fg="white", bg="#282828")
chaos_label.grid(row=0, column=3, padx=5)
chaos_dropdown = ttk.Combobox(dropdown_frame, textvariable=chaos_keys_var, values=list(range(6)), width=5, style="TCombobox", state="readonly")
chaos_dropdown.grid(row=1, column=3, padx=5)
chaos_dropdown.config(font=("Helvetica", 12))

# Auto-Gate Setup
gate_setup_label = tk.Label(root, text="Auto-Gate Setup", font=("Helvetica", 14, "bold"), fg="white", bg="#282828")
gate_setup_label.pack(pady=10)

gate_frame = tk.Frame(root, bg="#282828")
gate_frame.pack(pady=5)

gate_vars = {
    "GoldGate": tk.BooleanVar(),
    "RedGate": tk.BooleanVar(),
    "PurpleGate": tk.BooleanVar(),
    "BlueGate": tk.BooleanVar()
}

for i, (gate_name, var) in enumerate(gate_vars.items()):
    gate_checkbutton = tk.Checkbutton(gate_frame, text=gate_name, variable=var, fg="white", bg="#282828", selectcolor="black")
    gate_checkbutton.grid(row=0, column=i, padx=5)

# Instanz-Daily Setup
instanz_setup_label = tk.Label(root, text="Instanz-Daily Setup", font=("Helvetica", 14, "bold"), fg="white", bg="#282828")
instanz_setup_label.pack(pady=10)

instanz_frame = tk.Frame(root, bg="#282828")
instanz_frame.pack(pady=5)

# Kategorie-Auswahl
category_label = tk.Label(instanz_frame, text="Kategorie:", fg="white", bg="#282828")
category_label.grid(row=0, column=0, padx=5)
category_var = tk.StringVar(value="Armor")
category_dropdown = ttk.Combobox(instanz_frame, textvariable=category_var, values=["Armor", "Accessoires"], width=15, style="TCombobox", state="readonly")
category_dropdown.grid(row=1, column=0, padx=5)
category_dropdown.config(font=("Helvetica", 12))

# Ausrüstung-Auswahl
equipment_label = tk.Label(instanz_frame, text="Ausrüstung:", fg="white", bg="#282828")
equipment_label.grid(row=0, column=1, padx=5)
equipment_var = tk.StringVar(value="Boots+Hand")
equipment_dropdown = ttk.Combobox(instanz_frame, textvariable=equipment_var, values=["Boots+Hand", "Helmet+Armor", "Necklace+bracelet", "Earring+Ring"], width=15, style="TCombobox", state="readonly")
equipment_dropdown.grid(row=1, column=1, padx=5)
equipment_dropdown.config(font=("Helvetica", 12))

# Hunter-Setup
hunter_setup_label = tk.Label(root, text="Hunter-Setup", font=("Helvetica", 14, "bold"), fg="white", bg="#282828")
hunter_setup_label.pack(pady=10)

hunter_frame = tk.Frame(root, bg="#282828")
hunter_frame.pack(pady=5)

hunter_level_label = tk.Label(hunter_frame, text="Level:", fg="white", bg="#282828")
hunter_level_label.grid(row=0, column=0, padx=5)
hunter_level_var = tk.StringVar(value="Level10")
hunter_level_dropdown = ttk.Combobox(hunter_frame, textvariable=hunter_level_var, values=["Level10", "Level25", "Level40", "Level55", "Level70", "Level75", "Level80"], width=15, style="TCombobox", state="readonly")
hunter_level_dropdown.grid(row=1, column=0, padx=5)
hunter_level_dropdown.config(font=("Helvetica", 12))

# Chaos-Setup
chaos_setup_label = tk.Label(root, text="Chaos-Setup", font=("Helvetica", 14, "bold"), fg="white", bg="#282828")
chaos_setup_label.pack(pady=10)

chaos_frame = tk.Frame(root, bg="#282828")
chaos_frame.pack(pady=5)

chaos_selection_label = tk.Label(chaos_frame, text="Chaos:", fg="white", bg="#282828")
chaos_selection_label.grid(row=0, column=0, padx=5)
chaos_selection_var = tk.StringVar(value="Yes")
chaos_selection_dropdown = ttk.Combobox(chaos_frame, textvariable=chaos_selection_var, values=["Yes", "No"], width=5, style="TCombobox", state="readonly")
chaos_selection_dropdown.grid(row=1, column=0, padx=5)
chaos_selection_dropdown.config(font=("Helvetica", 12))

# Start-Button
start_button = tk.Button(root, text="Start", command=starte_bot, bg="#0080ff", fg="white", font=("Helvetica", 12))
start_button.pack(pady=20)

# Statusanzeige
status_frame = tk.Frame(root, bg="black")
status_frame.pack(fill=tk.X, padx=10, pady=10)

status_label = tk.Label(status_frame, text="", fg="white", bg="black", font=("Helvetica", 12, "bold"))
status_label.pack(fill=tk.X)

root.mainloop()