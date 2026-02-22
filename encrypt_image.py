import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from base64 import urlsafe_b64encode
from PIL import Image

password = b"mysecretpassword"

input_image = "sample.jpg"
output_file = "encrypted_image.bin"

# Read image as binary
with open(input_image, "rb") as f:
    data = f.read()

# Generate salt
salt = os.urandom(16)

# Key derivation
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
key = kdf.derive(password)

# Random IV
iv = os.urandom(16)

# Padding
padder = padding.PKCS7(128).padder()
padded_data = padder.update(data) + padder.finalize()

cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
encryptor = cipher.encryptor()
encrypted = encryptor.update(padded_data) + encryptor.finalize()

# Save encrypted file
with open(output_file, "wb") as f:
    f.write(salt + iv + encrypted)

print("Image encrypted successfully.")