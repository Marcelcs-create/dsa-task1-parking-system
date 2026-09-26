import sqlite3
from datetime import datetime, date

DB_PATH = "parking.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(total_slots=10):
    conn = get_connection()
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS vehicles (
        vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
        plate_number TEXT UNIQUE NOT NULL,
        vehicle_type TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS slots (
        slot_id INTEGER PRIMARY KEY AUTOINCREMENT,
        slot_number TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'FREE',
        zone TEXT
    );

    CREATE TABLE IF NOT EXISTS rates (
        rate_id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_type TEXT NOT NULL,
        rate_per_hour REAL NOT NULL,
        effective_date TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS tickets (
        ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_id INTEGER NOT NULL,
        slot_id INTEGER NOT NULL,
        entry_time TEXT NOT NULL,
        exit_time TEXT,
        amount_due REAL,
        status TEXT NOT NULL DEFAULT 'PARKED',
        FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id),
        FOREIGN KEY (slot_id) REFERENCES slots(slot_id)
    );

    CREATE TABLE IF NOT EXISTS payments (
        payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id INTEGER NOT NULL,
        amount_paid REAL NOT NULL,
        payment_method TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id)
    );

    CREATE TABLE IF NOT EXISTS verification_logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id INTEGER NOT NULL,
        entry_plate TEXT NOT NULL,
        exit_plate TEXT NOT NULL,
        match_result TEXT NOT NULL,
        checked_at TEXT NOT NULL,
        FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id)
    );
    """)

    cur.execute("SELECT COUNT(*) FROM slots")
    if cur.fetchone()[0] == 0:
        for i in range(1, total_slots + 1):
            zone = "A" if i <= total_slots / 2 else "B"
            cur.execute(
                "INSERT INTO slots (slot_number, status, zone) VALUES (?, 'FREE', ?)",
                (f"S{i:02d}", zone),
            )

    cur.execute("SELECT COUNT(*) FROM rates")
    if cur.fetchone()[0] == 0:
        today = date.today().isoformat()
        cur.execute(
            "INSERT INTO rates (vehicle_type, rate_per_hour, effective_date) VALUES (?, ?, ?)",
            ("car", 50.0, today),
        )
        cur.execute(
            "INSERT INTO rates (vehicle_type, rate_per_hour, effective_date) VALUES (?, ?, ?)",
            ("motorcycle", 20.0, today),
        )

    conn.commit()
    conn.close()


def get_rate_for(vehicle_type: str) -> float:
    conn = get_connection()
    row = conn.execute(
        "SELECT rate_per_hour FROM rates WHERE vehicle_type = ? "
        "ORDER BY effective_date DESC LIMIT 1",
        (vehicle_type,),
    ).fetchone()
    conn.close()
    if row is None:
        return 50.0  # fallback default rate
    return row["rate_per_hour"]


def now_str() -> str:
    return datetime.now().isoformat(timespec="seconds")
