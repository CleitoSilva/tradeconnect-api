from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Servico
from . import db

main = Blueprint('main', __name__)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user)
            if user.role == 'Cliente':
                return redirect(url_for('main.dashboard_cliente'))
            else:
                return redirect(url_for('main.dashboard_profissional'))
        else:
            flash('Invalid login.')

    return render_template('login.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        new_user = User(
            username=username,
            email=email,
            password=password,  # você pode trocar por senha criptografada depois
            role=role
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('main.login'))

    return render_template('register.html')

@main.route('/')
def index():
    return redirect(url_for('main.login'))

@main.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule_service():
    if current_user.role != 'Cliente':
        return redirect(url_for('main.dashboard_cliente'))

    if request.method == 'POST':
        descricao = request.form['descricao']
        data = request.form['data']
        horario = request.form['horario']

        new_service = Servico(
            descricao=descricao,
            data=data,
            horario=horario,
            cliente_id=current_user.id
        )

        db.session.add(new_service)
        db.session.commit()

        flash('Service scheduled successfully!')
        return redirect(url_for('main.dashboard_cliente'))

    return render_template('schedule_service.html')