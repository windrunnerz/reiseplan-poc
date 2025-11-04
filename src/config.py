from pathlib import Path
import os

# 📁 Projektroot = eine Ebene über src/
BASE_DIR = Path(__file__).resolve().parents[1]

# 📂 Standardordner für Daten, Templates, Static-Files
DATA_DIR = BASE_DIR / "data"
TEMPLATE_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

# 📄 Standarddateien
DEFAULT_FILE = DATA_DIR / "bausteine.json"
DEMO_FILE = DATA_DIR / "bausteine_demo.json"

# 🌐 Laufzeitsteuerung über Umgebungsvariable
# z. B.: $env:BAUSTEINE_FILE="data/bausteine.json"
BAUSTEINE_FILE = os.getenv("BAUSTEINE_FILE", str(DEMO_FILE))

# 📌 Vollständiger Pfad zur aktiven Datenquelle
DATA_FILE = BASE_DIR / BAUSTEINE_FILE

# Optional: Debug-Ausgabe bei Bedarf
if __name__ == "__main__":
    print(f"BASE_DIR:      {BASE_DIR}")
    print(f"DATA_DIR:      {DATA_DIR}")
    print(f"BAUSTEINE_FILE: {BAUSTEINE_FILE}")
    print(f"DATA_FILE:     {DATA_FILE}")
