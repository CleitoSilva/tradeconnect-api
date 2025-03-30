from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse, urljoin
from .models import User, Service, Log, Notification
from . import db
import requests
from flask import jsonify
import json

main = Blueprint('main', __name__)

# 🔒 Security: only redirect to safe URLs
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

# 🔐 LOGIN
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        print("📌 Email:", email)
        user = User.query.filter_by(email=email).first()
        print("📌 Found user:", user)

        if user:
            if not user.is_active:
                flash('This user is deactivated.')
                return redirect(url_for('main.login'))

            if check_password_hash(user.password, password):
                login_user(user)
                print("✅ Logged in as:", current_user.username)

                if user.role == 'Client':
                    return redirect(url_for('main.dashboard_client'))
                elif user.role == 'Professional':
                    return redirect(url_for('main.dashboard_professional'))
                elif user.role == 'Admin':
                    return redirect(url_for('main.admin_dashboard'))
                else:
                    flash('Invalid role.')
            else:
                flash('Incorrect password.')
        else:
            flash('User not found.')

    return render_template('login.html')

# 🧾 REGISTER
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

        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            role=role,
            address=address,
            latitude=latitude if latitude else None,
            longitude=longitude if longitude else None
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! Please log in.")  # 🔁 Alterado para inglês
        return redirect(url_for('main.login'))

    return render_template('register.html')

# 🔁 REDIRECT TO LOGIN
@main.route('/')
def index():
    return redirect(url_for('main.login'))

# 📅 SERVICE SCHEDULING
@main.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule_service():
    if current_user.role != 'Client':
        return redirect(url_for('main.dashboard_client'))

    if request.method == 'POST':
        description = request.form['description']
        date = request.form['date']
        time = request.form['time']
        address = request.form['address']
        latitude = request.form.get('latitude')  # 🧭 PEGA COORDENADAS DO FORM
        longitude = request.form.get('longitude')

        new_service = Service(
            description=description,
            date=date,
            time=time,
            address=address,
            latitude=latitude if latitude else None,
            longitude=longitude if longitude else None,
            client_id=current_user.id
        )

        db.session.add(new_service)
        db.session.commit()

        # 🔔 Notifica os profissionais
        professionals = User.query.filter_by(role='Professional', is_active=True).all()
        for prof in professionals:
            notification = Notification(
                user_id=prof.id,
                message=f"{current_user.username} scheduled a service at {address} on {date} at {time}"
            )
            db.session.add(notification)

        # 📝 Log único (✔️ corrigido)
        log = Log(action=f"{current_user.username} scheduled a service at {address} on {date} at {time}")
        db.session.add(log)

        db.session.commit()

        flash('Service scheduled successfully!')
        return redirect(url_for('main.dashboard_client'))

    return render_template('schedule_service.html')

# 👤 CLIENT DASHBOARD
@main.route('/dashboard_client')
@login_required
def dashboard_client():
    if current_user.role != 'Client':
        return redirect(url_for('main.login'))

    services = Service.query.filter_by(client_id=current_user.id).all()
    return render_template('dashboard_client.html', user=current_user, services=services)

# 👨‍🔧 PROFESSIONAL DASHBOARD
@main.route('/dashboard_professional')
@login_required
def dashboard_professional():
    if current_user.role != 'Professional':
        return redirect(url_for('main.login'))

    services = Service.query.filter_by(status='Pending').all()

    # 🔔 Get unread notifications
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).all()

    return render_template(
        'dashboard_professional.html',
        user=current_user,
        services=services,
        notifications=notifications
    )

@main.route('/mark_notification_read/<int:notification_id>')
@login_required
def mark_notification_read(notification_id):
    notification = Notification.query.get(notification_id)
    if notification and notification.user_id == current_user.id:
        notification.is_read = True
        db.session.commit()
        flash("Notification marked as read.")
    return redirect(url_for('main.dashboard_professional'))

