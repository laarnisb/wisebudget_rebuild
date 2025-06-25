import bcrypt
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import os

# --- Password hashing ---
def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# --- AES-256 encryption ---
KEY = os.environ.get("ENCRYPTION_KEY", None)
if KEY is None:
    raise ValueError("Missing AES-256 encryption key. Set ENCRYPTION_KEY in environment variables.")
key = KEY.encode("utf-8")[:32]  # ensure 32 bytes

def encrypt_data(data):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data.encode("utf-8"))
    return base64.b64encode(nonce + tag + ciphertext).decode("utf-8")

def decrypt_data(encoded):
    raw = base64.b64decode(encoded)
    nonce, tag, ciphertext = raw[:16], raw[16:32], raw[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag).decode("utf-8")
