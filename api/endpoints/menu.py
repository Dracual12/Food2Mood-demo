"""
Эндпоинты для работы с меню
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from api.models import MenuItemResponse
from database.db import Database

router = APIRouter()

def get_database():
    from api.main import db
    if db is None:
        raise HTTPException(status_code=503, detail="База данных не инициализирована")
    return db

@router.get("/", response_model=List[MenuItemResponse])
async def get_all_menu_items(
    category: Optional[str] = Query(None, description="Фильтр по категории"),
    restaurant: Optional[str] = Query(None, description="Фильтр по ресторану"),
    min_price: Optional[int] = Query(None, description="Минимальная цена"),
    max_price: Optional[int] = Query(None, description="Максимальная цена"),
    db: Database = Depends(get_database)
):
    """Получить отсортированный список позиций меню с возможностью фильтрации"""
    try:
        all_items = db.menu_get()
        
        # Применяем фильтры
        filtered_items = []
        for item in all_items:
            # Структура таблицы menu: id, Категория, Название блюда, Комментарий, Ингредиенты, 
            # Простые ингредиенты, КБЖУ, Граммы, Цена, Размер, iiko_id, Стиль питания, Настроение,
            # Рекомендации нутрициолога, Ссылка, Дополнительные продажи, Рейтинг, Отзывы, Коины
            dish_category = item[1] if len(item) > 1 else None  # Категория
            dish_name = item[2] if len(item) > 2 else None  # Название блюда
            dish_price = item[8] if len(item) > 8 and item[8] else 0  # Цена
            
            # Фильтр по категории
            if category and dish_category != category:
                continue
            
            # Фильтр по ресторану (в таблице menu нет rest_name, пропускаем)
            # if restaurant and item[1] != restaurant:
            #     continue
            
            # Фильтр по цене
            if min_price and dish_price < min_price:
                continue
            if max_price and dish_price > max_price:
                continue
            
            filtered_items.append(item)
        
        # Сортируем по категории и названию
        filtered_items.sort(key=lambda x: (x[1] or "", x[2] or ""))  # Сортировка по категории и названию
        
        # Преобразуем в формат ответа
        result = []
        for item in filtered_items:
            result.append(MenuItemResponse(
                id=item[0],
                dish_name=item[2] if len(item) > 2 else "Блюдо",  # Название блюда
                dish_category=item[1] if len(item) > 1 else "Основное",  # Категория блюда
                dish_price=item[8] if len(item) > 8 and item[8] else 0,  # Цена из БД
                dish_g=item[7] if len(item) > 7 else None,  # Граммы
                size=item[9] if len(item) > 9 and item[9] else None,  # Размер
                simple_ingridients=item[5] if len(item) > 5 else None,  # Простые ингредиенты
                additional_dishes=item[15] if len(item) > 15 else None,  # Дополнительные продажи
                iiko_id=item[10] if len(item) > 10 else None,  # iiko_id
                dish_rec_nutritionist=item[13] if len(item) > 13 else None,  # Рекомендации нутрициолога
                dish_rec_community=None,  # Нет в таблице menu
                dish_rec_a_oblomov=None,  # Нет в таблице menu
                dish_rec_a_ivlev=None,  # Нет в таблице menu
                stat_reviews=item[17] if len(item) > 17 else None,  # Отзывы
                stat_rating=item[16] if len(item) > 16 else None  # Рейтинг
            ))
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения меню: {str(e)}")

