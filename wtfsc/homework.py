import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
    QPushButton, QListWidget, QLabel, QComboBox, QListWidgetItem, QMessageBox, QLineEdit
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from datebase.db_manager import db_manager

class HomeworkWindow(QMainWindow):
    def __init__(self, admin=False):
        super().__init__()
        self.is_admin = admin
        self.setWindowTitle("Homework Assignment")
        self.setGeometry(100, 100, 800, 600)

        # Subjects by class
        self.subjects_by_class = {
            "1": ["Математика", "Русский язык", "Изо", "Технология", "Музыка", "Родной язык", "Родная литература", "Литературное чтение", "Окружающий мир", "Физическая культура"],
            "2": ["Математика", "Русский язык", "Изо", "Технология", "Музыка", "Родной язык", "Родная литература", "Литературное чтение", "Окружающий мир", "Английский язык", "Информатика", "Немецкий язык", "Физическая культура"],
            "3": ["Математика", "Русский язык", "Изо", "Технология", "Музыка", "Родной язык", "Родная литература", "Литературное чтение", "Окружающий мир", "Английский язык", "Информатика", "Немецкий язык", "Физическая культура"],
            "4": ["Математика", "Русский язык", "Изо", "Технология", "Музыка", "Родной язык", "Родная литература", "Литературное чтение", "Окружающий мир", "Английский язык", "Информатика", "Немецкий язык", "Основы религиозных культур и светской этики", "Физическая культура"],
            "5": ["Математика", "Русский язык", "Изо", "Технология", "Музыка", "Родной язык", "Родная литература", "Литературное чтение", "Биология", "Английский язык", "Информатика", "Немецкий язык", "История", "География", "Основы духовно-нравственной культуры народов России", "Обществознание", "Физическая культура"],
            "6": ["Математика", "Русский язык", "Изо", "Технология", "Музыка", "Родной язык", "Родная литература", "Литературное чтение", "Биология", "Английский язык", "Информатика", "Немецкий язык", "История", "География", "Обществознание", "Физическая культура"],
            "7": ["Химия", "Русский язык", "Изо", "Технология", "Музыка", "Родной язык", "Родная литература", "Литературное чтение", "Биология", "Английский язык", "Информатика", "Немецкий язык", "История", "География", "Обществознание", "Физическая культура", "Алгебра", "Геометрия", "Обж", "Физика"],
            "8": ["Химия", "Русский язык", "Изо", "Технология", "Музыка", "Родной язык", "Родная литература", "Литературное чтение", "Биология", "Английский язык", "Информатика", "Немецкий язык", "История", "География", "Обществознание", "Физическая культура", "Алгебра", "Геометрия", "Обж", "Физика"],
            "9": ["Химия", "Русский язык", "Изо", "Технология", "Родной язык", "Родная литература", "Литературное чтение", "Биология", "Английский язык", "Информатика", "Немецкий язык", "История", "География", "Обществознание", "Физическая культура", "Алгебра", "Геометрия", "Обж", "Физика"],
            "10": ["Химия", "Русский язык", "Родной язык", "Литературное чтение", "Биология", "Английский язык", "Информатика", "Немецкий язык", "История", "География", "Обществознание", "Физическая культура", "Математика", "Обж", "Физика"],
            "11": ["Химия", "Русский язык", "Родной язык", "Литературное чтение", "Биология", "Английский язык", "Информатика", "Немецкий язык", "История", "География", "Обществознание", "Физическая культура", "Математика", "Обж", "Физика", "Астрономия"]
        }

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layouts
        main_layout = QVBoxLayout(central_widget)
        form_layout = QVBoxLayout()
        list_layout = QVBoxLayout()

        # Class selection
        self.class_combo_box = QComboBox()
        for i in range(1, 12):
            self.class_combo_box.addItem(str(i))
        self.class_combo_box.currentIndexChanged.connect(self.update_subjects)

        # Subject selection
        self.subject_combo_box = QComboBox()

        # Widgets
        self.homework_text_edit = QTextEdit()
        self.homework_text_edit.setPlaceholderText("Enter homework assignment here...")
        self.homework_text_edit.setFont(QFont("Arial", 14))

        self.submit_button = QPushButton("Submit")
        self.submit_button.setFont(QFont("Arial", 14))
        self.submit_button.clicked.connect(self.submit_homework)

        self.homework_list_widget = QListWidget()
        self.homework_list_widget.setFont(QFont("Arial", 14))

        # Add widgets to layouts
        form_layout.addWidget(QLabel("Select Class:", self))
        form_layout.addWidget(self.class_combo_box)
        form_layout.addWidget(QLabel("Select Subject:", self))
        form_layout.addWidget(self.subject_combo_box)
        form_layout.addWidget(QLabel("New Homework Assignment:", self))
        form_layout.addWidget(self.homework_text_edit)
        if self.is_admin:
            form_layout.addWidget(self.submit_button)

        list_layout.addWidget(QLabel("Homework Assignments:", self))
        list_layout.addWidget(self.homework_list_widget)

        # Add layouts to main layout
        main_layout.addLayout(form_layout)
        main_layout.addLayout(list_layout)

        # Load existing homework assignments
        self.load_homework_assignments()

    def update_subjects(self):
        selected_class = self.class_combo_box.currentText()
        self.subject_combo_box.clear()
        self.subject_combo_box.addItems(self.subjects_by_class[selected_class])

    def load_homework_assignments(self):
        query = "SELECT class, subject, assignment FROM homework"
        result = db_manager.execute(query)

        if result["code"] == 200:
            self.homework_list_widget.clear()
            for class_name, subject, assignment in result["data"]:
                item_text = f"Class {class_name} - {subject}: {assignment}"
                item = QListWidgetItem(item_text)
                self.homework_list_widget.addItem(item)
        else:
            QMessageBox.warning(self, "Error", "Failed to load homework assignments.")

    def submit_homework(self):
        homework_text = self.homework_text_edit.toPlainText()
        selected_class = self.class_combo_box.currentText()
        selected_subject = self.subject_combo_box.currentText()

        if homework_text:
            # Save the homework to the database
            query = "INSERT INTO homework (class, subject, assignment) VALUES (?, ?, ?)"
            values = (selected_class, selected_subject, homework_text)
            result = db_manager.execute(query, values)

            if result["code"] == 200:
                QMessageBox.information(self, "Success", "Homework assignment submitted successfully.")
                self.load_homework_assignments()
                self.homework_text_edit.clear()
            else:
                QMessageBox.warning(self, "Error", "Failed to submit homework assignment.")
        else:
            QMessageBox.warning(self, "Warning", "Please enter homework assignment.")

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 200)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layouts
        layout = QVBoxLayout(central_widget)

        # Widgets
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Username")

        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Password")
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)

        # Add widgets to layout
        layout.addWidget(QLabel("Username:", self))
        layout.addWidget(self.username_edit)
        layout.addWidget(QLabel("Password:", self))
        layout.addWidget(self.password_edit)
        layout.addWidget(self.login_button)

    def login(self):
        username = self.username_edit.text()
        password = self.password_edit.text()

        # Check credentials (for simplicity, username: admin, password: admin)
        if username == "admin" and password == "admin":
            self.homework_window = HomeworkWindow(is_admin=True)
            self.homework_window.show()
            self.close()
        else:
            self.homework_window = HomeworkWindow(is_admin=False)
            self.homework_window.show()
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
