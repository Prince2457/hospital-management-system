import bcrypt
from utils.db_helpers import execute_query

def hash_password(password):
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password, hashed_password):
    """Verify a password against its hash"""
    return bcrypt.checkpw(
        password.encode('utf-8'), 
        hashed_password.encode('utf-8')
)


def create_user(username, password, role, full_name, email=None, phone=None):
    """Create a new user with hashed password."""
    hashed = hash_password(password)
    return execute_query(
        """INSERT INTO users 
        (username, password_hash, role, full_name, email, phone)
        VALUES (%s,%s,%s,%s,%s,%s)""",
        (username, hashed, role, full_name, email, phone), commit=True
    )

def login (username, password):
    user = execute_query(
        "SELECT * FROM users WHERE username = %s AND is_active = 1",(username,),fetch="one"
    )
    if not user:
        return None
    if verify_password(password, user['password_hash']):
        execute_query(
            "UPDATE users SET last_login = NOW() WHERE user_id =%s",
            (user['user_id'],), commit= True
        )
        return user
    return None