import time
from bild_erkennung import finde_bild, klicke_bild, warte_auf_bild, warte_und_klicke_bild
import threading
import pyautogui

# Globale Variablen
gatecheck_gefunden = False
inscheck_gefunden = False
huntercheck_gefunden = False
chascheck_gefunden = False
stop_bot = False

def kaufe_schluessel(key_typ, anzahl, status_callback):
    """Kauft Schlüssel eines bestimmten Typs."""
    if anzahl > 0:
        status_callback(f"Kaufe {anzahl} Schlüssel für {key_typ}")
        time.sleep(2)
        klicke_bild("buy.png", status_callback=status_callback)
        time.sleep(2)
        for _ in range(anzahl - 1):
            klicke_bild("buy1.png", status_callback=status_callback)
            time.sleep(1)
        time.sleep(2)
        klicke_bild("buy2.png", status_callback=status_callback)
        time.sleep(2)
        klicke_bild("dne.png", status_callback=status_callback)
        status_callback(f"{key_typ} Schlüssel gekauft")

def gatecheck_suche():
    """Sucht kontinuierlich nach gatecheck.png."""
    global gatecheck_gefunden
    while not gatecheck_gefunden and not stop_bot:  # Überprüfe stop_bot
        if finde_bild("gatecheck.png", schwellenwert=0.99):
            gatecheck_gefunden = True
        time.sleep(1)

def inscheck_suche():
    """Sucht kontinuierlich nach inscheck.png."""
    global inscheck_gefunden
    while not inscheck_gefunden and not stop_bot:  # Überprüfe stop_bot
        if finde_bild("inscheck.png", schwellenwert=0.99):
            inscheck_gefunden = True
        time.sleep(1)

def huntercheck_suche():
    """Sucht kontinuierlich nach huntercheck.png."""
    global huntercheck_gefunden
    while not huntercheck_gefunden and not stop_bot:  # Überprüfe stop_bot
        if finde_bild("huntercheck.png", schwellenwert=0.99):
            huntercheck_gefunden = True
        time.sleep(1)

def chascheck_suche():
    """Sucht kontinuierlich nach chascheck.png."""
    global chascheck_gefunden
    while not chascheck_gefunden and not stop_bot:  # Überprüfe stop_bot
        if finde_bild("chascheck.png", schwellenwert=0.99):
            chascheck_gefunden = True
        time.sleep(1)

def gate_daily(gate_auswahl, status_callback):
    """Führt den Gate Daily-Prozess aus und wiederholt ihn bei Debug-Modus."""
    while True:
        global gatecheck_gefunden
        gatecheck_gefunden = False

        time.sleep(2)
        if not warte_auf_bild("gates.png", status_callback):
            status_callback("Gate-Daily wird wiederholt...")
            continue
        klicke_bild("gates.png", status_callback=status_callback)

        if finde_bild("gatecheck.png", schwellenwert=0.99):
            time.sleep(2)
            klicke_bild("menu.png", status_callback=status_callback)
            time.sleep(2)
            klicke_bild("chapter.png", status_callback=status_callback)
            status_callback("Gate Daily abgeschlossen (Gatecheck gefunden)")
            return

        gate_bilder = {
            "GoldGate": "gate1.png",
            "RedGate": "gate2.png",
            "PurpleGate": "gate3.png",
            "BlueGate": "gate4.png"
        }

        gatecheck_thread = threading.Thread(target=gatecheck_suche)
        gatecheck_thread.daemon = True
        gatecheck_thread.start()

        while not gatecheck_gefunden and not stop_bot:
            gate_gefunden = False
            for gate_name, gate_bild in gate_bilder.items():
                if gate_name in gate_auswahl and finde_bild(gate_bild):
                    time.sleep(5)
                    klicke_bild(gate_bild, status_callback=status_callback)
                    time.sleep(2)
                    klicke_bild("gate5.png", status_callback=status_callback)
                    time.sleep(2)
                    klicke_bild("gate6.png", status_callback=status_callback)
                    warte_auf_bild("gate7.png", status_callback)
                    klicke_bild("gate7.png", status_callback=status_callback)
                    time.sleep(10)
                    gate_gefunden = True
                    break

            if gate_gefunden:
                if gatecheck_gefunden:
                    time.sleep(2)
                    klicke_bild("menu.png", status_callback=status_callback)
                    time.sleep(2)
                    klicke_bild("chapter.png", status_callback=status_callback)
                    status_callback("Gate Daily abgeschlossen (Gatecheck gefunden)")
                    return
            else:
                time.sleep(2)
                klicke_bild("gate8.png", status_callback=status_callback)
                time.sleep(2)
                if finde_bild("gate9.png"):
                    klicke_bild("gate9.png", status_callback=status_callback)
                    time.sleep(10)
                else:
                    klicke_bild("gate10.png", status_callback=status_callback)
                    time.sleep(10)

        if gatecheck_gefunden:
            time.sleep(2)
            klicke_bild("menu.png", status_callback=status_callback)
            time.sleep(2)
            klicke_bild("chapter.png", status_callback=status_callback)
            status_callback("Gate Daily abgeschlossen (Gatecheck gefunden)")
            return

