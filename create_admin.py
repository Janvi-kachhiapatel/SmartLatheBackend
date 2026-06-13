from database import SessionLocal
from models import User
from auth import hash_password

db = SessionLocal()

existing = (
    db.query(User)
    .filter(User.username == "admin")
    .first()
)

if existing:
    print("Admin already exists")

else:
    user = User(
    username="admin",
    email="yourgmail@gmail.com",
    password_hash=hash_password("admin123"),
    role="administrator",
    is_active=True,
)

    db.add(user)
    db.commit()

    print("Admin Created")