
import sqlite3
import os
import re
import hashlib
import secrets
import hmac


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE_DIR = os.path.join(BASE_DIR, "database")

DATABASE_PATH = os.path.join(DATABASE_DIR, "users.db")


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    """
    Create and return a connection to the SQLite database.
    """

    os.makedirs(DATABASE_DIR, exist_ok=True)

    connection = sqlite3.connect(
        DATABASE_PATH,
        timeout=10
    )

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def initialize_database():
    """
    Create the users table if it does not already exist.
    """

    connection = get_connection()

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                full_name TEXT NOT NULL,

                username TEXT NOT NULL COLLATE NOCASE UNIQUE,

                email TEXT NOT NULL COLLATE NOCASE UNIQUE,

                password_hash TEXT NOT NULL,

                salt TEXT NOT NULL,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
        """)

        connection.commit()

        print("Database initialized successfully!")

    except sqlite3.Error as error:

        print("Database initialization error:", error)

        raise

    finally:

        connection.close()


# ============================================================
# USERNAME VALIDATION
# ============================================================

def get_username_validation(username):
    """
    Return username validation results for live interface feedback.
    """

    username = username.strip()

    return {
        "length": 3 <= len(username) <= 30,
        "characters": bool(
            re.fullmatch(r"[A-Za-z0-9_.]+", username)
        )
    }


def validate_username(username):
    """
    Check whether a username satisfies registration rules.
    """

    if not username or not username.strip():
        return False, "Username is required."

    validation = get_username_validation(username)

    if not validation["length"]:
        return False, "Username must contain 3 to 30 characters."

    if not validation["characters"]:
        return False, (
            "Username can contain letters, numbers, "
            "dots and underscores only."
        )

    return True, "Username is valid."


def check_username(username):
    """
    Check whether a username is already registered.

    Returns:
        True  = Username already exists.
        False = Username is available.
    """

    username = username.strip()

    connection = get_connection()

    try:

        result = connection.execute(
            """
            SELECT id
            FROM users
            WHERE username = ?
            """,
            (username,)
        ).fetchone()

        return result is not None

    finally:

        connection.close()


def is_username_available(username):
    """
    Check whether a username can be registered.
    """

    if not username or not username.strip():
        return False

    return not check_username(username)


# ============================================================
# EMAIL VALIDATION
# ============================================================

def validate_email(email):
    """
    Check whether the email address has a basic valid format.
    """

    email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    return re.fullmatch(email_pattern, email) is not None


# ============================================================
# PASSWORD LIVE VALIDATION
# ============================================================

def get_password_validation(password):
    """
    Return individual password requirements.

    These results can be used by the registration screen
    to display red and green validation indicators.
    """

    return {
        "length": len(password) >= 11,
        "uppercase": bool(re.search(r"[A-Z]", password)),
        "lowercase": bool(re.search(r"[a-z]", password)),
        "number": bool(re.search(r"[0-9]", password)),
        "special": bool(re.search(r"[^A-Za-z0-9\s]", password))
    }


def validate_password(password):
    """
    Check all password security requirements.

    Required:
        At least 11 characters.
        At least one uppercase letter.
        At least one lowercase letter.
        At least one number.
        At least one special character.
    """

    if not password:
        return False, "Password is required."

    validation = get_password_validation(password)

    if not validation["length"]:
        return False, "Password must contain at least 11 characters."

    if not validation["uppercase"]:
        return False, "Password must contain an uppercase letter."

    if not validation["lowercase"]:
        return False, "Password must contain a lowercase letter."

    if not validation["number"]:
        return False, "Password must contain at least one number."

    if not validation["special"]:
        return False, "Password must contain a special character."

    return True, "Password is strong."


# ============================================================
# PASSWORD HASHING
# ============================================================

def hash_password(password):
    """
    Hash a password using PBKDF2-HMAC-SHA256.

    A unique random salt is generated for each password.

    Returns:
        password_hash, salt
    """

    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        300000
    )

    return password_hash.hex(), salt.hex()


# ============================================================
# PASSWORD VERIFICATION
# ============================================================

def verify_password(password, stored_hash, stored_salt):
    """
    Verify a password against its stored hash and salt.
    """

    try:

        salt = bytes.fromhex(stored_salt)

        new_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            300000
        )

        return hmac.compare_digest(
            new_hash.hex(),
            stored_hash
        )

    except (ValueError, TypeError):
        return False


# ============================================================
# USER REGISTRATION
# ============================================================

def register_user(full_name, username, email, password):
    """
    Register a new user.

    Returns:
        (True, success_message) if registration succeeds.
        (False, error_message) if registration fails.
    """

    full_name = full_name.strip()

    username = username.strip()

    email = email.strip().lower()

    # Check empty fields
    if not full_name or not username or not email or not password:

        return False, "All fields are required."

    # Check username rules
    username_valid, username_message = validate_username(username)

    if not username_valid:
        return False, username_message

    # Check email format
    if not validate_email(email):

        return False, "Please enter a valid email address."

    # Check password security rules
    password_valid, password_message = validate_password(password)

    if not password_valid:
        return False, password_message

    connection = get_connection()

    try:

        # Check duplicate username
        existing_username = connection.execute(
            """
            SELECT id
            FROM users
            WHERE username = ?
            """,
            (username,)
        ).fetchone()

        if existing_username:

            return False, "This username is already registered."

        # Check duplicate email
        existing_email = connection.execute(
            """
            SELECT id
            FROM users
            WHERE email = ?
            """,
            (email,)
        ).fetchone()

        if existing_email:

            return False, "This email address is already registered."

        # Hash the password
        password_hash, salt = hash_password(password)

        # Insert new user
        connection.execute(
            """
            INSERT INTO users (
                full_name,
                username,
                email,
                password_hash,
                salt
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                full_name,
                username,
                email,
                password_hash,
                salt
            )
        )

        connection.commit()

        return True, "Account created successfully!"

    except sqlite3.IntegrityError:

        return False, "Username or email is already registered."

    except sqlite3.Error as error:

        return False, f"Database error: {error}"

    finally:

        connection.close()


