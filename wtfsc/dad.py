import sys
from PyQt6 import QtWidgets, QtGui, QtCore
from datebase.db_manager import db_manager  # Импортируем ваш класс DBManager

class ScheduleWindow(QtWidgets.QWidget):
    def __init__(self, is_admin=False):
        super().__init__()
        self.is_admin = is_admin
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('School Schedule')
        self.setGeometry(100, 100, 572, 344)

        ScheduleWindow.setStyleSheet("background-color: dodgerblue")

        # Layouts
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.class_selector = QtWidgets.QComboBox()
        self.class_selector.addItems([str(i) for i in range(1, 12)])
        self.class_selector.currentIndexChanged.connect(self.load_schedule)

        self.table = QtWidgets.QTableWidget(7, 5)
        self.table.setHorizontalHeaderLabels(["Понедельник", "Вторник", "Среда", "Четверг", "пяница"])
        self.table.setVerticalHeaderLabels(["1 урок", "2 урок", "3 урок", "4 урок", "5 урок", "6 урок", "7 урок"])

        self.save_button = QtWidgets.QPushButton('Сохранить расписание')
        self.save_button.clicked.connect(self.save_schedule)
        self.save_button.setEnabled(self.is_admin)

        self.clear_button = QtWidgets.QPushButton('Удалить расписание')
        self.clear_button.clicked.connect(self.clear_schedule)
        self.clear_button.setEnabled(self.is_admin)

        self.layout.addWidget(self.class_selector)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.save_button)
        self.layout.addWidget(self.clear_button)

        self.load_schedule()

    def load_schedule(self):
        selected_class = self.class_selector.currentText()
        query = "SELECT * FROM schedule WHERE class = ?"
        result = db_manager.execute(query, (selected_class,), many=False)
        schedule_data = result["data"]

        self.table.clearContents()

        if schedule_data:
            for col in range(6):
                day_schedule = schedule_data[col + 1].split(",") if schedule_data[col + 1] else [""] * 6
                for row in range(min(6, len(day_schedule))):
                    self.table.setItem(row, col, QtWidgets.QTableWidgetItem(day_schedule[row]))

    def save_schedule(self):
        selected_class = self.class_selector.currentText()
        schedule_data = []

        for col in range(6):
            col_data = []
            for row in range(6):
                item = self.table.item(row, col)
                col_data.append(item.text() if item else "")
            schedule_data.append(",".join(col_data))

        delete_query = "DELETE FROM schedule WHERE class = ?"
        db_manager.execute(delete_query, (selected_class,))

        insert_query = """
            INSERT INTO schedule (class, monday, tuesday, wednesday, thursday, friday, saturday)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        db_manager.execute(insert_query, (selected_class, *schedule_data))

        QtWidgets.QMessageBox.information(self, "Success", "Schedule saved successfully!")

    def clear_schedule(self):
        selected_class = self.class_selector.currentText()
        db_manager.execute("UPDATE schedule SET monday = '', tuesday = '', wednesday = '', thursday = '', friday = '', saturday = '' WHERE class = ?", (selected_class,))
        self.table.clearContents()
        QtWidgets.QMessageBox.information(self, "Success", "Schedule cleared successfully!")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    schedule_window = ScheduleWindow(is_admin=True)
    schedule_window.show()
    sys.exit(app.exec())