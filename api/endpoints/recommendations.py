from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
import sys
import os

# Добавляем путь к корневой директории проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from database.db import Database
import random

router = APIRouter()

# Инициализация базы данных
db = Database('/Users/temurkarimov/PycharmProjects/koreanchick/files/databse.db')

# Dependency для получения базы данных
def get_database():
    return db

def calculate_match_score(dish_name: str, category: str, ingredients: str, like_to_eat: str, dont_like_to_eat: str, mood: str, style: str) -> int:
    """
    Умный расчет процента совпадения на основе предпочтений пользователя
    """
    score = 50  # Базовый процент
    
    # Проверяем черный список
    blacklist = [ingredient.strip().lower() for ingredient in dont_like_to_eat.split(",") if ingredient.strip()]
    whitelist = [ingredient.strip().lower() for ingredient in like_to_eat.split(",") if ingredient.strip()]
    
    ingredients_lower = ingredients.lower()
    
    # Черный список уже проверен на уровне фильтрации блюд
    # Блюда с нежелательными ингредиентами не попадают в рекомендации
    
    # Бонусы за желательные ингредиенты
    for ingredient in whitelist:
        if ingredient in ingredients_lower:
            score += 15  # Бонус за желательные ингредиенты
    
    # Бонусы за соответствие настроению
    mood_bonuses = {
        'Радость': ['сладкий', 'десерт', 'шоколад', 'фрукт', 'яркий'],
        'Печаль': ['суп', 'теплый', 'комфорт', 'уютный'],
        'Гнев': ['острый', 'пряный', 'интенсивный', 'кислый'],
        'Спокойствие': ['легкий', 'свежий', 'салат', 'зеленый'],
        'Волнение': ['энергичный', 'белок', 'мясо', 'рыба']
    }
    
    if mood in mood_bonuses:
        for keyword in mood_bonuses[mood]:
            if keyword in ingredients_lower or keyword in dish_name.lower():
                score += 10
    
    # Бонусы за соответствие стилю питания
    style_bonuses = {
        'Обычный': ['мясо', 'рыба', 'курица', 'говядина'],
        'Вегетарианский': ['овощ', 'салат', 'зелень', 'фрукт'],
        'Веганский': ['растительный', 'овощ', 'фрукт', 'орех'],
        'Кето': ['жир', 'масло', 'сыр', 'авокадо'],
        'Здоровый': ['свежий', 'салат', 'овощ', 'фрукт']
    }
    
    if style in style_bonuses:
        for keyword in style_bonuses[style]:
            if keyword in ingredients_lower:
                score += 8
    
    # Бонусы за категорию блюда
    category_bonuses = {
        'Суп': 5,
        'Салат': 8,
        'Основное': 10,
        'Вок': 7,
        'Корейский стритфуд': 6,
        'Горячие закуски': 4,
        'Десерт': 3,
        'Напиток': 2
    }
    
    if category in category_bonuses:
        score += category_bonuses[category]
    
    # Ограничиваем диапазон 20-98%
    score = max(20, min(98, score))
    
    return score

