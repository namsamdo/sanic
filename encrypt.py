import base64
from cryptography.fernet import Fernet






encryption_key = Fernet.generate_key()
cipher = Fernet(encryption_key)
encrypted_password = cipher.encrypt('1111Aa'.encode())
print(encrypted_password)

decrypted_password = cipher.decrypt(encrypted_password).decode()
print(decrypted_password)