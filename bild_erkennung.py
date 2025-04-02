import pyautogui
import time
import cv2
import numpy as np

def finde_bild(bild_pfad, schwellenwert=0.8):
    """Findet die Position eines Bildes auf dem Bildschirm."""
    screenshot = pyautogui.screenshot()
    screenshot_cv2 = np.array(screenshot)
    screenshot_cv2 = cv2.cvtColor(screenshot_cv2, cv2.COLOR_RGB2BGR)

    vorlage = cv2.imread(bild_pfad)
    ergebnis = cv2.matchTemplate(screenshot_cv2, vorlage, cv2.TM_CCOEFF_NORMED)
    min_wert, max_wert, min_position, max_position = cv2.minMaxLoc(ergebnis)

    if max_wert > schwellenwert:
        mitte_x = max_position[0] + vorlage.shape[1] // 2
        mitte_y = max_position[1] + vorlage.shape[0] // 2
        return mitte_x, mitte_y
    return None

def klicke_bild(bild_pfad, offset_y=0, status_callback=None):
    """Bewegt die Maus auf das Bild, wartet 1 Sekunde und klickt dann zweimal."""
    if status_callback:
        status_callback(f"Klicke auf Bild: {bild_pfad}")
    position = finde_bild(bild_pfad)
    if position:
        x, y = position
        pyautogui.moveTo(x, y + offset_y, duration=0.25)  # Sanfte Bewegung
        time.sleep(1)
        pyautogui.doubleClick(x, y + offset_y)
        return True
    return False

def warte_auf_bild(bild_pfad, status_callback):
    """Wartet, bis ein Bild gefunden wird, mit Debug-Modus nach 240 Sekunden."""
    status_callback(f"Warte auf {bild_pfad}")
    start_time = time.time()
    while True:
        if finde_bild(bild_pfad):
            return True
        if time.time() - start_time > 240:
            status_callback("Debug-Modus aktiviert (240 Sekunden Wartezeit)")
            klicke_bild("dne.png", status_callback=status_callback)
            klicke_bild("dne2.png", status_callback=status_callback)
            klicke_bild("dne3.png", status_callback=status_callback)
            klicke_bild("dne4.png", status_callback=status_callback)
            time.sleep(3)
            klicke_bild("menu.png", status_callback=status_callback)
            time.sleep(3)
            klicke_bild("chapter.png", status_callback=status_callback)
            return False  # Gibt False zurück, um Wiederholung zu signalisieren
        time.sleep(1)

def warte_und_klicke_bild(bild_pfad, status_callback, offset_y=0):
    """Wartet, bis ein Bild gefunden wird, und klickt dann darauf."""
    status_callback(f"Warte auf {bild_pfad} und klicke")
    while True:
        if warte_auf_bild(bild_pfad, status_callback):
            klicke_bild(bild_pfad, offset_y, status_callback)
            return True
        # warte_auf_bild hat Debug-Modus ausgelöst, Wiederholung wird in spiel_aktionen.py gehandhabt