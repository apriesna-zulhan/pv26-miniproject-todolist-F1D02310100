"""
database/db_manager.py
Modul untuk manajemen database SQLite.
Separation of Concerns: hanya menangani operasi database.
"""

import sqlite3
import os
from datetime import datetime


DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "todo.db")


def get_connection():
    """Membuka dan mengembalikan koneksi ke database SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Inisialisasi database dan buat tabel jika belum ada."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT    NOT NULL,
            description TEXT,
            category    TEXT    NOT NULL DEFAULT 'Umum',
            priority    TEXT    NOT NULL DEFAULT 'Sedang',
            due_date    TEXT,
            status      TEXT    NOT NULL DEFAULT 'Belum Selesai',
            created_at  TEXT    NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# CREATE 

def create_task(title: str, description: str, category: str,
                priority: str, due_date: str) -> int:
    """Menyimpan tugas baru. Mengembalikan id baris yang baru dibuat."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO tasks (title, description, category, priority, due_date, status, created_at)
           VALUES (?, ?, ?, ?, ?, 'Belum Selesai', ?)""",
        (title, description, category, priority, due_date,
         datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id


# READ 

def get_all_tasks(filter_status: str = "Semua", filter_category: str = "Semua",
                  filter_priority: str = "Semua") -> list[dict]:
    """Mengambil semua tugas dengan filter opsional."""
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM tasks WHERE 1=1"
    params = []

    if filter_status != "Semua":
        query += " AND status = ?"
        params.append(filter_status)
    if filter_category != "Semua":
        query += " AND category = ?"
        params.append(filter_category)
    if filter_priority != "Semua":
        query += " AND priority = ?"
        params.append(filter_priority)

    query += " ORDER BY created_at DESC"
    cursor.execute(query, params)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def get_task_by_id(task_id: int) -> dict | None:
    """Mengambil satu tugas berdasarkan id."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_statistics() -> dict:
    """Mengembalikan statistik ringkas untuk dashboard."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tasks")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'Selesai'")
    done = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'Belum Selesai'")
    pending = cursor.fetchone()[0]
    conn.close()
    return {"total": total, "done": done, "pending": pending}


# UPDATE
def update_task(task_id: int, title: str, description: str, category: str,
                priority: str, due_date: str) -> None:
    """Memperbarui data tugas yang sudah ada."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE tasks SET title=?, description=?, category=?, priority=?, due_date=?
           WHERE id=?""",
        (title, description, category, priority, due_date, task_id)
    )
    conn.commit()
    conn.close()


def toggle_status(task_id: int) -> str:
    """Membalik status tugas antara 'Selesai' dan 'Belum Selesai'. Mengembalikan status baru."""
    task = get_task_by_id(task_id)
    if task is None:
        return ""
    new_status = "Selesai" if task["status"] == "Belum Selesai" else "Belum Selesai"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status=? WHERE id=?", (new_status, task_id))
    conn.commit()
    conn.close()
    return new_status


# DELETE

def delete_task(task_id: int) -> None:
    """Menghapus tugas berdasarkan id."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
