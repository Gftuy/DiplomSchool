import json

class ScheduleManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_schedule(self, class_name):
        res = self.db_manager.execute("SELECT * FROM schedule WHERE class = ?", args=(class_name,))
        return res if res else None

    def save_schedule(self, class_name, schedule):
        # Удалите существующее расписание для данного класса
        self.db_manager.execute("DELETE FROM schedule WHERE class = ?", args=(class_name,))
        # Добавьте новое расписание
        try:
            self.db_manager.execute("""
                INSERT INTO schedule (class, monday, tuesday, wednesday, thursday, friday, saturday)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, args=(class_name, json.dumps(schedule[0]), json.dumps(schedule[1]), json.dumps(schedule[2]),
                       json.dumps(schedule[3]), json.dumps(schedule[4]), json.dumps(schedule[5])))
            print("Расписание успешно сохранено в базе данных.")
        except Exception as e:
            print("Произошла ошибка при сохранении расписания:", e)
