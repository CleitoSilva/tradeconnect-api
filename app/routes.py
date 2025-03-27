from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse, urljoin
from .models import User, Service
from . import db

main = Blueprint('main', __name__)

# 🔒 Segurança no redirecionamento
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        print("📌 Email digitado:", email)
        user = User.query.filter_by(email=email).first()
        print("📌 Usuário encontrado:", user)

        if user:
            # ❌ Block login if user is not active
            if not user.is_active:
                flash('This user is deactivated.')
                return redirect(url_for('main.login'))

            # ✅ Check password hash
            if check_password_hash(user.password, password):
                print("🔒 Senha correta:", True)
                login_user(user)
                print("✅ Login feito!")
                print("🙋 Autenticado:", current_user.is_authenticated)

                # 🔁 Redirect based on user role
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

# 🧾 Registro
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            role=role
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('main.login'))

    return render_template('register.html')

# 🔁 Redireciona para login
@main.route('/')
def index():
    return redirect(url_for('main.login'))

# 📅 Agendamento de serviço
@main.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule_service():
    if current_user.role != 'Client':
        return redirect(url_for('main.dashboard_client'))

    if request.method == 'POST':
        description = request.form['description']
        date = request.form['date']
        time = request.form['time']

        new_service = Service(
            description=description,
            date=date,
            time=time,
            client_id=current_user.id
        )

        db.session.add(new_service)
        db.session.commit()

        flash('Service scheduled successfully!')
        return redirect(url_for('main.dashboard_client'))

    return render_template('schedule_service.html')

# 👤 Dashboard do cliente
@main.route('/dashboard_client')
@login_required
def dashboard_client():
    if current_user.role != 'Client':
        return redirect(url_for('main.login'))

    services = Service.query.filter_by(client_id=current_user.id).all()
    return render_template('dashboard_client.html', user=current_user, services=services)

# 👨‍🔧 Dashboard do profissional
@main.route('/dashboard_professional')
@login_required
def dashboard_professional():
    if current_user.role != 'Professional':
        return redirect(url_for('main.login'))

    services = Service.query.filter_by(status='Pending').all()
    return render_template('dashboard_professional.html', user=current_user, services=services)

# ✅ Atualizar status do serviço (profissional)
@main.route('/update_status/<int:service_id>/<string:new_status>')
@login_required
def update_status(service_id, new_status):
    service = Service.query.get(service_id)

    if current_user.role != 'Professional' or not service:
        return redirect(url_for('main.dashboard_professional'))

    service.status = new_status
    db.session.commit()
    return redirect(url_for('main.dashboard_professional'))

# 🚪 Logout
@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'Admin':
        flash("Access denied.")
        return redirect(url_for('main.login'))

    users = User.query.all()
    return render_template('admin_dashboard.html', users=users)

# app/routes.py

@main.route('/toggle_status/<int:user_id>')
@login_required
def toggle_status(user_id):
    if current_user.role != 'Admin':
        flash("Acesso negado.")
        return redirect(url_for('main.login'))

    user = User.query.get(user_id)
    if user:
        user.is_active = not user.is_active
        db.session.commit()
        flash(f"Usuário {user.username} agora está {'ativo' if user.is_active else 'desativado'}.")
    
    return redirect(url_for('main.admin_dashboard'))
