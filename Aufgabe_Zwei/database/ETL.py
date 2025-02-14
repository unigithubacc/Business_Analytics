import subprocess
import os

etl_folder = "ETL"  # Ordner mit den Skripten
scripts = ["days.py", "weeks.py", "person.py", "combined.py"]  # person.py ist jetzt dabei

for script in scripts:
    script_path = os.path.join(etl_folder, script)  # Erzeugt den Pfad zum Skript
    try:
        print(f"Starte {script}...")
        result = subprocess.run(["python", script_path], check=True, capture_output=True, text=True)

        # Ausgabe des Skripts anzeigen
        print(f"Ausgabe von {script}:\n{result.stdout}")

        print(f"{script} erfolgreich ausgeführt.\n")

    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Ausführen von {script}: {e}")
        print(f"Fehlermeldung: {e.stderr}")
        break  # Stoppt die Ausführung, falls ein Fehler auftritt
