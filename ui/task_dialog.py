"""
ui/task_dialog.py
Dialog terpisah untuk menambah / mengedit tugas.
Separation of Concerns: hanya menangani form input.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QTextEdit, QComboBox, QDateEdit,
    QPushButton, QFrame, QMessageBox
)
from PySide6.QtCore import Qt, QDate
from logic.task_controller import CATEGORIES, PRIORITIES


class TaskDialog(QDialog):
    """Dialog modal untuk tambah / edit tugas."""

    def __init__(self, parent=None, task: dict | None = None):
        super().__init__(parent)
        self._task = task          # None → mode tambah, dict → mode edit
        self._result_data: dict | None = None

        self.setWindowTitle("Edit Tugas" if task else "Tambah Tugas Baru")
        self.setMinimumWidth(460)
        self.setModal(True)

        self._build_ui()
        self._connect_signals()

        if task:
            self._populate(task)

    # Build UI 

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setSpacing(14)
        root.setContentsMargins(24, 20, 24, 20)

        # Judul dialog 
        title_text = "Edit Tugas" if self._task else "Tambah Tugas Baru"
        lbl_title = QLabel(title_text)
        lbl_title.setObjectName("dialogTitle")
        root.addWidget(lbl_title)

        sep = QFrame()
        sep.setObjectName("dialogSeparator")
        root.addWidget(sep)

        # Form 
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        form.setSpacing(10)
        form.setHorizontalSpacing(16)

        # Field 1 – Judul
        self.txt_title = QLineEdit()
        self.txt_title.setPlaceholderText("Masukkan judul tugas (wajib)…")
        self.txt_title.setMaxLength(100)
        lbl1 = QLabel("Judul *")
        lbl1.setObjectName("fieldLabel")
        form.addRow(lbl1, self.txt_title)

        # Field 2 – Deskripsi
        self.txt_desc = QTextEdit()
        self.txt_desc.setPlaceholderText("Deskripsi tambahan (opsional)…")
        self.txt_desc.setFixedHeight(80)
        lbl2 = QLabel("Deskripsi")
        lbl2.setObjectName("fieldLabel")
        form.addRow(lbl2, self.txt_desc)

        # Field 3 – Kategori
        self.cmb_category = QComboBox()
        self.cmb_category.addItems(CATEGORIES)
        lbl3 = QLabel("Kategori")
        lbl3.setObjectName("fieldLabel")
        form.addRow(lbl3, self.cmb_category)

        # Field 4 – Prioritas
        self.cmb_priority = QComboBox()
        self.cmb_priority.addItems(PRIORITIES)
        self.cmb_priority.setCurrentText("Sedang")
        lbl4 = QLabel("Prioritas")
        lbl4.setObjectName("fieldLabel")
        form.addRow(lbl4, self.cmb_priority)

        # Field 5 – Tenggat waktu
        self.date_due = QDateEdit()
        self.date_due.setCalendarPopup(True)
        self.date_due.setDisplayFormat("dd MMM yyyy")
        self.date_due.setDate(QDate.currentDate())
        lbl5 = QLabel("Tenggat Waktu")
        lbl5.setObjectName("fieldLabel")
        form.addRow(lbl5, self.date_due)

        root.addLayout(form)

        # Tombol aksi
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)
        btn_row.addStretch()

        self.btn_cancel = QPushButton("Batal")
        self.btn_cancel.setObjectName("btnCancel")

        self.btn_save = QPushButton("Simpan" if self._task else "Tambah")
        self.btn_save.setObjectName("btnSave")
        self.btn_save.setDefault(True)

        btn_row.addWidget(self.btn_cancel)
        btn_row.addWidget(self.btn_save)
        root.addLayout(btn_row)

    # Signals

    def _connect_signals(self):
        self.btn_save.clicked.connect(self._on_save)
        self.btn_cancel.clicked.connect(self.reject)

    # Slots

    def _populate(self, task: dict):
        """Isi form dengan data tugas yang akan diedit."""
        self.txt_title.setText(task.get("title", ""))
        self.txt_desc.setPlainText(task.get("description", ""))
        self.cmb_category.setCurrentText(task.get("category", CATEGORIES[0]))
        self.cmb_priority.setCurrentText(task.get("priority", "Sedang"))
        due = task.get("due_date", "")
        if due:
            self.date_due.setDate(QDate.fromString(due, "yyyy-MM-dd"))

    def _on_save(self):
        title = self.txt_title.text().strip()
        if not title:
            QMessageBox.warning(self, "Input Tidak Valid",
                                "Judul tugas tidak boleh kosong.")
            self.txt_title.setFocus()
            return

        self._result_data = {
            "title":       title,
            "description": self.txt_desc.toPlainText().strip(),
            "category":    self.cmb_category.currentText(),
            "priority":    self.cmb_priority.currentText(),
            "due_date":    self.date_due.date().toString("yyyy-MM-dd"),
        }
        self.accept()

    # Public accessor 

    def get_data(self) -> dict | None:
        """Mengembalikan data form jika disimpan, None jika dibatalkan."""
        return self._result_data
