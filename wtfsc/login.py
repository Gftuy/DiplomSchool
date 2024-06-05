from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QCheckBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from datebase.db_manager import db_manager
from main import MainWindow
from dad import ScheduleWindow
import sys

class RegistrationWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Регистрация")
        self.setWindowIcon(QIcon('static/autoreg.png'))
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout()

        self.setStyleSheet("background-color: #ffffff; color: #000000; font-size: 12px;")

        self.username_label = QLabel("Логин:")
        self.username_label.setStyleSheet("font-family: Arial; font-size: 10pt;")
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.password_label = QLabel("Пароль:")
        self.password_label.setStyleSheet("color: #000000;")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.show_password_checkbox = QCheckBox("Показать пароль")
        self.show_password_checkbox.setStyleSheet("color: #000000;")
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)
        layout.addWidget(self.show_password_checkbox)

        self.register_button = QPushButton("Зарегистрироваться")
        self.register_button.setStyleSheet("color: #ffffff; background-color: #008CBA; border: 1px solid #000000; padding: 5px 10px;")
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        self.back_button = QPushButton("Назад к авторизации")
        self.back_button.setStyleSheet("color: #ffffff; background-color: #f44336; border: 1px solid #000000; padding: 5px 10px;")
        self.back_button.clicked.connect(self.back_to_authorization)
        layout.addWidget(self.back_button)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(layout)

    def toggle_password_visibility(self, checked):
        if checked:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

    def back_to_authorization(self):
        self.hide()
        self.parent().show()

    def register(self):
        new_username = self.username_input.text()
        new_password = self.password_input.text()

        # Проверяем, существует ли пользователь с таким логином
        res = db_manager.execute("""SELECT * FROM users WHERE username = ?""", args=(new_username,))
        if res and 'data' in res and res['data']:
            # Если пользователь уже существует, выдаем ошибку
            QMessageBox.warning(self, "Ошибка регистрации", "Пользователь с таким логином уже существует. Пожалуйста, выберите другой логин.")
        else:
            # Регистрируем нового пользователя
            if len(new_username) > 3 and len(new_password) > 3:
                db_manager.execute("""INSERT INTO users (username, password, user_type) VALUES (?, ?, 5);""", args=(new_username, new_password))
                QMessageBox.information(self, "Успешная регистрация", "Новый пользователь зарегистрирован.")
            else:
                QMessageBox.warning(self, "Ошибка регистрации", "Логин и пароль должны содержать не менее 4 символов.")

class AuthorizationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Авторизация")
        self.setWindowIcon(QIcon('static/autoreg.png'))
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.setStyleSheet("background-color: #ffffff; color: #000000; font-size: 12px;")

        self.username_label = QLabel("Логин:")
        self.username_label.setStyleSheet("font-family: Arial; font-size: 10pt;")
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.password_label = QLabel("Пароль:")
        self.password_label.setStyleSheet("color: #000000;")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.show_password_checkbox = QCheckBox("Показать пароль")
        self.show_password_checkbox.setStyleSheet("color: #000000;")
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)
        layout.addWidget(self.show_password_checkbox)

        self.login_button = QPushButton("Войти")
        self.login_button.setStyleSheet("color: #ffffff; background-color: #008CBA; border: 1px solid #000000; padding: 5px 10px;")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.register_button = QPushButton("Регистрация")
        self.register_button.setStyleSheet("color: #ffffff; background-color: #f44336; border: 1px solid #000000; padding: 5px 10px;")
        self.register_button.clicked.connect(self.show_registration_window)
        layout.addWidget(self.register_button)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(layout)

    def toggle_password_visibility(self, checked):
        if checked:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

    def show_registration_window(self):
        self.hide()
        self.registration_window = RegistrationWindow(parent=self)
        self.registration_window.show()

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Проверяем, существует ли пользователь с таким логином
        res = db_manager.execute("""SELECT * FROM users WHERE username = ?""", args=(username,))
        if res and 'data' in res and res['data']:
            # Если пользователь существует, проверяем правильность пароля
            res = db_manager.execute("""SELECT * FROM users WHERE username = ? AND password = ?""", args=(username, password))
            if res:
                if username == "admin":
                    QMessageBox.information(self, "Успешный вход", f"Вы успешно вошли как {'администратор' if username else 'пользователь'}.")
                    self.hide()
                    self.addwindow = MainWindow(type_user= "admin")
                    self.addwindow.show()
                else:
                    QMessageBox.information(self, "Успешный вход", "Вы успешно вошли.")
                    self.hide()
                    self.addwindow = MainWindow(type_user= "pupils")
                    self.addwindow.show()
            else:
                QMessageBox.warning(self, "Ошибка входа", "Неверный пароль.")
        else:
            # Если пользователь не существует, выдаем ошибку
            QMessageBox.warning(self, "Ошибка входа", "Пользователя с таким логином не существует. Добавьте его в базу данных или проверьте правильность логина.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AuthorizationWindow()
    window.show()
    sys.exit(app.exec())
