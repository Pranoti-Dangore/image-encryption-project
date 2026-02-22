import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

password = b"mysecretpassword"

input_file = "encrypted_image.bin"
output_image = "decrypted_image.jpg"

with open(input_file, "rb") as f:
    data = f.read()

salt = data[:16]
iv = data[16:32]
encrypted_data = data[32:]

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
)
key = kdf.derive(password)

cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
decryptor = cipher.decryptor()
decrypted_padded = decryptor.update(encrypted_data) + decryptor.finalize()

unpadder = padding.PKCS7(128).unpadder()
decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()

with open(output_image, "wb") as f:
    f.write(decrypted)

print("Image decrypted successfully.")