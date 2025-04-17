from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'segredo123'

    # ✅ DATABASE (PostgreSQL no Render)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", 'sqlite:///local.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from . import models
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.create_all()

        # ✅ Criação automática de usuários padrão
        if not User.query.filter_by(email="admin@tradeconnect.com").first():
            admin = User(
                username="superadmin",
                email="admin@tradeconnect.com",
                password=generate_password_hash("UltraSecurePass123"),
                role="Admin",
                address="Admin HQ",
                is_active=True
            )
            db.session.add(admin)

        if not User.query.filter_by(email="cliente@tradeconnect.com").first():
            client = User(
                username="clientezin",
                email="cliente@tradeconnect.com",
                password=generate_password_hash("Cliente123"),
                role="Client",
                address="Rua do Cliente",
                is_active=True
            )
            db.session.add(client)

        if not User.query.filter_by(email="pro@tradeconnect.com").first():
            pro = User(
                username="profissionalzão",
                email="pro@tradeconnect.com",
                password=generate_password_hash("Pro123"),
                role="Professional",
                specialty="Eletricista",
                address="Rua do Profissional",
                is_active=True
            )
            db.session.add(pro)

        db.session.commit()
        print("✅ Usuários criados com sucesso.")

    return app