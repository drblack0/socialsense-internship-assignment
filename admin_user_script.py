# create_first_admin.py
from app.db.session import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User

db = SessionLocal()

# --- !! CHANGE THESE VALUES !! ---
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "adminpassword"
# ------------------------------------

# Check if the user already exists
user = db.query(User).filter(User.username == ADMIN_USERNAME).first()

if not user:
    admin_user = User(
        username=ADMIN_USERNAME,
        hashed_password=get_password_hash(ADMIN_PASSWORD),
        role="admin",
    )
    db.add(admin_user)
    db.commit()
    print(f"Admin user '{ADMIN_USERNAME}' created successfully.")
else:
    print(f"Admin user '{ADMIN_USERNAME}' already exists.")

db.close()