def generate_smart_recommendations(user_id: int, mood: str, style: str, like_to_eat: str, dont_like_to_eat: str) -> list:
    """
    Умная функция генерации рекомендаций на основе логики из бота
    """
    try:
        print(f"Начинаем генерацию рекомендаций для user_id={user_id}, mood={mood}, style={style}")
        
        # Получаем все блюда из меню
        with db.connection:
            result = db.connection.execute("SELECT * FROM menu").fetchall()
        
        print(f"Получено {len(result)} блюд из базы данных")
        
        if not result:
            print("База данных пуста")
            return []
        
        # Умная логика - выбираем 5 блюд из разных категорий с учетом предпочтений
        recommendations = []
        categories_seen = set()
        
        # Получаем черный и белый списки
        blacklist = [ingredient.strip().lower() for ingredient in dont_like_to_eat.split(",") if ingredient.strip()]
        whitelist = [ingredient.strip().lower() for ingredient in like_to_eat.split(",") if ingredient.strip()]
        
        print(f"Черный список: {blacklist}")
        print(f"Белый список: {whitelist}")
        print(f"Всего блюд в базе: {len(result)}")
        
        # Добавляем отладочную информацию в ответ
        debug_info = {
            "blacklist": blacklist,
            "whitelist": whitelist,
            "total_dishes": len(result)
        }
        
        # Временно добавляем отладочную информацию в результат
        print(f"DEBUG: blacklist={blacklist}, whitelist={whitelist}, total_dishes={len(result)}")
        
        # Сначала пробуем найти блюда с предпочтительными ингредиентами
        for dish in result:
            if len(recommendations) >= 5:
                break
                
            category = dish[1] if len(dish) > 1 else "Основное"  # Категория
            name = dish[2] if len(dish) > 2 else "Блюдо"  # Название
            price = dish[8] if len(dish) > 8 and dish[8] else 500  # Цена
            ingredients = str(dish[4] or '').lower()  # Ингредиенты
            
            # Проверяем черный список - если есть нежелательный ингредиент, пропускаем блюдо
            # Проверяем только в столбце dish_ingredients (ingredients)
            has_blacklist = any(ingredient in ingredients for ingredient in blacklist)
            if has_blacklist:
                print(f"Пропускаем блюдо '{name}' из-за нежелательного ингредиента")
                print(f"  - Ингредиенты: {ingredients}")
                print(f"  - Черный список: {blacklist}")
                continue
                
            # Проверяем, что категория еще не использована
            if category not in categories_seen:
                categories_seen.add(category)
                
                # Иконки для категорий
                icons_map = {
                    'Суп': '🍲',
                    'Салат': '🥗', 
                    'Основное': '🍽️',
                    'Вок': '🍜',
                    'Корейский стритфуд': '🌶️',
                    'Горячие закуски': '🔥',
                    'Десерт': '🍰',
                    'Десерты': '🍰',
                    'Напиток': '🥤'
                }
                
                icon = icons_map.get(category, "🍽️")
                ingredients = str(dish[4] or '')  # Ингредиенты для расчета
                match_score = calculate_match_score(name, category, ingredients, like_to_eat, dont_like_to_eat, mood, style)
                recommendations.append((icon, name, price, match_score))
                print(f"Добавлено блюдо: {name} ({category}) - {match_score}%")
        
        # Если не набрали 5 блюд, добавляем любые подходящие
        if len(recommendations) < 5:
            for dish in result:
                if len(recommendations) >= 5:
                    break
                    
                category = dish[1] if len(dish) > 1 else "Основное"
                name = dish[2] if len(dish) > 2 else "Блюдо"
                price = dish[8] if len(dish) > 8 and dish[8] else 500
                ingredients = str(dish[4] or '').lower()
                
                # Проверяем черный список
                has_blacklist = any(ingredient in ingredients for ingredient in blacklist)
                if has_blacklist:
                    continue
                    
                # Проверяем, что категория еще не использована
                if category not in categories_seen:
                    categories_seen.add(category)
                    
                    icons_map = {
                        'Суп': '🍲',
                        'Салат': '🥗', 
                        'Основное': '🍽️',
                        'Вок': '🍜',
                        'Корейский стритфуд': '🌶️',
                        'Горячие закуски': '🔥',
                        'Десерт': '🍰',
                        'Десерты': '🍰',
                        'Напиток': '🥤'
                    }
                    
                    icon = icons_map.get(category, "🍽️")
                    ingredients = str(dish[4] or '')  # Ингредиенты для расчета
                    match_score = calculate_match_score(name, category, ingredients, like_to_eat, dont_like_to_eat, mood, style)
                    recommendations.append((icon, name, price, match_score))
                    print(f"Добавлено дополнительное блюдо: {name} ({category}) - {match_score}%")
        
        print(f"Сгенерировано {len(recommendations)} рекомендаций")
        
        # Добавляем отладочную информацию
        recommendations_with_debug = []
        for rec in recommendations:
            if len(rec) == 4:
                icon, name, price, match_score = rec
                recommendations_with_debug.append((icon, name, price, match_score, debug_info))
            else:
                recommendations_with_debug.append(rec)
        
        return recommendations_with_debug
        
    except Exception as e:
        print(f"Ошибка генерации рекомендаций: {e}")
        import traceback
        traceback.print_exc()
        return []

class QuestionnaireData(BaseModel):
    user_id: int
    mood: str
    style: str
    like_to_eat: str
    dont_like_to_eat: str
    category: Optional[str] = None

class RecommendationResponse(BaseModel):
    id: int
    name: str
    category: str
    price: int
    icon: str
    description: Optional[str] = None
    match_score: Optional[int] = None
    reasons: Optional[List[str]] = None

