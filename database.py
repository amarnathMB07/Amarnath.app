import sqlite3
from pathlib import Path
import hashlib

DB_PATH = Path(__file__).parent / "agrosmart.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the tables if they don't exist and populate default crop data."""
    conn = get_connection()
    cur = conn.cursor()
    # users table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # crop table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS crops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            temp TEXT,
            water TEXT,
            harvest TEXT,
            season TEXT,
            fertilizer TEXT
        )
        """
    )

    # populate default crops if empty
    cur.execute("SELECT COUNT(*) AS cnt FROM crops")
    if cur.fetchone()["cnt"] == 0:
        default = [
            ("Wheat", "10-25", "Moderate", "120 days", "Winter/Spring", "Nitrogen-rich (urea) and phosphate fertilizers."),
            ("Corn", "18-27", "High", "90-120 days", "Spring/Summer", "Balanced NPK with extra nitrogen."),
            ("Rice", "20-35", "Very high", "120-150 days", "Summer/Monsoon", "Organic compost plus urea or DAP."),
            ("Tomato", "18-27", "Moderate", "60-85 days", "Summer", "High potassium and phosphorus fertilizers."),
            ("Soybean", "15-30", "Moderate", "80-120 days", "Summer", "Legume inoculants and low nitrogen (fixes its own)."),
        ]
        cur.executemany(
            "INSERT INTO crops (name, temp, water, harvest, season, fertilizer) VALUES (?, ?, ?, ?, ?, ?)",
            default,
        )
    conn.commit()
    conn.close()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_user(email: str, password: str) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            (email, hash_password(password)),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def authenticate_user(email: str, password: str) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM users WHERE email = ?", (email,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return False
    return row["password_hash"] == hash_password(password)


def get_crops():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM crops ORDER BY name")
    crops = [r["name"] for r in cur.fetchall()]
    conn.close()
    return crops


def get_crop_info(name: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT temp, water, harvest, season, fertilizer FROM crops WHERE name = ?",
        (name,),
    )
    row = cur.fetchone()
    conn.close()
    if row:
        return dict(row)
    return {}