# 🔄 UPDATE SERVICE STATUS
@main.route('/update_status/<int:service_id>/<string:new_status>')
@login_required
def update_status(service_id, new_status):
    service = Service.query.get(service_id)

    if current_user.role != 'Professional' or not service:
        return redirect(url_for('main.dashboard_professional'))

    service.status = new_status

    # 🔍 LOG
    log = Log(action=f"{current_user.username} updated service #{service.id} to {new_status}")
    db.session.add(log)

    db.session.commit()
    return redirect(url_for('main.dashboard_professional'))

# 🧑‍💼 ADMIN DASHBOARD
@main.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'Admin':
        flash("Access denied.")
        return redirect(url_for('main.login'))

    users = User.query.all()
    return render_template('admin_dashboard.html', users=users)

# 🔁 TOGGLE ACTIVE STATUS
@main.route('/toggle_status/<int:user_id>')
@login_required
def toggle_status(user_id):
    if current_user.role != 'Admin':
        flash("Access denied.")
        return redirect(url_for('main.login'))

    user = User.query.get(user_id)
    if user:
        user.is_active = not user.is_active

        status_txt = 'activated' if user.is_active else 'deactivated'
        log = Log(action=f"Admin {current_user.username} {status_txt} user {user.username}")
        db.session.add(log)

        db.session.commit()
        flash(f"User {user.username} is now {'active' if user.is_active else 'inactive'}.")

    return redirect(url_for('main.admin_dashboard'))

# 📜 VIEW LOGS (ADMIN)
@main.route('/admin_logs')
@login_required
def admin_logs():
    if current_user.role != 'Admin':
        flash("Access denied.")
        return redirect(url_for('main.login'))

    logs = Log.query.order_by(Log.timestamp.desc()).all()
    return render_template('admin_logs.html', logs=logs)

# 🚪 LOGOUT
@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/mark_notifications_read', methods=['POST'])
@login_required
def mark_notifications_read():
    if current_user.role != 'Professional':
        flash("Access denied.")
        return redirect(url_for('main.login'))

    for note in current_user.notifications:
        note.is_read = True

    db.session.commit()
    flash("All notifications marked as read.")
    return redirect(url_for('main.dashboard_professional'))

# Profile
# 🔧 EDIT PROFILE
@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    # Allow both Client and Professional roles
    if current_user.role not in ['Client', 'Professional']:
        flash("Access denied.")
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        address = request.form['address']
        current_user.address = address

        # 🌍 Get coordinates using Google Maps API
        api_key = 'AIzaSyBVoEt5W58vz-76LWwftrIHww4FBnvGVmo'
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
        response = requests.get(geocode_url).json()

        if response['status'] == 'OK':
            location = response['results'][0]['geometry']['location']
            current_user.latitude = location['lat']
            current_user.longitude = location['lng']
            db.session.commit()
            flash("Location updated successfully!")
        else:
            flash("Could not find location. Please check the address.")

    return render_template('edit_profile.html', user=current_user)

# map
@main.route('/map_professionals')
@login_required
def map_professionals():
    professionals = User.query.filter_by(role='Professional', is_active=True).all()

    professionals_json = json.dumps([
        {
            "username": user.username,
            "latitude": user.latitude,
            "longitude": user.longitude
        }
        for user in professionals if user.latitude and user.longitude
    ])

    return render_template("map_professionals.html", professionals_json=professionals_json)

@main.route('/map_services')
@login_required
def map_services():
    if current_user.role not in ['Professional', 'Client']:
        return redirect(url_for('main.dashboard_client'))

    services = Service.query.filter(
        Service.latitude.isnot(None), 
        Service.longitude.isnot(None)
    ).all()

    services_json = json.dumps([
        {
            "id": s.id,
            "description": s.description,
            "date": s.date,
            "time": s.time,
            "address": s.address,
            "latitude": s.latitude,
            "longitude": s.longitude
        }
        for s in services
    ])

    return render_template("map_services.html", services_json=services_json)


# History
@main.route('/history')
@login_required
def history():
    if current_user.role == 'Client':
        services = Service.query.filter_by(client_id=current_user.id).order_by(Service.date.desc()).all()
    elif current_user.role == 'Professional':
        services = Service.query.order_by(Service.date.desc()).all()
    else:
        flash("Access denied.")
        return redirect(url_for('main.login'))

    return render_template('history.html', services=services)
