# services/database.py
import sqlite3
from config import DB_FILE

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sarcini (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titlu TEXT NOT NULL,
            prioritate TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def obtine_sarcini_din_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM sarcini 
        ORDER BY done ASC, 
        CASE prioritate 
            WHEN 'mare' THEN 1 
            WHEN 'medie' THEN 2 
            WHEN 'mica' THEN 3 
            ELSE 4 
        END ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def adauga_sarcina_db(titlu: str, prioritate: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sarcini (titlu, prioritate, done) VALUES (?, ?, ?)",
        (titlu, prioritate, False)
    )
    conn.commit()
    conn.close()

def bifeaza_sarcina_db(sarcina_id: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE sarcini SET done = NOT done WHERE id = ?", (sarcina_id,))
    conn.commit()
    conn.close()

def sterge_sarcina_db(sarcina_id: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sarcini WHERE id = ?", (sarcina_id,))
    conn.commit()
    conn.close()