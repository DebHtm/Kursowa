from app import app, db
from app.models import User

def initialize_database():
    with app.app_context():
        db.create_all()
        print("База даних та таблиці успішно створені.")

if __name__ == "__main__":
    initialize_database()
