from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "trends.db"
HOST = "127.0.0.1"
PORT = 8000
