import requests
from datetime import datetime
from app import db
from app.models import Website

def check_website_availability():
    websites = Website.query.all()  # Отримуємо всі сайти з бази даних
    for site in websites:
        try:
            # Виконуємо запит до сайту
            response = requests.get(site.url, timeout=5)
            # Якщо відповідь має код 200, сайт доступний
            site.status = 'Available' if response.status_code == 200 else 'Unavailable'
        except requests.RequestException:
            # Якщо є помилка підключення, сайт недоступний
            site.status = 'Unavailable'
        
        site.last_checked = datetime.now()  # Оновлюємо час останньої перевірки
        db.session.commit()  # Зберігаємо зміни в базі даних
