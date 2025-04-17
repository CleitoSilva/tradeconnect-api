from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse, urljoin
from .models import User, Service, Log, Notification, Review
from . import db
import requests
import json

main = Blueprint('main', __name__)

# Safe redirect
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

# LOGIN
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            if not user.is_active:
                flash('This user is deactivated.')
                return redirect(url_for('main.login'))
            login_user(user)
            if user.role == 'Client':
                return redirect(url_for('main.dashboard_client'))
            elif user.role == 'Professional':
                return redirect(url_for('main.dashboard_professional'))
            elif user.role == 'Admin':
                return redirect(url_for('main.admin_dashboard'))
            flash('Invalid role.')
        else:
            flash('Incorrect email or password.')

    return render_template('login.html')

# LOGOUT
@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

# REGISTER
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        address = request.form['address']
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        specialty = request.form.get('specialty') if role == 'Professional' else None

        custom_specialty = request.form.get('custom_specialty')
        if specialty == 'Other' and custom_specialty:
            specialty = custom_specialty

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("⚠️ This email is already registered.")
            return redirect(url_for('main.register'))

        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            role=role,
            address=address,
            latitude=latitude,
            longitude=longitude,
            specialty=specialty,
            is_active=True
        )

        db.session.add(new_user)
        db.session.commit()
        flash("✅ Account created. Please log in.")
        return redirect(url_for('main.login'))

    return render_template('register.html')

# HOME
@main.route('/')
def index():
    return render_template('landing.html')

# DASHBOARDS
@main.route('/dashboard_client')
@login_required
def dashboard_client():
    if current_user.role != 'Client':
        return redirect(url_for('main.login'))
    services = Service.query.filter_by(client_id=current_user.id).all()
    return render_template('dashboard_client.html', user=current_user, services=services)

@main.route('/dashboard_professional')
@login_required
def dashboard_professional():
    if current_user.role != 'Professional':
        return redirect(url_for('main.login'))
    services = Service.query.filter_by(status='Pending').all()
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).all()
    return render_template('dashboard_professional.html', user=current_user, services=services, notifications=notifications)

@main.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'Admin':
        flash("Access denied.")
        return redirect(url_for('main.login'))
    users = User.query.all()
    return render_template('admin_dashboard.html', users=users)

# SCHEDULE SERVICE
@main.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule_service():
    if current_user.role != 'Client':
        return redirect(url_for('main.dashboard_client'))
    if request.method == 'POST':
        service = Service(
            description=request.form['description'],
            date=request.form['date'],
            time=request.form['time'],
            address=request.form['address'],
            latitude=request.form.get('latitude'),
            longitude=request.form.get('longitude'),
            client_id=current_user.id
        )
        db.session.add(service)
        db.session.commit()
        flash('Service scheduled successfully!')
        return redirect(url_for('main.dashboard_client'))
    return render_template('schedule_service.html')

# VIEW PROFESSIONALS
@main.route('/view_professionals')
@login_required
def view_professionals():
    if current_user.role != 'Client':
        return redirect(url_for('main.login'))
    professionals = User.query.filter_by(role='Professional', is_active=True).all()
    return render_template('view_professionals.html', professionals=professionals)

# REVIEWS
@main.route('/submit_review/<int:service_id>', methods=['GET', 'POST'])
@login_required
def submit_review(service_id):
    service = Service.query.get_or_404(service_id)

    if service.client_id != current_user.id:
        flash("This service does not belong to you.")
        return redirect(url_for('main.dashboard_client'))

    if request.method == 'POST':
        rating = int(request.form['rating'])
        comment = request.form['comment']

        review = Review(
            rating=rating,
            comment=comment,
            service_id=service.id,
            client_id=current_user.id,
        )
        db.session.add(review)
        db.session.commit()
        flash("Review submitted.")
        return redirect(url_for('main.dashboard_client'))

    return render_template('submit_review.html', service=service)

# SETTINGS
@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if current_user.role not in ['Client', 'Professional']:
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        current_user.address = request.form['address']
        db.session.commit()
        flash("Profile updated.")
    return render_template('edit_profile.html', user=current_user)

# HISTORY
@main.route('/history')
@login_required
def history():
    if current_user.role == 'Client':
        services = Service.query.filter_by(client_id=current_user.id).order_by(Service.date.desc()).all()
    elif current_user.role == 'Professional':
        services = []  # Temporário
    else:
        services = []
    return render_template('history.html', services=services)

# NOTIFICATIONS
@main.route('/mark_notification_read/<int:notification_id>')
@login_required
def mark_notification_read(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id != current_user.id:
        flash("This notification is not yours.")
        return redirect(url_for('main.dashboard_professional'))

    notification.is_read = True
    db.session.commit()
    flash("Notification marked as read.")
    return redirect(url_for('main.dashboard_professional'))

# MAPS
@main.route('/map_services')
@login_required
def map_services():
    return render_template("map_services.html", services_json="[]")

@main.route('/map_professionals')
@login_required
def map_professionals():
    return render_template("map_professionals.html", professionals_json="[]")

# ADMIN LOGS
@main.route('/admin_logs')
@login_required
def admin_logs():
    if current_user.role != 'Admin':
        return redirect(url_for('main.login'))
    logs = Log.query.order_by(Log.timestamp.desc()).all()
    return render_template("admin_logs.html", logs=logs)

# TOGGLE USER STATUS
@main.route('/toggle_status/<int:user_id>')
@login_required
def toggle_status(user_id):
    if current_user.role != 'Admin':
        return redirect(url_for('main.login'))

    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("Você não pode desativar a si mesmo.")
        return redirect(url_for('main.admin_dashboard'))

    user.is_active = not user.is_active
    db.session.commit()
    flash("User status changed.")
    return redirect(url_for('main.admin_dashboard'))

# SIMPLE PAGES
@main.route('/about')
def about():
    return render_template('about.html')

# TERMS PAGE
@main.route('/terms')
def terms():
    return render_template('terms.html')

# PRIVACY PAGE
@main.route('/privacy')
def privacy():
    return render_template('privacy.html')


@main.route('/update_status/<int:service_id>/<string:new_status>')
@login_required
def update_status(service_id, new_status):
    if current_user.role != 'Professional':
        flash("Acesso negado.")
        return redirect(url_for('main.login'))

    service = Service.query.get_or_404(service_id)

    if new_status in ['Accepted', 'Rejected']:
        service.status = new_status
        db.session.commit()
        flash(f"Serviço {new_status.lower()} com sucesso!")
    else:
        flash("Status inválido.")

    return redirect(url_for('main.dashboard_professional'))
