import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "trends.db"
HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 8000))