def instanz_daily(category, equipment, status_callback):
    """Führt den Instanz-Daily-Prozess aus und wiederholt ihn bei Debug-Modus."""
    while True:
        global inscheck_gefunden
        inscheck_gefunden = False
        time.sleep(5)
        if category == "Armor":
            if not warte_und_klicke_bild("rep2.png", status_callback):
                status_callback("Instanz-Daily wird wiederholt...")
                continue
        else:
            if not warte_und_klicke_bild("rep1.png", status_callback):
                status_callback("Instanz-Daily wird wiederholt...")
                continue
        time.sleep(3)
        if finde_bild("inscheck.png", schwellenwert=0.99):
            time.sleep(3)
            klicke_bild("menu.png", status_callback=status_callback)
            time.sleep(3)
            klicke_bild("chapter.png", status_callback=status_callback)
            status_callback("Instanz-Daily abgeschlossen (inscheck gefunden)")
            return

        if equipment == "Boots+Hand":
            klicke_bild("ins1.png", -150, status_callback=status_callback)
        elif equipment == "Helmet+Armor":
            klicke_bild("ins2.png", -150, status_callback=status_callback)
        elif equipment == "Necklace+bracelet":
            klicke_bild("ins3.png", -150, status_callback=status_callback)
        elif equipment == "Earring+Ring":
            klicke_bild("ins4.png", -150, status_callback=status_callback)
        time.sleep(3)
        if finde_bild("inscheck.png", schwellenwert=0.99):
            time.sleep(3)
            klicke_bild("menu.png", status_callback=status_callback)
            time.sleep(3)
            klicke_bild("chapter.png", status_callback=status_callback)
            status_callback("Instanz-Daily abgeschlossen (inscheck gefunden)")
            return

        time.sleep(5)
        if finde_bild("inscheck.png", schwellenwert=0.99):
            time.sleep(3)
            klicke_bild("menu.png", status_callback=status_callback)
            time.sleep(3)
            klicke_bild("chapter.png", status_callback=status_callback)
            status_callback("Instanz-Daily abgeschlossen (inscheck gefunden)")
            return

        inscheck_thread = threading.Thread(target=inscheck_suche)
        inscheck_thread.daemon = True
        inscheck_thread.start()

        while True and not stop_bot:
            if inscheck_gefunden:
                time.sleep(3)
                klicke_bild("menu.png", status_callback=status_callback)
                time.sleep(3)
                klicke_bild("chapter.png", status_callback=status_callback)
                status_callback("Instanz-Daily abgeschlossen (inscheck gefunden)")
                return

            if finde_bild("ins6.png"):
                klicke_bild("ins6.png", status_callback=status_callback)
            else:
                klicke_bild("ins5.png", status_callback=status_callback)
            time.sleep(3)
            if finde_bild("inscheck.png", schwellenwert=0.99):
                time.sleep(3)
                klicke_bild("menu.png", status_callback=status_callback)
                time.sleep(3)
                klicke_bild("chapter.png", status_callback=status_callback)
                status_callback("Instanz-Daily abgeschlossen (inscheck gefunden)")
                return
            klicke_bild("ins7.png", status_callback=status_callback)
            time.sleep(3)
            if finde_bild("inscheck.png", schwellenwert=0.99):
                time.sleep(3)
                klicke_bild("menu.png", status_callback=status_callback)
                time.sleep(3)
                klicke_bild("chapter.png", status_callback=status_callback)
                status_callback("Instanz-Daily abgeschlossen (inscheck gefunden)")
                return
            klicke_bild("ins8.png", status_callback=status_callback)
            if not warte_auf_bild("gate7.png", status_callback):
                status_callback("Instanz-Daily wird wiederholt...")
                break # Starte die Wiederholung
            klicke_bild("gate7.png", status_callback=status_callback)
            time.sleep(10)

