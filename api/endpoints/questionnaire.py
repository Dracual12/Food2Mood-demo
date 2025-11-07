"""
Эндпоинты для работы с анкетами пользователей
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from pydantic import BaseModel
from database.db import Database

router = APIRouter()

def get_database():
    from api.main import db
    if db is None:
        raise HTTPException(status_code=503, detail="База данных не инициализирована")
    return db

class QuestionnaireData(BaseModel):
    """Модель данных анкеты"""
    user_id: int
    # Первая анкета (настроение и голод)
    mood: Optional[str] = None  # Спокойствие, Радость, Печаль, Гнев, Волнение
    hungry: Optional[int] = None  # 2, 5, 7, 10
    prefers: Optional[str] = None  # "Мне как обычно", "Хочу экспериментов"
    # Вторая анкета (предпочтения)
    sex: Optional[str] = None  # Мужчина, Женщина
    age: Optional[str] = None  # До 18, 18-25, 26-35, 36-45, 45+
    food_style: Optional[str] = None  # Стандартное, Диетическое, Вегетарианское, Веганское, Кето, Палео
    ccal: Optional[str] = None  # <300, <500, <700
    dont_like_to_eat: Optional[str] = None  # Список продуктов через запятую
    like_to_eat: Optional[str] = None  # Список продуктов через запятую

@router.post("/questionnaire", response_model=dict)
async def submit_questionnaire(
    questionnaire_data: QuestionnaireData,
    db: Database = Depends(get_database)
):
    """Отправка параметров анкеты с вставкой в базу данных"""
    try:
        # Проверяем, существует ли пользователь
        if not db.check_users_user_exists(questionnaire_data.user_id):
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        # Обновляем первую анкету (users_anketa1)
        if questionnaire_data.mood is not None:
            db.set_temp_users_mood(questionnaire_data.user_id, questionnaire_data.mood)
        
        if questionnaire_data.hungry is not None:
            db.set_temp_users_hungry(questionnaire_data.user_id, questionnaire_data.hungry)
        
        if questionnaire_data.prefers is not None:
            db.set_temp_users_prefers(questionnaire_data.user_id, questionnaire_data.prefers)
        
        # Обновляем вторую анкету (users_anketa2)
        if questionnaire_data.sex is not None:
            db.set_temp_users_sex(questionnaire_data.user_id, questionnaire_data.sex)
        
        if questionnaire_data.age is not None:
            db.set_temp_users_age(questionnaire_data.user_id, questionnaire_data.age)
        
        if questionnaire_data.food_style is not None:
            db.set_temp_users_food_style(questionnaire_data.user_id, questionnaire_data.food_style)
        
        if questionnaire_data.ccal is not None:
            db.set_temp_users_ccal(questionnaire_data.user_id, questionnaire_data.ccal)
        
        if questionnaire_data.dont_like_to_eat is not None:
            db.set_temp_users_dont_like_to_eat(questionnaire_data.user_id, questionnaire_data.dont_like_to_eat)
        
        if questionnaire_data.like_to_eat is not None:
            db.set_temp_users_like_to_eat(questionnaire_data.user_id, questionnaire_data.like_to_eat)
        
        return {
            "message": "Анкета успешно сохранена",
            "user_id": questionnaire_data.user_id
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сохранения анкеты: {str(e)}")

