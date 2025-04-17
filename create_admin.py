from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()
app.app_context().push()

# Check if admin already exists
existing = User.query.filter_by(email="admin@tradeconnect.com").first()

if not existing:
    admin = User(
        username="superadmin",
        email="admin@tradeconnect.com",
        password=generate_password_hash("UltraSecurePass123"),
        role="Admin",
        address="Admin Headquarters",
        is_active=True
    )

    db.session.add(admin)
    db.session.commit()
    print("✅ Admin user created successfully!")
else:
    print("⚠️ Admin user already exists.")
