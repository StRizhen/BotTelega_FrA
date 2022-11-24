import sqlite3


class Database:

#Тупо подключение ЭСКУЭЛ
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

#Проверить есть ли в БД
    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchmany(1)
            return bool(len(result))

#Добавить в БД
    def add_user(self, user_id):
        with self.connection:
            return self.connection.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))

#Проверка активности пользователя
    def set_active(self, user_id, active):
        with self.connection:
            return self.cursor.execute("UPDATE users SET active = ? WHERE user_id = ?", (active, user_id,))

#Забрать инфу из БД
    def get_users(self):
        with self.connection:
            return self.cursor.execute("SELECT user_id, active  FROM users").fetchmany(100)
