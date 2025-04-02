import time
from bild_erkennung import finde_bild

# Globale Variablen
gatecheck_gefunden = False
inscheck_gefunden = False
huntercheck_gefunden = False
chascheck_gefunden = False
stop_bot = False

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