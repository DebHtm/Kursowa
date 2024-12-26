from app import app, db  # Імпортуємо додаток Flask та об'єкт db
from app.models import User  # Імпортуємо модель, яку ви хочете створити, додайте інші, якщо вони є

# Створюємо функцію для ініціалізації бази даних
def initialize_database():
    with app.app_context():  # Створюємо контекст додатка
        db.create_all()  # Викликаємо створення всіх таблиць
        print("База даних та таблиці успішно створені.")

# Викликаємо функцію для ініціалізації бази даних
if __name__ == "__main__":
    initialize_database()