def hunter_daily(hunter_level, status_callback):
    """Führt den Hunter-Daily-Prozess aus und wiederholt ihn bei Debug-Modus."""
    while True:
        global huntercheck_gefunden
        huntercheck_gefunden = False

        time.sleep(3)
        if not warte_auf_bild("hunter.png", status_callback):
            status_callback("Hunter-Daily wird wiederholt...")
            continue
        klicke_bild("hunter.png", status_callback=status_callback)
        time.sleep(5)

        huntercheck_thread = threading.Thread(target=huntercheck_suche)
        huntercheck_thread.daemon = True
        huntercheck_thread.start()

        if huntercheck_gefunden:
            time.sleep(3)
            klicke_bild("menu.png", status_callback=status_callback)
            time.sleep(3)
            klicke_bild("chapter.png", status_callback=status_callback)
            status_callback("Hunter-Daily abgeschlossen (huntercheck gefunden)")
            return

        level_bilder = {
            "Level10": "hunter1.png",
            "Level25": "hunter2.png",
            "Level40": "hunter3.png",
            "Level55": "hunter4.png",
            "Level70": "hunter5.png",
            "Level75": "hunter6.png",
            "Level80": "hunter7.png"
        }

        if hunter_level in level_bilder:
            klicke_bild(level_bilder[hunter_level], status_callback=status_callback)
            time.sleep(3)
            klicke_bild("hunter8.png", status_callback=status_callback)
            warte_auf_bild("hunter9.png", status_callback)
            klicke_bild("hunter9.png", status_callback=status_callback)
            time.sleep(10)
        else:
            status_callback(f"Ungültiges Hunter-Level: {hunter_level}")
            return

        while True and not stop_bot:
            if huntercheck_gefunden:
                time.sleep(3)
                klicke_bild("menu.png", status_callback=status_callback)
                time.sleep(3)
                klicke_bild("chapter.png", status_callback=status_callback)
                status_callback("Hunter-Daily abgeschlossen (huntercheck gefunden)")
                return

            if hunter_level in level_bilder:
                klicke_bild(level_bilder[hunter_level], status_callback=status_callback)
                time.sleep(3)
                klicke_bild("hunter8.png", status_callback=status_callback)
                warte_auf_bild("hunter9.png", status_callback)
                klicke_bild("hunter9.png", status_callback=status_callback)
                time.sleep(10)
            else:
                status_callback(f"Ungültiges Hunter-Level: {hunter_level}")
                return

