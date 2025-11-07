"""
Система аутентификации для Food2Mood API
"""

import jwt
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional
import os

# Секретный ключ для JWT (в продакшене должен быть в переменных окружения)
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "korean-chick-secret-key-2024")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(user_id: int, user_type: str = "client") -> str:
    """Создать JWT токен для пользователя"""
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "user_id": user_id,
        "user_type": user_type,
        "exp": expire,
        "iat": datetime.utcnow()
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[int]:
    """Проверить JWT токен и вернуть user_id"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            return None
        return user_id
    except jwt.PyJWTError:
        return None

def create_api_key() -> str:
    """Создать API ключ для администраторов"""
    return secrets.token_urlsafe(32)

def hash_password(password: str) -> str:
    """Хешировать пароль"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed_password: str) -> bool:
    """Проверить пароль"""
    return hash_password(password) == hashed_password

# Простая система API ключей (в продакшене лучше использовать более сложную систему)
API_KEYS = {
    "admin": "korean-chick-admin-key-2024",
    "waiter": "korean-chick-waiter-key-2024",
    "client": "korean-chick-client-key-2024"
}

def verify_api_key(api_key: str) -> Optional[str]:
    """Проверить API ключ и вернуть тип пользователя"""
    for user_type, key in API_KEYS.items():
        if key == api_key:
            return user_type
    return None

def get_user_type_from_token(token: str) -> Optional[str]:
    """Получить тип пользователя из токена"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("user_type")
    except jwt.PyJWTError:
        return None
