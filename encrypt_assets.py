# encrypt_assets.py
import os
from cryptography.fernet import Fernet

# Paths
src_dir = './assets'
dst_dir = './assets_enc'
os.makedirs(dst_dir, exist_ok=True)

# Key file path
key_path = os.path.join(dst_dir, 'key.key')
# Generate a new key if not present
if not os.path.exists(key_path):
    key = Fernet.generate_key()
    with open(key_path, 'wb') as f:
        f.write(key)
    print(f'Generated new key at {key_path}')
else:
    with open(key_path, 'rb') as f:
        key = f.read()

cipher = Fernet(key)

# Encrypt all PNGs
for fname in os.listdir(src_dir):
    if fname.lower().endswith('.png'):
        data = open(os.path.join(src_dir, fname), 'rb').read()
        token = cipher.encrypt(data)
        with open(os.path.join(dst_dir, fname + '.enc'), 'wb') as out:
            out.write(token)

# print('Encrypted assets in desktop-ai/assets_enc/')