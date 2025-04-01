import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import hashlib
import os
import threading
import sys

# GitHub-Repository-Informationen
repo_owner = "Prot3ctiv"
repo_name = "update"

def starte_patch_vorgang():
    """Erstellt ein Fenster für den Patchvorgang mit Fortschrittsbalken."""
    print("starte_patch_vorgang() aufgerufen.")  # Debugging
    patch_fenster = tk.Tk()
    patch_fenster.title("Patchvorgang")
    patch_fenster.geometry("400x300")

    try:
        head_image = Image.open(os.path.join(os.path.dirname(__file__), "head3.png"))
        head_photo = ImageTk.PhotoImage(head_image)
        head_label = tk.Label(patch_fenster, image=head_photo)
        head_label.pack(pady=5)
    except FileNotFoundError:
        print("starte_patch_vorgang(): head3.png nicht gefunden.")  # Debugging

    status_label = tk.Label(patch_fenster, text="Patchvorgang wird gestartet...", fg="blue")
    status_label.pack(pady=10)

    fortschritt_var = tk.DoubleVar()
    fortschritt_balken = ttk.Progressbar(patch_fenster, variable=fortschritt_var, maximum=100)
    fortschritt_balken.pack(pady=10)

    def patch_thread():
        """Führt den Patchvorgang in einem separaten Thread aus."""
        print("patch_thread() aufgerufen.")  # Debugging
        try:
            # Erstelle patch.pid
            with open("patch.pid", "w") as f:
                f.write(str(os.getpid()))

            # Patchvorgang von GitHub
            repo_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents"
            response = requests.get(repo_url)
            response.raise_for_status()

            dateien = response.json()
            gesamt_dateien = 0
            for datei in dateien:
                if datei["type"] == "file" and datei["name"].endswith((".py", ".png", ".jpg", ".jpeg")):
                    gesamt_dateien +=1
            for i, datei in enumerate(dateien):
                if datei["type"] == "file" and datei["name"].endswith((".py", ".png", ".jpg", ".jpeg")):
                    datei_url = datei["download_url"]
                    datei_inhalt = requests.get(datei_url).content

                    lokale_datei_pfad = datei["name"]
                    if os.path.exists(lokale_datei_pfad):
                        with open(lokale_datei_pfad, "rb") as lokale_datei:
                            lokaler_inhalt = lokale_datei.read()
                            if hashlib.sha256(lokaler_inhalt).hexdigest() == hashlib.sha256(datei_inhalt).hexdigest():
                                continue
                    status_label.config(text=f"Lade {datei['name']} herunter...")
                    patch_fenster.update_idletasks()
                    with open(lokale_datei_pfad, "wb") as lokale_datei:
                        lokale_datei.write(datei_inhalt)
                    fortschritt = (i + 1) / gesamt_dateien * 100
                    fortschritt_var.set(fortschritt)
                    status_label.config(text=f"Aktualisiere {datei['name']} ({int(fortschritt)}%)")
                    patch_fenster.update_idletasks()  # UI aktualisieren

            print("patch_thread(): Patch-Vorgang abgeschlossen.")  # Debugging
            status_label.config(text="Patch-Vorgang abgeschlossen.")
            patch_fenster.after(2000, patch_fenster.destroy) # Fenster nach 2 Sekunden schließen

            # Lösche patch.pid
            os.remove("patch.pid")

        except requests.exceptions.RequestException as e:
            status_label.config(text=f"Fehler beim Patchvorgang: {e}")
            print(f"patch_thread(): Fehler beim Patchvorgang: {e}")  # Debugging
        except Exception as e:
            status_label.config(text=f"Unerwarteter Fehler: {e}")
            print(f"patch_thread(): Unerwarteter Fehler: {e}")  # Debugging

    threading.Thread(target=patch_thread).start()
    patch_fenster.mainloop()