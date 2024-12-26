from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Змініть на власний секретний ключ
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Використовується SQLite база даних

# Ініціалізація бази даних, шифрування паролів та менеджера сесій користувачів
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Вказуємо, яку сторінку використовувати для входу
login_manager.login_message_category = 'info'

# Завантаження користувачів для Flask-Login
from app.models import User, Website

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Функція для перевірки статусу сайтів
def check_website_availability(url):
    import requests
    try:
        response = requests.get(url, timeout=5)
        return "Online" if response.status_code == 200 else "Offline"
    except requests.RequestException:
        return "Offline"

# Фонове оновлення статусів сайтів
def update_website_statuses():
    with app.app_context():
        websites = Website.query.all()
        for website in websites:
            website.status = check_website_availability(website.url)
            website.last_checked = datetime.utcnow()
            db.session.commit()

# Ініціалізація планувальника задач
scheduler = BackgroundScheduler()
scheduler.add_job(func=update_website_statuses, trigger="interval", minutes=10)
scheduler.start()

# Зупинка планувальника при завершенні програми
atexit.register(lambda: scheduler.shutdown())

# Імпорт представлень (views) після створення об'єктів додатка
from app import views
