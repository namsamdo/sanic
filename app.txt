import base64,os
from cryptography.fernet import Fernet,InvalidToken
from sanic import Sanic
from sanic.response import json
from sanic_cors import CORS
import sqlite3

app = Sanic("api_server")
CORS(app)

# Generate encryption key and Fernet instance
# encryption_key = Fernet.generate_key()
# encryption_key = "Fs9YrlmGcnXUhl1fo6MTs-7161171kcz1Sm90zfGq2c="


KEY_FILE = "encryption_key.txt"
# Load or generate encryption key
if os.path.exists(KEY_FILE):
    with open(KEY_FILE, "rb") as f:
        encryption_key = f.read()
else:
    encryption_key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(encryption_key)
cipher = Fernet(encryption_key)

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

def insert_encrypted_password(username, encrypted_password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, encrypted_password) VALUES (?, ?)",
        (username, sqlite3.Binary(encrypted_password)),  # Wrap encrypted_password in sqlite3.Binary
    )
    conn.commit()

@app.post("/register")
async def register(request):
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        encrypted_password = cipher.encrypt(password.encode())
        try:
            insert_encrypted_password(username, encrypted_password)
            return json({"message": "User registered successfully"}, status=201)
        except sqlite3.IntegrityError:
            return json({"message": "Username already exists"}, status=409)
    else:
        return json({"message": "Username and password are required"}, status=400)

@app.post("/login")
async def login(request):
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        cursor.execute("SELECT encrypted_password FROM users WHERE username=?", (username,))
        result = cursor.fetchone()
        if result:
            encrypted_password = bytes(result[0])  # Convert the retrieved data to bytes
            try:
                decrypted_password = cipher.decrypt(encrypted_password).decode()
                if password == decrypted_password:
                    return json({"message": "Login successful"}, status=200)
                else:
                    return json({"message": "Invalid password"}, status=401)
            except:
                return json({"message": "Invalid encryption token"}, status=500)
        else:
            return json({"message": "User not found"}, status=404)
    else:
        return json({"message": "Username and password are required"}, status=400)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)