# app/models.py
# Define o modelo de usuário

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from . import db

# Modelo de usuário
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # Cliente ou Profissional

class Servico(db.Model):
    __tablename__ = 'servicos'

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    data = db.Column(db.String(20), nullable=False)
    horario = db.Column(db.String(10), nullable=False)
    
    cliente_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    cliente = db.relationship('User', backref='servicos')
