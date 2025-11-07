"""
Эндпоинты для работы с пользователями
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from datetime import datetime
from api.models import UserResponse
from database.db import Database

router = APIRouter()

def get_database():
    from api.main import db
    if db is None:
        raise HTTPException(status_code=503, detail="База данных не инициализирована")
    return db

@router.get("/check/{phone}", response_model=dict)
async def check_user_registration(
    phone: str,
    db: Database = Depends(get_database)
):
    """Проверка регистрации пользователя по номеру телефона"""
    try:
        # Ищем пользователя по телефону
        result = db.connection.execute(
            "SELECT user_id FROM users WHERE phone = ?",
            (phone,)
        ).fetchone()
        
        if result:
            user_id = result[0]
            return {
                "registered": True,
                "user_id": user_id,
                "message": "Пользователь зарегистрирован"
            }
        else:
            return {
                "registered": False,
                "message": "Пользователь не найден"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка проверки регистрации: {str(e)}")

@router.post("/register", response_model=dict)
async def register_user(
    phone: str = Query(..., description="Номер телефона (основной аргумент регистрации)"),
    user_id: Optional[int] = Query(None, description="ID пользователя (опционально)"),
    user_name: Optional[str] = Query(None, description="Имя пользователя"),
    user_first_name: Optional[str] = Query(None, description="Имя"),
    user_last_name: Optional[str] = Query(None, description="Фамилия"),
    db: Database = Depends(get_database)
):
    """Регистрация нового пользователя по номеру телефона"""
    try:
        # Проверяем, не зарегистрирован ли уже пользователь с таким телефоном
        existing_user = db.connection.execute(
            "SELECT user_id FROM users WHERE phone = ?",
            (phone,)
        ).fetchone()
        
        if existing_user:
            raise HTTPException(status_code=400, detail="Пользователь с таким номером телефона уже зарегистрирован")
        
        # Если user_id не передан, генерируем его на основе телефона
        if user_id is None:
            # Используем хеш телефона как user_id (упрощенный вариант)
            user_id = abs(hash(phone)) % (10 ** 9)
        
        # Проверяем, не существует ли уже пользователь с таким user_id
        if db.check_users_user_exists(user_id):
            raise HTTPException(status_code=400, detail="Пользователь с таким ID уже существует")
        
        # Регистрационное время
        reg_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_link = f"tg://user?id={user_id}"
        
        # Создаем пользователя
        db.add_users_user(
            user_id=user_id,
            user_link=user_link,
            user_reg_time=reg_time,
            user_name=user_name,
            user_first_name=user_first_name,
            user_last_name=user_last_name,
            coin_count=0
        )
        
        # Устанавливаем телефон
        db.set_users_phone(user_id, phone)
        
        # Создаем дефолтные анкеты
        db.set_default_q1(user_id)
        db.set_default_q2(user_id)
        
        return {
            "message": "Пользователь успешно зарегистрирован",
            "user_id": user_id,
            "phone": phone
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка регистрации: {str(e)}")