@router.post("/recommendations", response_model=List[RecommendationResponse])
async def get_recommendations(
    questionnaire_data: QuestionnaireData,
    db: Database = Depends(get_database)
):
    """
    Получить персональные рекомендации блюд на основе анкеты пользователя
    """
    try:
        # Пока что просто пропускаем сохранение данных анкеты
        # В будущем можно добавить эти методы в Database класс
        
        # Получаем рекомендации используя умную логику
        recommendations = generate_smart_recommendations(
            questionnaire_data.user_id,
            questionnaire_data.mood,
            questionnaire_data.style,
            questionnaire_data.like_to_eat,
            questionnaire_data.dont_like_to_eat
        )
        
        if not recommendations:
            raise HTTPException(status_code=404, detail="Рекомендации не найдены")
        
        # Преобразуем в формат API
        result = []
        for i, rec in enumerate(recommendations[:5]):  # Берем до 5 блюд
            if len(rec) == 5:  # Новый формат с процентами и отладкой
                icon, name, price, match_score, debug_info = rec
            elif len(rec) == 4:  # Формат с процентами без отладки
                icon, name, price, match_score = rec
            else:  # Старый формат без процентов
                icon, name, price = rec
                match_score = 95 - (i * 5)  # Fallback к старой логике
            
            # Получаем дополнительную информацию о блюде
            dish_info = db.restaurants_get_by_name(name)
            if dish_info:
                dish_id = dish_info[0]
                category = dish_info[1]
                description = dish_info[3] if len(dish_info) > 3 else None
                
                # Генерируем объяснения на основе настроения
                reasons = generate_reasons(questionnaire_data.mood, name, category)
                
                result.append(RecommendationResponse(
                    id=dish_id,
                    name=name,
                    category=category,
                    price=price,
                    icon=icon,
                    description=description,
                    match_score=match_score,  # Используем рассчитанный процент
                    reasons=reasons
                ))
        
        return result
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Ошибка получения рекомендаций: {error_details}")
        raise HTTPException(status_code=500, detail=f"Ошибка получения рекомендаций: {str(e)}")

def generate_reasons(mood: str, dish_name: str, category: str) -> List[str]:
    """
    Генерирует объяснения, почему блюдо подходит пользователю
    """
    reasons = []
    
    # Базовые объяснения по настроению
    mood_reasons = {
        'Радость': [
            "Отлично подходит для праздничного настроения",
            "Яркие вкусы поднимут настроение еще выше"
        ],
        'Печаль': [
            "Комфортная еда поможет справиться с грустью",
            "Теплые вкусы создадут ощущение уюта"
        ],
        'Гнев': [
            "Острота поможет выпустить негативные эмоции",
            "Интенсивные вкусы отвлекут от проблем"
        ],
        'Спокойствие': [
            "Легкое блюдо не нарушит внутренний покой",
            "Сбалансированные вкусы поддержат гармонию"
        ],
        'Волнение': [
            "Сытное блюдо успокоит нервную систему",
            "Питательные вещества помогут сосредоточиться"
        ]
    }
    
    # Добавляем объяснения по настроению
    if mood in mood_reasons:
        reasons.extend(mood_reasons[mood])
    
    # Добавляем объяснения по категории
    category_reasons = {
        'Суп': "Теплый суп согреет и успокоит",
        'Салат': "Свежие овощи дадут энергию",
        'Основное': "Сытное блюдо насытит надолго",
        'Вок': "Горячее блюдо согреет и поднимет настроение",
        'Корейский стритфуд': "Острые вкусы взбодрят"
    }
    
    if category in category_reasons:
        reasons.append(category_reasons[category])
    
    # Добавляем общие объяснения
    reasons.append(f"Блюдо '{dish_name}' идеально подходит под твое текущее настроение")
    
    return reasons[:3]  # Возвращаем максимум 3 объяснения

@router.get("/recommendations/{user_id}", response_model=List[RecommendationResponse])
async def get_user_recommendations(
    user_id: int,
    db: Database = Depends(get_database)
):
    """
    Получить сохраненные рекомендации пользователя
    """
    try:
        # Получаем сохраненные рекомендации пользователя (с дефолтными параметрами)
        recommendations = generate_smart_recommendations(
            user_id,
            "Радость",  # Дефолтное настроение
            "Обычный",  # Дефолтный стиль
            "мясо, рыба",  # Дефолтные предпочтения
            "грибы"  # Дефолтные ограничения
        )
        
        if not recommendations:
            raise HTTPException(status_code=404, detail="Рекомендации не найдены")
        
        result = []
        for i, rec in enumerate(recommendations[:5]):
            if len(rec) == 4:  # Новый формат с процентами
                icon, name, price, match_score = rec
            else:  # Старый формат без процентов
                icon, name, price = rec
                match_score = 95 - (i * 5)  # Fallback к старой логике
            
            # Получаем информацию о блюде
            dish_info = db.restaurants_get_by_name(name)
            if dish_info:
                dish_id = dish_info[0]
                category = dish_info[1]
                description = dish_info[3] if len(dish_info) > 3 else None
                
                # Генерируем объяснения с дефолтным настроением
                reasons = generate_reasons("Радость", name, category)
                
                result.append(RecommendationResponse(
                    id=dish_id,
                    name=name,
                    category=category,
                    price=price,
                    icon=icon,
                    description=description,
                    match_score=match_score,  # Используем рассчитанный процент
                    reasons=reasons
                ))
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения рекомендаций: {str(e)}")
