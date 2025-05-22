# config.py
import secrets

SECRET_KEY = secrets.token_hex(16)  # Tạo một khóa bí mật ngẫu nhiên
ALGORITHM = 'HS256'
