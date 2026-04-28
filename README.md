# 📋 To-Do List App

Aplikasi manajemen tugas harian berbasis GUI desktop yang dibangun menggunakan **PySide6** dan **Python**, dengan penyimpanan data permanen menggunakan **SQLite**.

---

## 📝 Deskripsi

To-Do List App memungkinkan pengguna untuk mengelola tugas sehari-hari secara terstruktur. Setiap tugas dapat dilengkapi dengan judul, deskripsi, kategori, tingkat prioritas, dan tenggat waktu. Data tersimpan secara otomatis ke database lokal sehingga tetap ada meskipun aplikasi ditutup.

Aplikasi ini dikembangkan sebagai project akhir mata kuliah **Pemrograman Berbasis Objek**, menerapkan prinsip **Separation of Concerns (SoC)** dengan memisahkan lapisan UI, logika bisnis, database, dan styling ke modul yang berbeda.

---

## ✨ Fitur Utama

- **Tambah, Edit, Hapus Tugas** — dengan form dialog terpisah dan konfirmasi sebelum menghapus
- **Ubah Status** — tandai tugas sebagai Selesai atau Belum Selesai
- **Filter Data** — saring tugas berdasarkan Status, Kategori, dan Prioritas
- **Statistik Real-time** — ringkasan jumlah tugas Total, Selesai, dan Belum Selesai
- **Pewarnaan Prioritas** — baris tabel diwarnai otomatis berdasarkan tingkat prioritas
- **Sorting Kolom** — klik header tabel untuk mengurutkan data
- **Menu Bar** — shortcut keyboard dan menu Tentang Aplikasi
- **Persistent Storage** — data tersimpan permanen via SQLite

---

## 🚀 Cara Menjalankan

### 1. Clone repository

```bash
git clone https://github.com/apriesna-zulhan/pv26-miniproject-todolist-F1D02310100.git
cd cd pv26-miniproject-todolist-F1D02310100
```

### 2. Install dependencies

```bash
pip install PySide6
```

### 3. Jalankan aplikasi

```bash
python main.py
```

> Database `todo.db` akan dibuat otomatis di folder project saat pertama kali dijalankan.

---

## 🛠️ Teknologi

| Teknologi | Versi | Kegunaan |
|-----------|-------|----------|
| Python | 3.12+ | Bahasa pemrograman utama |
| PySide6 | 6.x | Framework GUI berbasis Qt 6 |
| SQLite | built-in | Database penyimpanan lokal |
| QSS | — | Styling antarmuka dari file eksternal |

---

## 🗂️ Struktur Project

```
todo_app/
├── main.py                   # Entry point aplikasi
├── todo.db                   # Database SQLite (auto-generated)
├── database/
│   └── db_manager.py         # Lapisan data — operasi CRUD SQLite
├── logic/
│   └── task_controller.py    # Lapisan logika — validasi & bisnis
├── ui/
│   ├── main_window.py        # Jendela utama
│   └── task_dialog.py        # Dialog form tambah/edit
└── styles/
    └── style.qss             # Stylesheet QSS eksternal
```

---

## 👤 Identitas

| | |
|---|---|
| **Nama** | Apriesna Zulhan |
| **NIM** | F1D02310100 |
| **Mata Kuliah** | Pemrograman Visual |
| **Tahun** | 2026 |