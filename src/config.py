from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent

DEFAULT_FILE = "data/bausteine.json"
DEMO_FILE = "data/bausteine_demo.json"

# Über Umgebungsvariable steuerbar
BAUSTEINE_FILE = os.getenv("BAUSTEINE_FILE", DEMO_FILE)

DATA_FILE = BASE_DIR / BAUSTEINE_FILE
