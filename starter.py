import subprocess
import os
import time

# Starte key.py
subprocess.run(["python", "key.py"])

# Warte, bis patch.py abgeschlossen ist
while os.path.exists("patch.pid"):
    time.sleep(1)

# Starte start_bot.py
subprocess.run(["python", "start_bot.py"])