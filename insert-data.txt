import base64
from cryptography.fernet import Fernet
from sanic import Sanic
from sanic.response import json
from sanic_cors import CORS
import sqlite3

app = Sanic("api_server")
CORS(app)

# Generate encryption key and Fernet instance
encryption_key = Fernet.generate_key()
cipher = Fernet(encryption_key)

conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        encrypted_password BLOB NOT NULL
    )
    """
)
conn.commit()

# conn = sqlite3.connect("users.db")
# cursor = conn.cursor()
# cursor.execute("SELECT * FROM table_name;")
# conn.commit()

conn.close()