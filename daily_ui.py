import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import hashlib
import os
import json
import base64
import threading

# GitHub-Repository-Informationen
repo_owner = "Prot3ctiv"
repo_name = "auto"
file_path = "keys.json"
github_token = "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"  # Ersetzen Sie dies durch Ihr GitHub-Token

def lade_keys_von_online():
    """Lädt die Aktivierungskeys von der Online-Datei."""
    try:
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
        headers = {"Authorization": f"token {github_token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        content = response.json()["content"]
        decoded_content = base64.b64decode(content).decode('utf-8')
        return json.loads(decoded_content)
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Laden der Keys von der Online-Datei: {e}")
        return {"gültige_keys": [], "verwendete_keys": []}

def speichere_verwendete_keys(verwendete_keys):
    """Speichert die verwendeten Keys in der Online-Datei."""
    try:
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
        headers = {"Authorization": f"token {github_token}", "Content-Type": "application/json"}
        daten = {"gültige_keys": gültige_keys, "verwendete_keys": verwendete_keys}
        response = requests.put(url, headers=headers, json=daten)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Speichern der verwendeten Keys: {e}")

key_daten = lade_keys_von_online()
gültige_keys = key_daten["gültige_keys"]
verwendete_keys = key_daten["verwendete_keys"]

def speichere_lokalen_key(key):
    """Speichert den eingegebenen Key lokal."""
    try:
        with open("lokaler_key.txt", "w") as f:
            f.write(key)
    except Exception as e:
        print(f"Fehler beim Speichern des lokalen Keys: {e}")

def lade_lokalen_key():
    """Lädt den lokal gespeicherten Key."""
    try:
        with open("lokaler_key.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Fehler beim Laden des lokalen Keys: {e}")
        return None

def aktiviere_skript(key_eingabe_fenster, key_eingabe_feld, status_label):
    """Überprüft den Aktivierungskey, speichert ihn und startet den Patchvorgang."""
    key = key_eingabe_feld.get()
    if key in gültige_keys and key not in verwendete_keys:
        verwendete_keys.append(key)
        speichere_verwendete_keys(verwendete_keys)
        speichere_lokalen_key(key)
        key_eingabe_fenster.destroy()
        starte_patch_vorgang()
    else:
        status_label.config(text="Ungültiger oder bereits verwendeter Key.")

def starte_key_eingabe():
    """Erstellt ein Fenster zur Eingabe des Aktivierungskeys."""
    key_eingabe_fenster = tk.Tk()
    key_eingabe_fenster.title("Aktivierungskey")
    key_eingabe_fenster.geometry("300x350")

    try:
        head_image = Image.open(os.path.join(os.path.dirname(__file__), "head2.png"))
        head_photo = ImageTk.PhotoImage(head_image)
        head_label = tk.Label(key_eingabe_fenster, image=head_photo)
        head_label.pack(pady=5)
    except FileNotFoundError:
        print("head2.png not found.")

    style = ttk.Style()
    style.configure("TEntry", padding=5, font=("Helvetica", 12))
    style.configure("TButton", padding=5, font=("Helvetica", 12, "bold"), background="#800080", foreground="black")

    tk.Label(key_eingabe_fenster, text="Aktivierungskey eingeben:", font=("Helvetica", 12)).pack(pady=5)
    key_eingabe_feld = ttk.Entry(key_eingabe_fenster, width=25, style="TEntry")
    key_eingabe_feld.pack(pady=10)

    status_label = tk.Label(key_eingabe_fenster, text="", fg="red")
    status_label.pack(pady=5)

    ttk.Button(key_eingabe_fenster, text="Aktivieren", command=lambda: aktiviere_skript(key_eingabe_fenster, key_eingabe_feld, status_label), style="TButton").pack(pady=5)

    key_eingabe_fenster.mainloop()

def starte_patch_vorgang():
    """Erstellt ein Fenster für den Patchvorgang mit Fortschrittsbalken."""
    patch_fenster = tk.Tk()
    patch_fenster.title("Patchvorgang")
    patch_fenster.geometry("400x200")

    try:
        head_image = Image.open(os.path.join(os.path.dirname(__file__), "head3.png"))
        head_photo = ImageTk.PhotoImage(head_image)
        head_label = tk.Label(patch_fenster, image=head_photo)
        head_label.pack(pady=5)
    except FileNotFoundError:
        print("head3.png not found.")

    ttk.Label(patch_fenster, text="Updates werden heruntergeladen...", font=("Helvetica", 12)).pack(pady=10)

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(patch_fenster, variable=progress_var, maximum=100, length=300)
    progress_bar.pack(pady=10)

    def update_progress(wert):
        """Aktualisiert den Fortschrittsbalken."""
        progress_var.set(wert)
        patch_fenster.update_idletasks()

    def patch_thread():
        """Führt den Patchvorgang in einem separaten Thread aus."""
        try:
            repo_url = "https://api.github.com/repos/Prot3ctiv/update/contents"
            response = requests.get(repo_url)
            response.raise_for_status()

            dateien = response.json()
            total_dateien = len(dateien)
            geladene_dateien = 0

            for datei in dateien:
                if datei["type"] == "file" and datei["name"].endswith((".py", ".png", ".jpg", ".jpeg")):
                    datei_url = datei["download_url"]
                    datei_inhalt = requests.get(datei_url).content

                    lokale_datei_pfad = datei["name"]
                    if os.path.exists(lokale_datei_pfad):
                        with open(lokale_datei_pfad, "rb") as lokale_datei:
                            lokaler_inhalt = lokale_datei.read()
                            if hashlib.sha256(lokaler_inhalt).hexdigest() == hashlib.sha256(datei_inhalt).hexdigest():
                                geladene_dateien += 1
                                update_progress((geladene_dateien / total_dateien) * 100)
                                continue

                    with open(lokale_datei_pfad, "wb") as lokale_datei:
                        lokale_datei.write(datei_inhalt)
                    geladene_dateien += 1
                    update_progress((geladene_dateien / total_dateien) * 100)

            patch_fenster.destroy()
            starte_ui()  # Starte die UI nach erfolgreichem Patch

        except requests.exceptions.RequestException as e:
            print(f"Fehler beim Herunterladen der Updates: {e}")
            patch_fenster.destroy()
            starte_ui()
        except Exception as e:
            print(f"Unerwarteter Fehler: {e}")
            patch_fenster.destroy()
            starte_ui()

    threading.Thread(target=patch_thread).start()
    patch_fenster.mainloop()

def starte_bot():
    """Starts the Daily Bot with selected values."""
    gate_keys = gate_keys_var.get()
    replay_keys = replay_keys_var.get()
    hunter_keys = hunter_keys_var.get()
    chaos_keys = chaos_keys_var.get()
    gate_auswahl = [gate_name for gate_name, var in gate_vars.items() if var.get()]
    category = category_var.get()
    equipment = equipment_var.get()
    hunter_level = hunter_level_var.get()
    chaos_selection = chaos_selection_var.get()
    # daily.daily_bot(gate_keys, replay_keys, hunter_keys, chaos_keys, gate_auswahl, category, equipment, hunter_level, chaos_selection, aktualisiere_status)

def aktualisiere_status(status):
    """Updates the status display in the UI."""
    status_label.config(text=status)

def auto_update():
    """Checks and downloads updates from GitHub."""
    aktualisiere_status("Checking for updates...")
    try:
        repo_url = "https://api.github.com/repos/Prot3ctiv/update/contents"
        response = requests.get(repo_url)
        response.raise_for_status()

        dateien = response.json()
        for datei in dateien:
            if datei["type"] == "file" and datei["name"].endswith((".py", ".png", ".jpg", ".jpeg")):
                datei_url = datei["download_url"]
                datei_inhalt = requests.get(datei_url).content

                lokale_datei_pfad = datei["name"]
                if os.path.exists(lokale_datei_pfad):
                    with open(lokale_datei_pfad, "rb") as lokale_datei:
                        lokaler_inhalt = lokale_datei.read()
                        if hashlib.sha256(lokaler_inhalt).hexdigest() == hashlib.sha256(datei_inhalt).hexdigest():
                            continue

                with open(lokale_datei_pfad, "wb") as lokale_datei:
                    lokale_datei.write(datei_inhalt)
                aktualisiere_status(f"{datei['name']} updated")

        aktualisiere_status("You have the latest files")

    except requests.exceptions.RequestException as e:
        aktualisiere_status(f"Error downloading updates: {e}")
    except Exception as e:
        aktualisiere_status(f"Unexpected error: {e}")
        
def starte_ui():
    """Erstellt die Haupt-UI."""
    global root, status_label, gate_keys_var, replay_keys_var, hunter_keys_var, chaos_keys_var, gate_vars, category_var, equipment_var, hunter_level_var, chaos_selection_var

    # UI-Setup
    root = tk.Tk()
    root.title("Daily Bot")

    # Header-Bild
    try:
        head_image = Image.open(os.path.join(os.path.dirname(__file__), "head.png"))
        head_photo = ImageTk.PhotoImage(head_image)
        head_label = tk.Label(root, image=head_photo)
        head_label.pack(pady=10)
    except FileNotFoundError:
        print("head.png not found.")

    # Stil für Dropdowns
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TCombobox",
        fieldbackground="#f0f0f0",
        foreground="black",
        font=("Helvetica", 12),
        bordercolor="blue",
        borderwidth=1,
        padding=5,
        arrowcolor="blue")
    style.map("TCombobox",
        fieldbackground=[("readonly", "#f0f0f0")],
        foreground=[("readonly", "black")],
        selectbackground=[("readonly", "#f0f0f0")],
        selectforeground=[("readonly", "black")],
        arrowcolor=[("readonly", "blue")])

    # Stil für Buttons
    button_style = ttk.Style()
    button_style.configure("TButton",
        padding=10,
        font=("Helvetica", 12, "bold"),
        background="#4CAF50",
        foreground="white")

    # Frame für die Hauptinhalte
    main_frame = tk.Frame(root, padx=20, pady=20)
    main_frame.pack(padx=10, pady=10)

    # Dropdown-Menüs in einem Frame
    dropdown_frame = tk.Frame(main_frame)
    dropdown_frame.grid(row=0, column=0, columnspan=8, pady=10)

    # Dropdown-Menüs
    gate_keys_var = tk.IntVar(value=0)
    replay_keys_var = tk.IntVar(value=0)
    hunter_keys_var = tk.IntVar(value=0)
    chaos_keys_var = tk.IntVar(value=0)

    # Bilder für Dropdown-Menüs
    key_images = ["key1.png", "key2.png", "key3.png", "key4.png"]
    key_photos = []
    key_labels = []

    # Dropdown-Menüs und Labels mit Bildern
    ttk.Label(dropdown_frame, text="Gate Keys:").grid(row=0, column=1, padx=5)
    try:
        key_image = Image.open(os.path.join(os.path.dirname(__file__), "key1.png"))
        key_image = key_image.resize((32, 32), Image.LANCZOS)
        key_photo = ImageTk.PhotoImage(key_image)
        key_label = tk.Label(dropdown_frame, image=key_photo)
        key_label.image = key_photo
        key_label.grid(row=1, column=0, padx=5)
    except FileNotFoundError:
        print("key1.png not found.")
    ttk.Combobox(dropdown_frame, textvariable=gate_keys_var, values=list(range(11)), width=5, style="TCombobox", state="readonly").grid(row=1, column=1, padx=5)

    ttk.Label(dropdown_frame, text="Replay Keys:").grid(row=0, column=3, padx=5)
    try:
        key_image = Image.open(os.path.join(os.path.dirname(__file__), "key2.png"))
        key_image = key_image.resize((32, 32), Image.LANCZOS)
        key_photo = ImageTk.PhotoImage(key_image)
        key_label = tk.Label(dropdown_frame, image=key_photo)
        key_label.image = key_photo
        key_label.grid(row=1, column=2, padx=5)
    except FileNotFoundError:
        print("key2.png not found.")
    ttk.Combobox(dropdown_frame, textvariable=replay_keys_var, values=list(range(21)), width=5, style="TCombobox", state="readonly").grid(row=1, column=3, padx=5)

    ttk.Label(dropdown_frame, text="Hunter Archive Keys:").grid(row=0, column=5, padx=5)
    try:
        key_image = Image.open(os.path.join(os.path.dirname(__file__), "key3.png"))
        key_image = key_image.resize((32, 32), Image.LANCZOS)
        key_photo = ImageTk.PhotoImage(key_image)
        key_label = tk.Label(dropdown_frame, image=key_photo)
        key_label.image = key_photo
        key_label.grid(row=1, column=4, padx=5)
    except FileNotFoundError:
        print("key3.png not found.")
    ttk.Combobox(dropdown_frame, textvariable=hunter_keys_var, values=list(range(6)), width=5, style="TCombobox", state="readonly").grid(row=1, column=5, padx=5)

    ttk.Label(dropdown_frame, text="Chaos Keys:").grid(row=0, column=7, padx=5)
    try:
        key_image = Image.open(os.path.join(os.path.dirname(__file__), "key4.png"))
        key_image = key_image.resize((32, 32), Image.LANCZOS)
        key_photo = ImageTk.PhotoImage(key_image)
        key_label = tk.Label(dropdown_frame, image=key_photo)
        key_label.image = key_photo
        key_label.grid(row=1, column=6, padx=5)
    except FileNotFoundError:
        print("key4.png not found.")
    ttk.Combobox(dropdown_frame, textvariable=chaos_keys_var, values=list(range(6)), width=5, style="TCombobox", state="readonly").grid(row=1, column=7, padx=5)

    # Auto-Gate Setup
    ttk.Label(main_frame, text="Auto-Gate Setup", font=("Helvetica", 14, "bold")).grid(row=1, column=0, columnspan=2, pady=10)

    gate_frame = tk.Frame(main_frame)
    gate_frame.grid(row=2, column=0, columnspan=2, pady=5)

    gate_vars = {
        "GoldGate": tk.BooleanVar(),
        "RedGate": tk.BooleanVar(),
        "PurpleGate": tk.BooleanVar(),
        "BlueGate": tk.BooleanVar()
    }

    # Gate-Checkbuttons und Bilder
    gate_images = ["gg1.png", "gg2.png", "gg3.png", "gg4.png"]
    for i, (gate_name, var) in enumerate(gate_vars.items()):
        tk.Checkbutton(gate_frame, text="", variable=var).grid(row=0, column=i * 2, padx=5)
        try:
            gate_image = Image.open(os.path.join(os.path.dirname(__file__), gate_images[i]))
            gate_image = gate_image.resize((32, 32), Image.LANCZOS)
            gate_photo = ImageTk.PhotoImage(gate_image)
            gate_label = tk.Label(gate_frame, image=gate_photo)
            gate_label.image = gate_photo
            gate_label.grid(row=0, column=i * 2 + 1, padx=5)
        except FileNotFoundError:
            print(f"{gate_images[i]} not found.")

    # Instanz-Daily Setup
    ttk.Label(main_frame, text="Instance-Daily Setup", font=("Helvetica", 14, "bold")).grid(row=1, column=2, columnspan=2, pady=10)

    instanz_frame = tk.Frame(main_frame)
    instanz_frame.grid(row=2, column=2, columnspan=2, pady=5)

    ttk.Label(instanz_frame, text="Category:").grid(row=0, column=0, padx=5)
    category_var = tk.StringVar(value="Armor")
    ttk.Combobox(instanz_frame, textvariable=category_var, values=["Armor", "Accessories"], width=15, style="TCombobox", state="readonly").grid(row=1, column=0, padx=5)

    ttk.Label(instanz_frame, text="Equipment:").grid(row=0, column=1, padx=5)
    equipment_var = tk.StringVar(value="Boots+Hand")
    ttk.Combobox(instanz_frame, textvariable=equipment_var, values=["Boots+Hand", "Helmet+Armor", "Necklace+bracelet", "Earring+Ring"], width=15, style="TCombobox", state="readonly").grid(row=1, column=1, padx=5)

    # Hunter-Setup
    ttk.Label(main_frame, text="Hunter Setup", font=("Helvetica", 14, "bold")).grid(row=3, column=0, columnspan=2, pady=10)

    hunter_frame = tk.Frame(main_frame)
    hunter_frame.grid(row=4, column=0, columnspan=2, pady=5)

    ttk.Label(hunter_frame, text="Level:").grid(row=0, column=0, padx=5)
    hunter_level_var = tk.StringVar(value="Level10")
    ttk.Combobox(hunter_frame, textvariable=hunter_level_var, values=["Level10", "Level25", "Level40", "Level55", "Level70", "Level75", "Level80"], width=15, style="TCombobox", state="readonly").grid(row=1, column=0, padx=5)

    # Chaos-Setup
    ttk.Label(main_frame, text="Chaos Setup", font=("Helvetica", 14, "bold")).grid(row=3, column=2, columnspan=2, pady=10)

    chaos_frame = tk.Frame(main_frame)
    chaos_frame.grid(row=4, column=2, columnspan=2, pady=5)

    ttk.Label(chaos_frame, text="Chaos:").grid(row=0, column=0, padx=5)
    chaos_selection_var = tk.StringVar(value="Yes")
    ttk.Combobox(chaos_frame, textvariable=chaos_selection_var, values=["Yes", "No"], width=5, style="TCombobox", state="readonly").grid(row=1, column=0, padx=5)

    # Buttons
    update_button = ttk.Button(main_frame, text="Check for Updates", command=auto_update, style="TButton")
    update_button.grid(row=5, column=0, columnspan=2, pady=10)

    start_button = ttk.Button(main_frame, text="Start", command=starte_bot, style="TButton")
    start_button.grid(row=5, column=2, columnspan=2, pady=10)

    # Statusanzeige
    status_frame = tk.Frame(main_frame, bg="black")
    status_frame.grid(row=6, column=0, columnspan=4, sticky="ew", padx=10, pady=10)

    status_label = tk.Label(status_frame, text="", fg="white", bg="black", font=("Helvetica", 12, "bold"))
    status_label.pack(fill=tk.X)

    root.mainloop()

# Überprüfe, ob ein lokaler Key vorhanden ist
lokaler_key = lade_lokalen_key()
if lokaler_key and lokaler_key in gültige_keys and lokaler_key not in verwendete_keys:
    # Starte direkt den Patchvorgang, wenn ein gültiger Key vorhanden ist
    verwendete_keys.append(lokaler_key)
    speichere_verwendete_keys(verwendete_keys)
    starte_patch_vorgang()
else:
    # Starte die Key-Eingabe, wenn kein gültiger Key vorhanden ist
    starte_key_eingabe()