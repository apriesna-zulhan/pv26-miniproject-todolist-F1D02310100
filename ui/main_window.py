"""
ui/main_window.py
Jendela utama aplikasi To-Do List.
Separation of Concerns: hanya menangani tampilan dan event UI.
Logika bisnis didelegasikan ke task_controller.
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QComboBox, QHeaderView, QMessageBox, QFrame, QSizePolicy,
    QSpacerItem, QAbstractItemView
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QFont, QAction

from logic import task_controller
from ui.task_dialog import TaskDialog

# Konstanta identitas mahasiswa 
STUDENT_NAME = "Apriesna Zulhan"
STUDENT_NIM  = "F1D02310100"

# Kolom tabel
COL_ID       = 0
COL_TITLE    = 1
COL_CATEGORY = 2
COL_PRIORITY = 3
COL_DUE      = 4
COL_STATUS   = 5
COL_CREATED  = 6


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("To-Do List — Tugas PySide6")
        self.setMinimumSize(QSize(1000, 640))

        task_controller.initialize()
        self._build_menu()
        self._build_ui()
        self._connect_signals()
        self._refresh_table()
        self._refresh_stats()

    # Menu Bar

    def _build_menu(self):
        menubar = self.menuBar()

        # Menu File
        menu_file = menubar.addMenu("File")
        act_refresh = QAction("Refresh Data", self)
        act_refresh.setShortcut("F5")
        act_refresh.triggered.connect(self._refresh_all)
        menu_file.addAction(act_refresh)
        menu_file.addSeparator()
        act_exit = QAction("Keluar", self)
        act_exit.setShortcut("Ctrl+Q")
        act_exit.triggered.connect(self.close)
        menu_file.addAction(act_exit)

        # Menu Tugas
        menu_task = menubar.addMenu("Tugas")
        act_add = QAction("Tambah Tugas Baru", self)
        act_add.setShortcut("Ctrl+N")
        act_add.triggered.connect(self._on_add)
        menu_task.addAction(act_add)

        act_edit = QAction("Edit Tugas Terpilih", self)
        act_edit.setShortcut("Ctrl+E")
        act_edit.triggered.connect(self._on_edit)
        menu_task.addAction(act_edit)

        act_del = QAction("Hapus Tugas Terpilih", self)
        act_del.setShortcut("Delete")
        act_del.triggered.connect(self._on_delete)
        menu_task.addAction(act_del)

        # Menu Bantuan → Tentang Aplikasi
        menu_help = menubar.addMenu("Bantuan")
        act_about = QAction("Tentang Aplikasi", self)
        act_about.triggered.connect(self._show_about)
        menu_help.addAction(act_about)

    # Build UI 

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._make_header())
        root.addWidget(self._make_body(), 1)
        root.addWidget(self._make_footer())

    def _make_header(self) -> QWidget:
        header = QFrame()
        header.setObjectName("headerPanel")
        header.setFixedHeight(90)

        hl = QHBoxLayout(header)
        hl.setContentsMargins(20, 10, 20, 10)

        # Kiri: judul
        left = QVBoxLayout()
        lbl_title = QLabel("📋  To-Do List")
        lbl_title.setObjectName("appTitle")
        lbl_sub = QLabel("Kelola tugas harianmu dengan mudah")
        lbl_sub.setObjectName("appSubtitle")
        left.addWidget(lbl_title)
        left.addWidget(lbl_sub)
        hl.addLayout(left)

        hl.addStretch()

        # Kanan: identitas mahasiswa (read-only, selalu tampil)
        right = QVBoxLayout()
        right.setAlignment(Qt.AlignRight)
        lbl_name = QLabel(f"👤  {STUDENT_NAME}")
        lbl_name.setObjectName("identityLabel")
        lbl_nim = QLabel(f"NIM: {STUDENT_NIM}")
        lbl_nim.setObjectName("identityLabel")
        right.addWidget(lbl_name)
        right.addWidget(lbl_nim)
        hl.addLayout(right)

        return header

    def _make_body(self) -> QWidget:
        body = QWidget()
        hl = QHBoxLayout(body)
        hl.setContentsMargins(16, 12, 16, 12)
        hl.setSpacing(14)

        # Sidebar kiri
        hl.addWidget(self._make_sidebar(), 0)

        # Konten utama (tabel)
        hl.addWidget(self._make_table_area(), 1)

        return body

    def _make_sidebar(self) -> QWidget:
        sidebar = QWidget()
        sidebar.setFixedWidth(220)
        vl = QVBoxLayout(sidebar)
        vl.setSpacing(12)
        vl.setContentsMargins(0, 0, 0, 0)

        # ── Panel statistik ──
        stats_frame = QFrame()
        stats_frame.setObjectName("statsPanel")
        sv = QVBoxLayout(stats_frame)
        sv.setSpacing(4)

        lbl_stats_title = QLabel("📊  Statistik")
        lbl_stats_title.setObjectName("sectionTitle")
        sv.addWidget(lbl_stats_title)

        sv.addWidget(self._make_divider())

        # Total
        self.lbl_total = QLabel("0")
        self.lbl_total.setObjectName("statNumber")
        self.lbl_total.setAlignment(Qt.AlignCenter)
        lbl_total_desc = QLabel("Total Tugas")
        lbl_total_desc.setObjectName("statLabel")
        lbl_total_desc.setAlignment(Qt.AlignCenter)

        # Selesai
        self.lbl_done = QLabel("0")
        self.lbl_done.setObjectName("statNumber")
        self.lbl_done.setAlignment(Qt.AlignCenter)
        self.lbl_done.setStyleSheet("color: #38A169;")
        lbl_done_desc = QLabel("Selesai")
        lbl_done_desc.setObjectName("statLabel")
        lbl_done_desc.setAlignment(Qt.AlignCenter)

        # Belum selesai
        self.lbl_pending = QLabel("0")
        self.lbl_pending.setObjectName("statNumber")
        self.lbl_pending.setAlignment(Qt.AlignCenter)
        self.lbl_pending.setStyleSheet("color: #E53E3E;")
        lbl_pending_desc = QLabel("Belum Selesai")
        lbl_pending_desc.setObjectName("statLabel")
        lbl_pending_desc.setAlignment(Qt.AlignCenter)

        for w in [self.lbl_total, lbl_total_desc,
                  self.lbl_done, lbl_done_desc,
                  self.lbl_pending, lbl_pending_desc]:
            sv.addWidget(w)

        vl.addWidget(stats_frame)

        # ── Panel filter ──
        filter_frame = QFrame()
        filter_frame.setObjectName("filterPanel")
        fv = QVBoxLayout(filter_frame)
        fv.setSpacing(8)

        lbl_filter_title = QLabel("🔎  Filter")
        lbl_filter_title.setObjectName("sectionTitle")
        fv.addWidget(lbl_filter_title)
        fv.addWidget(self._make_divider())

        fv.addWidget(QLabel("Status:"))
        self.cmb_filter_status = QComboBox()
        self.cmb_filter_status.addItems(["Semua", "Belum Selesai", "Selesai"])
        fv.addWidget(self.cmb_filter_status)

        fv.addWidget(QLabel("Kategori:"))
        self.cmb_filter_cat = QComboBox()
        cats = ["Semua"] + task_controller.CATEGORIES
        self.cmb_filter_cat.addItems(cats)
        fv.addWidget(self.cmb_filter_cat)

        fv.addWidget(QLabel("Prioritas:"))
        self.cmb_filter_prio = QComboBox()
        self.cmb_filter_prio.addItems(["Semua"] + task_controller.PRIORITIES)
        fv.addWidget(self.cmb_filter_prio)

        btn_apply = QPushButton("Terapkan Filter")
        btn_apply.setObjectName("btnRefresh")
        btn_apply.clicked.connect(self._refresh_table)
        fv.addWidget(btn_apply)

        btn_reset = QPushButton("Reset Filter")
        btn_reset.setObjectName("btnRefresh")
        btn_reset.clicked.connect(self._reset_filter)
        fv.addWidget(btn_reset)

        vl.addWidget(filter_frame)
        vl.addStretch()
        return sidebar

    def _make_table_area(self) -> QWidget:
        area = QWidget()
        vl = QVBoxLayout(area)
        vl.setSpacing(10)
        vl.setContentsMargins(0, 0, 0, 0)

        # Toolbar tombol aksi
        toolbar = QHBoxLayout()
        toolbar.setSpacing(8)

        self.btn_add = QPushButton("＋  Tambah Tugas")
        self.btn_add.setObjectName("btnAdd")

        self.btn_edit = QPushButton("✏  Edit")
        self.btn_edit.setObjectName("btnEdit")

        self.btn_delete = QPushButton("🗑  Hapus")
        self.btn_delete.setObjectName("btnDelete")

        self.btn_toggle = QPushButton("✔  Ubah Status")
        self.btn_toggle.setObjectName("btnToggle")

        self.btn_refresh = QPushButton("↺  Refresh")
        self.btn_refresh.setObjectName("btnRefresh")

        toolbar.addWidget(self.btn_add)
        toolbar.addWidget(self.btn_edit)
        toolbar.addWidget(self.btn_delete)
        toolbar.addWidget(self.btn_toggle)
        toolbar.addStretch()
        toolbar.addWidget(self.btn_refresh)
        vl.addLayout(toolbar)

        # Tabel utama
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Judul", "Kategori", "Prioritas", "Tenggat", "Status", "Dibuat"])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setSortingEnabled(True)

        hh = self.table.horizontalHeader()
        hh.setSectionResizeMode(COL_ID,       QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(COL_TITLE,    QHeaderView.Stretch)
        hh.setSectionResizeMode(COL_CATEGORY, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(COL_PRIORITY, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(COL_DUE,      QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(COL_STATUS,   QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(COL_CREATED,  QHeaderView.ResizeToContents)

        vl.addWidget(self.table)

        # Label info baris terpilih
        self.lbl_info = QLabel("Pilih tugas untuk melihat detail.")
        self.lbl_info.setStyleSheet("color: #718096; font-size: 12px;")
        vl.addWidget(self.lbl_info)

        return area

    def _make_footer(self) -> QLabel:
        lbl = QLabel(
            f"  Aplikasi To-Do List  |  {STUDENT_NAME}  |  NIM: {STUDENT_NIM}"
            "  |  Mata Kuliah Pemrograman Berbasis Objek  "
        )
        lbl.setObjectName("footerLabel")
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setFixedHeight(30)
        return lbl

    @staticmethod
    def _make_divider() -> QFrame:
        line = QFrame()
        line.setObjectName("dialogSeparator")
        line.setFixedHeight(1)
        return line

    # Signals & Slots 

    def _connect_signals(self):
        self.btn_add.clicked.connect(self._on_add)
        self.btn_edit.clicked.connect(self._on_edit)
        self.btn_delete.clicked.connect(self._on_delete)
        self.btn_toggle.clicked.connect(self._on_toggle)
        self.btn_refresh.clicked.connect(self._refresh_all)
        self.table.itemSelectionChanged.connect(self._on_selection_changed)
        self.table.doubleClicked.connect(self._on_edit)

    # Table helpers 

    def _refresh_table(self):
        status   = self.cmb_filter_status.currentText()
        category = self.cmb_filter_cat.currentText()
        priority = self.cmb_filter_prio.currentText()

        tasks = task_controller.fetch_tasks(status, category, priority)
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(tasks))

        PRIORITY_COLOR = {"Tinggi": "#FFF5F5", "Sedang": "#FEFCE8", "Rendah": "#F0FFF4"}

        for row, task in enumerate(tasks):
            bg = QColor(PRIORITY_COLOR.get(task["priority"], "#FFFFFF"))
            if task["status"] == "Selesai":
                bg = QColor("#F0FFF4")

            def cell(text: str) -> QTableWidgetItem:
                item = QTableWidgetItem(str(text))
                item.setBackground(bg)
                return item

            self.table.setItem(row, COL_ID,       cell(task["id"]))
            self.table.setItem(row, COL_TITLE,    cell(task["title"]))
            self.table.setItem(row, COL_CATEGORY, cell(task["category"]))
            self.table.setItem(row, COL_PRIORITY, cell(task["priority"]))
            self.table.setItem(row, COL_DUE,      cell(task["due_date"] or "-"))
            self.table.setItem(row, COL_CREATED,  cell((task["created_at"] or "")[:10]))

            # Status dengan warna teks
            status_item = cell(task["status"])
            status_item.setForeground(
                QColor("#276749") if task["status"] == "Selesai" else QColor("#C53030"))
            font = QFont()
            font.setBold(True)
            status_item.setFont(font)
            self.table.setItem(row, COL_STATUS, status_item)

        self.table.setSortingEnabled(True)
        self.lbl_info.setText(f"Menampilkan {len(tasks)} tugas.")

    def _refresh_stats(self):
        stats = task_controller.fetch_statistics()
        self.lbl_total.setText(str(stats["total"]))
        self.lbl_done.setText(str(stats["done"]))
        self.lbl_pending.setText(str(stats["pending"]))

    def _refresh_all(self):
        self._refresh_table()
        self._refresh_stats()

    def _reset_filter(self):
        self.cmb_filter_status.setCurrentText("Semua")
        self.cmb_filter_cat.setCurrentText("Semua")
        self.cmb_filter_prio.setCurrentText("Semua")
        self._refresh_table()

    def _selected_task_id(self) -> int | None:
        row = self.table.currentRow()
        if row < 0:
            return None
        item = self.table.item(row, COL_ID)
        return int(item.text()) if item else None

    # Slot handlers

    def _on_selection_changed(self):
        task_id = self._selected_task_id()
        if task_id is None:
            self.lbl_info.setText("Pilih tugas untuk melihat detail.")
            return
        task = task_controller.fetch_task(task_id)
        if task:
            self.lbl_info.setText(
                f"ID {task['id']}  |  {task['title']}  |  "
                f"Kategori: {task['category']}  |  Prioritas: {task['priority']}  |  "
                f"Status: {task['status']}"
            )

    def _on_add(self):
        dlg = TaskDialog(self)
        if dlg.exec():
            data = dlg.get_data()
            ok, msg = task_controller.add_task(
                data["title"], data["description"],
                data["category"], data["priority"], data["due_date"]
            )
            if ok:
                self._refresh_all()
                self._show_info("Berhasil", msg)
            else:
                QMessageBox.warning(self, "Gagal", msg)

    def _on_edit(self):
        task_id = self._selected_task_id()
        if task_id is None:
            QMessageBox.information(self, "Perhatian", "Pilih tugas yang ingin diedit.")
            return
        task = task_controller.fetch_task(task_id)
        if not task:
            return

        dlg = TaskDialog(self, task=task)
        if dlg.exec():
            data = dlg.get_data()
            ok, msg = task_controller.edit_task(
                task_id, data["title"], data["description"],
                data["category"], data["priority"], data["due_date"]
            )
            if ok:
                self._refresh_all()
                self._show_info("Berhasil", msg)
            else:
                QMessageBox.warning(self, "Gagal", msg)

    def _on_delete(self):
        task_id = self._selected_task_id()
        if task_id is None:
            QMessageBox.information(self, "Perhatian", "Pilih tugas yang ingin dihapus.")
            return
        task = task_controller.fetch_task(task_id)
        if not task:
            return

        # Dialog konfirmasi (QMessageBox)
        reply = QMessageBox.question(
            self, "Konfirmasi Hapus",
            f"Apakah Anda yakin ingin menghapus tugas:\n\n"
            f"  '{task['title']}'\n\nTindakan ini tidak dapat dibatalkan.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            ok, msg = task_controller.remove_task(task_id)
            if ok:
                self._refresh_all()
                self._show_info("Berhasil", msg)

    def _on_toggle(self):
        task_id = self._selected_task_id()
        if task_id is None:
            QMessageBox.information(self, "Perhatian", "Pilih tugas yang ingin diubah statusnya.")
            return
        ok, msg = task_controller.toggle_task_status(task_id)
        if ok:
            self._refresh_all()

    # About dialog 

    def _show_about(self):
        QMessageBox.about(
            self,
            "Tentang Aplikasi",
            "<h2>📋 To-Do List</h2>"
            "<p><b>Deskripsi:</b><br>"
            "Aplikasi manajemen tugas berbasis GUI yang dibangun menggunakan PySide6. "
            "Mendukung CRUD tugas, filter, dan penyimpanan permanen menggunakan SQLite.</p>"
            "<hr>"
            f"<p><b>Nama Mahasiswa:</b> {STUDENT_NAME}<br>"
            f"<b>NIM:</b> {STUDENT_NIM}</p>"
            "<p><b>Mata Kuliah:</b> Pemrograman Visual<br>"
            "<b>Teknologi:</b> Python 3.12 · PySide6 · SQLite</p>"
        )

    @staticmethod
    def _show_info(title: str, msg: str):
        box = QMessageBox()
        box.setWindowTitle(title)
        box.setText(msg)
        box.setIcon(QMessageBox.Information)
        box.exec()