# ============================================================
# USER LOGIN / AUTHENTICATION
# ============================================================

def authenticate_user(username, password):
    username = username.strip()

    if not username or not password:
        return None

    connection = get_connection()

    try:
        user = connection.execute(
            """
            SELECT *
            FROM users
            WHERE username = ? OR email = ?
            """,
            (username, username)
        ).fetchone()

        if user is None:
            return None

        if not verify_password(
            password,
            user["password_hash"],
            user["salt"]
        ):
            return None

        return {
            "id": user["id"],
            "full_name": user["full_name"],
            "username": user["username"],
            "email": user["email"],
            "created_at": user["created_at"]
        }

    finally:
        connection.close()

# ============================================================
# GET USER INFORMATION BY ID
# ============================================================

def get_user_by_id(user_id):
    """
    Retrieve a user's profile using their unique ID.
    """

    connection = get_connection()

    try:

        user = connection.execute(
            """
            SELECT
                id,
                full_name,
                username,
                email,
                created_at
            FROM users
            WHERE id = ?
            """,
            (user_id,)
        ).fetchone()

        if user is None:

            return None

        return dict(user)

    finally:

        connection.close()


# ============================================================
# GET USER INFORMATION BY USERNAME
# ============================================================

def get_user_by_username(username):
    """
    Retrieve user information using username.
    """

    connection = get_connection()

    try:

        user = connection.execute(
            """
            SELECT
                id,
                full_name,
                username,
                email,
                created_at
            FROM users
            WHERE username = ?
            """,
            (username.strip(),)
        ).fetchone()

        if user is None:

            return None

        return dict(user)

    finally:

        connection.close()
