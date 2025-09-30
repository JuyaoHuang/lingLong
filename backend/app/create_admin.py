"""
Create initial admin user script
Run this script to create the first admin user in the database
"""
import sys
sys.path.append('/code')

from app.data.database import SessionLocal, create_tables
from app.data.models import User
from app.core.security import get_password_hash

def create_admin_user():
    """Create initial admin user"""
    # Create database tables
    create_tables()

    # Create database session
    db = SessionLocal()

    try:
        # Check if admin user already exists
        existing_user = db.query(User).filter(User.username == "admin").first()

        if existing_user:
            print("Admin user already exists!")
            print(f"Username: admin")
            print("Password: admin")
            return

        # Create new admin user
        admin_password = "admin"  # Simplified password
        hashed_password = get_password_hash(admin_password)

        admin_user = User(
            username="admin",
            hashed_password=hashed_password
        )

        db.add(admin_user)
        db.commit()

        print("Admin user created successfully!")
        print(f"Username: admin")
        print(f"Password: {admin_password}")
        print("\nYou can now login at http://localhost:8000/docs")

    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()