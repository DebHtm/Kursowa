import requests
from datetime import datetime
from app import db
from app.models import Website

def check_website_availability():
    websites = Website.query.all()
    for site in websites:
        try:
            response = requests.get(site.url, timeout=5)
            site.status = 'Available' if response.status_code == 200 else 'Unavailable'
        except requests.RequestException:
            site.status = 'Unavailable'
        
        site.last_checked = datetime.now()
        db.session.commit()
