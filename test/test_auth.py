import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.auth import hash_password, verify_password

def test_password_is_hashed():
    """Password should not be stored as plain text."""
    password = "TestPassword123"
    hashed = hash_password(password)
    assert hashed != password

def test_correct_password_verifies():
    """Correct password should verify against its hash."""
    password = "TestPassword123"
    hashed = hash_password(password)
    assert verify_password(password, hashed) == True

def test_wrong_password_fails():
    """Wrong password should not verify against hash."""
    password = "TestPassword123"
    hashed = hash_password(password)
    assert verify_password("WrongPassword", hashed) == False

def test_same_password_different_hashes():
    """Same password hashed twice should produce different hashes."""
    password = "TestPassword123"
    hash1 = hash_password(password)
    hash2 = hash_password(password)
    assert hash1 != hash2