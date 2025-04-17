from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()

    professionals = [
        {
            "username": "michael_carter", "email": "michael@example.com", "password": "123456",
            "role": "Professional", "address": "Brooklyn, NY", "specialty": "Plumber",
            "photo": "https://randomuser.me/api/portraits/men/1.jpg"
        },
        {
            "username": "james_walker", "email": "james@example.com", "password": "123456",
            "role": "Professional", "address": "San Diego, CA", "specialty": "Electrician",
            "photo": "https://randomuser.me/api/portraits/men/2.jpg"
        },
        {
            "username": "ryan_mitchell", "email": "ryan@example.com", "password": "123456",
            "role": "Professional", "address": "Chicago, IL", "specialty": "Painter",
            "photo": "https://randomuser.me/api/portraits/men/3.jpg"
        },
        {
            "username": "william_harris", "email": "william@example.com", "password": "123456",
            "role": "Professional", "address": "Austin, TX", "specialty": "Carpenter",
            "photo": "https://randomuser.me/api/portraits/men/4.jpg"
        },
        {
            "username": "daniel_lewis", "email": "daniel@example.com", "password": "123456",
            "role": "Professional", "address": "Seattle, WA", "specialty": "Handyman",
            "photo": "https://randomuser.me/api/portraits/men/5.jpg"
        },
        {
            "username": "john_thompson", "email": "john@example.com", "password": "123456",
            "role": "Professional", "address": "Miami, FL", "specialty": "Roofer",
            "photo": "https://randomuser.me/api/portraits/men/6.jpg"
        },
        {
            "username": "ethan_hall", "email": "ethan@example.com", "password": "123456",
            "role": "Professional", "address": "Denver, CO", "specialty": "Welder",
            "photo": "https://randomuser.me/api/portraits/men/7.jpg"
        },
        {
            "username": "aaron_white", "email": "aaron@example.com", "password": "123456",
            "role": "Professional", "address": "Phoenix, AZ", "specialty": "HVAC Technician",
            "photo": "https://randomuser.me/api/portraits/men/8.jpg"
        },
        {
            "username": "tyler_green", "email": "tyler@example.com", "password": "123456",
            "role": "Professional", "address": "Atlanta, GA", "specialty": "Floor Installer",
            "photo": "https://randomuser.me/api/portraits/men/9.jpg"
        },
        {
            "username": "brandon_brown", "email": "brandon@example.com", "password": "123456",
            "role": "Professional", "address": "Detroit, MI", "specialty": "Masonry",
            "photo": "https://randomuser.me/api/portraits/men/10.jpg"
        },
        {
            "username": "logan_scott", "email": "logan@example.com", "password": "123456",
            "role": "Professional", "address": "Boston, MA", "specialty": "Glazier",
            "photo": "https://randomuser.me/api/portraits/men/11.jpg"
        },
        {
            "username": "cole_baker", "email": "cole@example.com", "password": "123456",
            "role": "Professional", "address": "Cleveland, OH", "specialty": "Drywall Installer",
            "photo": "https://randomuser.me/api/portraits/men/12.jpg"
        },
        {
            "username": "owen_reed", "email": "owen@example.com", "password": "123456",
            "role": "Professional", "address": "Dallas, TX", "specialty": "Fence Builder",
            "photo": "https://randomuser.me/api/portraits/men/13.jpg"
        },
        {
            "username": "leo_jordan", "email": "leo@example.com", "password": "123456",
            "role": "Professional", "address": "Portland, OR", "specialty": "Window Installer",
            "photo": "https://randomuser.me/api/portraits/men/14.jpg"
        },
        {
            "username": "luke_west", "email": "luke@example.com", "password": "123456",
            "role": "Professional", "address": "Las Vegas, NV", "specialty": "Garage Door Tech",
            "photo": "https://randomuser.me/api/portraits/men/15.jpg"
        }
    ]

    for pro in professionals:
        exists = User.query.filter_by(email=pro["email"]).first()
        if not exists:
            user = User(
                username=pro["username"],
                email=pro["email"],
                password=generate_password_hash(pro["password"]),
                role=pro["role"],
                address=pro["address"],
                specialty=pro["specialty"],
                photo=pro["photo"],
                is_active=True
            )
            db.session.add(user)

    db.session.commit()
    print("✅ 15 professionals added successfully!")
