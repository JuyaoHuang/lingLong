"""
Simple admin user creator without bcrypt issues
"""
import sys
import hashlib
import sqlite3

def create_simple_admin():
    """Create admin user with simple hash (for testing only)"""

    # Simple hash for testing (NOT for production)
    password = "admin"
    # Using bcrypt manually with a fixed salt for testing
    import bcrypt
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

    # Connect to database
    conn = sqlite3.connect('/code/data/dataBase.db')
    cursor = conn.cursor()

    try:
        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE username = ?", ("admin",))
        if cursor.fetchone():
            print("Admin user already exists!")
            print("Username: admin")
            print("Password: admin")
            return

        # Insert new user
        cursor.execute(
            "INSERT INTO users (username, hashed_password) VALUES (?, ?)",
            ("admin", hashed.decode('utf-8'))
        )
        conn.commit()

        print("Admin user created successfully!")
        print("Username: admin")
        print("Password: admin")
        print("\nYou can now login at http://localhost:8000/docs")

    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    create_simple_admin()