def chaos_daily(chaos_selection, status_callback):
    """Führt den Chaos-Daily-Prozess aus und wiederholt ihn bei Debug-Modus."""
    while True:
        global chascheck_gefunden
        chascheck_gefunden = False

        chascheck_thread = threading.Thread(target=chascheck_suche)
        chascheck_thread.daemon = True
        chascheck_thread.start()

        time.sleep(3)
        if not warte_auf_bild("chas.png", status_callback):
            status_callback("Chaos-Daily abgebrochen.")
            continue

        klicke_bild("chas.png", status_callback=status_callback)
        time.sleep(3)

        if chascheck_gefunden:
            time.sleep(3)
            klicke_bild("menu.png", status_callback=status_callback)
            time.sleep(3)
            klicke_bild("chapter.png", status_callback=status_callback)
            status_callback("Chaos-Daily abgeschlossen (chascheck gefunden)")
            return

        chas_bilder = ["chas1.png", "chas2.png", "chas3.png", "chas4.png", "chas5.png"]
        gefunden = False
        for bild in chas_bilder:
            if finde_bild(bild):
                klicke_bild(bild, status_callback=status_callback)
                gefunden = True
                time.sleep(3)
                break

        if not gefunden:
            status_callback("Keines der chas1-5 Bilder gefunden. Chaos-Daily abgebrochen.")
            continue

        if chascheck_gefunden:
            time.sleep(3)
            klicke_bild("menu.png", status_callback=status_callback)
            time.sleep(3)
            klicke_bild("chapter.png", status_callback=status_callback)
            status_callback("Chaos-Daily abgeschlossen (chascheck gefunden)")
            return

        # Hier die Logik für chas6.png basierend auf der Auswahl
        positionen = pyautogui.locateAllOnScreen("chas6.png")
        if positionen:
            try:
                if chaos_selection == "Yes":
                    rechts_position = max(positionen, key=lambda pos: pos.left)
                    pyautogui.click(rechts_position.left + rechts_position.width / 2, rechts_position.top + rechts_position.height / 2)
                else:
                    links_position = min(positionen, key=lambda pos: pos.left)
                    pyautogui.click(links_position.left + links_position.width / 2, links_position.top + links_position.height / 2)
            except ValueError:
                status_callback("Fehler beim Auswählen von chas6.png. Chaos-Daily abgebrochen.")
                continue
        else:
            status_callback("chas6.png nicht gefunden. Chaos-Daily abgebrochen.")
            continue

        time.sleep(3)
        klicke_bild("chas7.png", status_callback=status_callback)
        time.sleep(3)
        klicke_bild("chas8.png", status_callback=status_callback)
        if not warte_auf_bild("chas9.png", status_callback):
            status_callback("chas9.png nicht gefunden. Chaos-Daily abgebrochen.")
            continue
        klicke_bild("chas9.png", status_callback=status_callback)
        time.sleep(10)

        while True and not stop_bot:
            if chascheck_gefunden:
                time.sleep(3)
                klicke_bild("menu.png", status_callback=status_callback)
                time.sleep(3)
                klicke_bild("chapter.png", status_callback=status_callback)
                status_callback("Chaos-Daily abgeschlossen (chascheck gefunden)")
                return

            positionen = pyautogui.locateAllOnScreen("chas6.png")
            if positionen:
                try:
                    if chaos_selection == "Yes":
                        rechts_position = max(positionen, key=lambda pos: pos.left)
                        pyautogui.click(rechts_position.left + rechts_position.width / 2, rechts_position.top + rechts_position.height / 2)
                    else:
                        links_position = min(positionen, key=lambda pos: pos.left)
                        pyautogui.click(links_position.left + links_position.width / 2, links_position.top + links_position.height / 2)
                except ValueError:
                    status_callback("Fehler beim Auswählen von chas6.png. Chaos-Daily abgebrochen.")
                    return
            else:
                status_callback("chas6.png nicht gefunden. Chaos-Daily abgebrochen.")
                return

            time.sleep(3)
            klicke_bild("chas7.png", status_callback=status_callback)
            time.sleep(3)
            klicke_bild("chas8.png", status_callback=status_callback)
            if not warte_auf_bild("chas9.png", status_callback):
                status_callback("chas9.png nicht gefunden. Chaos-Daily abgebrochen.")
                return
            klicke_bild("chas9.png", status_callback=status_callback)
            time.sleep(10)
            klicke_bild("dne.png", status_callback=status_callback)
            time.sleep(3)

def gatemine_prozess(status_callback):
    """Führt den Gatemining-Prozess aus."""
    status_callback("Gatemining im Gange")
    time.sleep(3)
    warte_und_klicke_bild("gates.png", status_callback=status_callback)
    time.sleep(5)
    warte_und_klicke_bild("mine.png", status_callback=status_callback)

    while True:
        klicke_bild("mine2.png", status_callback=status_callback)
        time.sleep(3)
        klicke_bild("mine3.png", status_callback=status_callback)
        time.sleep(60)  # Warte 1 Minute