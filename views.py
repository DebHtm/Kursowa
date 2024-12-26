from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, AddWebsiteForm
from app.models import User, Website
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
import requests

def check_website_availability(url):
    try:
        response = requests.get(url, timeout=5)
        return "Online" if response.status_code == 200 else "Offline"
    except requests.RequestException:
        return "Offline"

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('monitor'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('monitor'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('monitor'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/monitor', methods=['GET', 'POST'])
@login_required
def monitor():
    form = AddWebsiteForm()
    if form.validate_on_submit():
        new_website = Website(url=form.url.data, status="Unknown")
        db.session.add(new_website)
        db.session.commit()
        flash('Website added to monitoring!', 'success')
        return redirect(url_for('monitor'))

    websites = Website.query.all()
    for website in websites:
        website.status = check_website_availability(website.url)
        website.last_checked = datetime.utcnow()
        db.session.commit()

    return render_template('monitor.html', form=form, websites=websites)
