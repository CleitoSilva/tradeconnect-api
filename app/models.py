from flask_login import UserMixin
from datetime import datetime
from . import db

# 🧑 User model
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'  # ESSENCIAL! Esse nome precisa bater com os ForeignKeys

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # Client, Professional, Admin
    address = db.Column(db.String(200))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    is_active = db.Column(db.Boolean, default=True)
    photo = db.Column(db.String(255))
    specialty = db.Column(db.String(100))

    # ✅ Relationships corrigidos
    services = db.relationship('Service', foreign_keys='Service.client_id', backref='client', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)
    reviews_written = db.relationship('Review', foreign_keys='Review.client_id', backref='client')
    reviews_received = db.relationship('Review', foreign_keys='Review.professional_id', backref='professional')




# 📅 Service model
class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), default='Pending')  # Pending, Accepted, Rejected
    address = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    specialty = db.Column(db.String(100))
    photo = db.Column(db.String(255))

    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)



# 📝 Review model
from datetime import datetime  # já deve estar no topo

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)

    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    professional_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    service = db.relationship('Service', backref='review')


# 🔔 Notification model
class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)


# 🧾 Log model
class Log(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)