"""
logic/task_controller.py
Lapisan logika bisnis aplikasi To-Do List.
Separation of Concerns: tidak menyentuh UI maupun SQL secara langsung.
"""

from database import db_manager

CATEGORIES = ["Umum", "Kuliah", "Pribadi", "Kerja", "Belanja", "Kesehatan"]
PRIORITIES  = ["Rendah", "Sedang", "Tinggi"]
STATUSES    = ["Semua", "Belum Selesai", "Selesai"]


def initialize():
    """Panggil saat aplikasi pertama kali dibuka."""
    db_manager.init_db()


# Operasi tugas 

def add_task(title: str, description: str, category: str,
             priority: str, due_date: str) -> tuple[bool, str]:
    """Validasi input lalu simpan tugas baru.
    Mengembalikan (sukses, pesan)."""
    title = title.strip()
    if not title:
        return False, "Judul tugas tidak boleh kosong."
    if len(title) > 100:
        return False, "Judul tugas maksimal 100 karakter."
    if category not in CATEGORIES:
        return False, f"Kategori tidak valid: {category}"
    if priority not in PRIORITIES:
        return False, f"Prioritas tidak valid: {priority}"

    db_manager.create_task(title, description.strip(), category, priority, due_date)
    return True, f"Tugas '{title}' berhasil ditambahkan."


def edit_task(task_id: int, title: str, description: str, category: str,
              priority: str, due_date: str) -> tuple[bool, str]:
    """Validasi lalu perbarui tugas yang ada."""
    title = title.strip()
    if not title:
        return False, "Judul tugas tidak boleh kosong."
    if len(title) > 100:
        return False, "Judul tugas maksimal 100 karakter."

    task = db_manager.get_task_by_id(task_id)
    if task is None:
        return False, "Tugas tidak ditemukan."

    db_manager.update_task(task_id, title, description.strip(), category, priority, due_date)
    return True, f"Tugas '{title}' berhasil diperbarui."


def remove_task(task_id: int) -> tuple[bool, str]:
    """Hapus tugas berdasarkan id."""
    task = db_manager.get_task_by_id(task_id)
    if task is None:
        return False, "Tugas tidak ditemukan."
    db_manager.delete_task(task_id)
    return True, f"Tugas '{task['title']}' berhasil dihapus."


def toggle_task_status(task_id: int) -> tuple[bool, str]:
    """Balik status selesai / belum selesai."""
    new_status = db_manager.toggle_status(task_id)
    if not new_status:
        return False, "Tugas tidak ditemukan."
    return True, f"Status diubah menjadi '{new_status}'."


# Pengambilan data

def fetch_tasks(filter_status: str = "Semua",
                filter_category: str = "Semua",
                filter_priority: str = "Semua") -> list[dict]:
    return db_manager.get_all_tasks(filter_status, filter_category, filter_priority)


def fetch_task(task_id: int) -> dict | None:
    return db_manager.get_task_by_id(task_id)


def fetch_statistics() -> dict:
    return db_manager.get_statistics()
