import threading
import time
from spiel_aktionen import gate_daily, instanz_daily, hunter_daily, chaos_daily, kaufe_schluessel
from bild_erkennung import klicke_bild, warte_und_klicke_bild
from bild_suche_threads import gatecheck_suche, inscheck_suche, huntercheck_suche, chascheck_suche

def daily_bot(gate_keys, replay_keys, hunter_keys, chaos_keys, gate_auswahl, category, equipment, hunter_level, chaos_selection, status_callback):
    """Führt den Daily-Bot in einem separaten Thread aus."""
    def bot_thread():
        global gatecheck_gefunden, inscheck_gefunden, huntercheck_gefunden, chascheck_gefunden, stop_bot
        gatecheck_gefunden = False
        inscheck_gefunden = False
        huntercheck_gefunden = False
        chascheck_gefunden = False
        stop_bot = False  # Setze stop_bot auf False am Anfang

        time.sleep(2)
        klicke_bild("menu.png", status_callback=status_callback)
        time.sleep(2)
        klicke_bild("chapter.png", status_callback=status_callback)

        if gate_keys > 0:
            warte_und_klicke_bild("gates.png", status_callback)
            kaufe_schluessel("Gate", gate_keys, status_callback)
            time.sleep(2)
            time.sleep(2)
            klicke_bild("menu.png", status_callback=status_callback)
            time.sleep(2)
            klicke_bild("chapter.png", status_callback=status_callback)

        if replay_keys > 0:
            warte_und_klicke_bild("rep1.png", status_callback)
            kaufe_schluessel("Replay", replay_keys, status_callback)
            time.sleep(2)
            time.sleep(2)
            klicke_bild("menu.png", status_callback=status_callback)
            time.sleep(2)
            klicke_bild("chapter.png", status_callback=status_callback)

        if hunter_keys > 0:
            warte_und_klicke_bild("hunter.png", status_callback)
            kaufe_schluessel("Hunter-Archiv", hunter_keys, status_callback)
            time.sleep(2)
            time.sleep(2)
            klicke_bild("menu.png", status_callback=status_callback)
            time.sleep(2)
            klicke_bild("chapter.png", status_callback=status_callback)

        if chaos_keys > 0:
            warte_und_klicke_bild("chas.png", status_callback)
            kaufe_schluessel("Chaos", chaos_keys, status_callback)
            time.sleep(2)
            time.sleep(2)
            klicke_bild("menu.png", status_callback=status_callback)
            time.sleep(2)
            klicke_bild("chapter.png", status_callback=status_callback)

        gate_daily(gate_auswahl, status_callback)
        instanz_daily(category, equipment, status_callback)
        hunter_daily(hunter_level, status_callback)
        chaos_daily(chaos_selection, status_callback)

        status_callback("Tägliche Aufgaben abgeschlossen")

    threading.Thread(target=bot_thread).start()