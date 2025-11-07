"""
Эндпоинты для работы с заказами
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from api.models import OrderResponse, OrderCreate, OrderUpdate, OrderStats, BasketResponse, BasketItem
from database.db import Database
import json

router = APIRouter()

def get_database():
    from api.main import db
    return db

@router.post("/", response_model=dict)
async def create_order(
    order_data: OrderCreate,
    db: Database = Depends(get_database)
):
    """Создать новый заказ"""
    try:
        # Проверяем, существует ли пользователь
        if not db.check_users_user_exists(order_data.user_id):
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        # Создаем заказ
        db.add_order(
            user_id=order_data.user_id,
            table_number=order_data.table_number,
            time=order_data.time,
            amount=order_data.order_amount
        )
        
        # Добавляем заказ в историю (используем только user_id и basket)
        db.connection.execute(
            "INSERT INTO orders_history (user_id, basket) VALUES (?, ?)",
            (order_data.user_id, json.dumps(order_data.basket))
        )
        db.connection.commit()
        
        return {
            "message": "Заказ успешно создан",
            "user_id": order_data.user_id,
            "amount": order_data.order_amount
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка создания заказа: {str(e)}")

@router.get("/", response_model=List[OrderResponse])
async def get_orders(
    user_id: Optional[int] = Query(None, description="Фильтр по пользователю"),
    skip: int = Query(0, description="Количество пропущенных записей"),
    limit: int = Query(100, description="Максимальное количество записей"),
    db: Database = Depends(get_database)
):
    """Получить список заказов"""
    try:
        if user_id:
            # Получаем заказы конкретного пользователя
            orders = db.connection.execute(
                "SELECT * FROM orders WHERE waiter_id = ? ORDER BY time DESC LIMIT ? OFFSET ?",
                (user_id, limit, skip)
            ).fetchall()
        else:
            # Получаем все заказы
            orders = db.connection.execute(
                "SELECT * FROM orders ORDER BY time DESC LIMIT ? OFFSET ?",
                (limit, skip)
            ).fetchall()
        
        result = []
        for i, order in enumerate(orders):
            result.append(OrderResponse(
                id=i + 1,  # Генерируем ID
                user_id=order[0],  # waiter_id
                table_number=order[1],
                time=order[2],
                order_amount=order[3],
                basket={}  # В реальной реализации нужно получать корзину
            ))
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения заказов: {str(e)}")

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order_by_id(
    order_id: int,
    db: Database = Depends(get_database)
):
    """Получить заказ по ID"""
    try:
        order = db.connection.execute(
            "SELECT * FROM orders WHERE id = ?", (order_id,)
        ).fetchone()
        
        if not order:
            raise HTTPException(status_code=404, detail="Заказ не найден")
        
        return OrderResponse(
            id=order[0],
            user_id=order[1],
            table_number=order[2],
            time=order[3],
            order_amount=order[4],
            basket={}  # В реальной реализации нужно получать корзину
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения заказа: {str(e)}")

@router.put("/{order_id}", response_model=dict)
async def update_order(
    order_id: int,
    order_update: OrderUpdate,
    db: Database = Depends(get_database)
):
    """Обновить заказ"""
    try:
        # Проверяем, существует ли заказ
        order = db.connection.execute(
            "SELECT * FROM orders WHERE id = ?", (order_id,)
        ).fetchone()
        
        if not order:
            raise HTTPException(status_code=404, detail="Заказ не найден")
        
        # Обновляем заказ
        if order_update.table_number is not None:
            db.connection.execute(
                "UPDATE orders SET table_number = ? WHERE id = ?",
                (order_update.table_number, order_id)
            )
        
        if order_update.order_amount is not None:
            db.connection.execute(
                "UPDATE orders SET order_amount = ? WHERE id = ?",
                (order_update.order_amount, order_id)
            )
        
        db.connection.commit()
        
        return {"message": "Заказ обновлен"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обновления заказа: {str(e)}")

@router.delete("/{order_id}")
async def delete_order(
    order_id: int,
    db: Database = Depends(get_database)
):
    """Удалить заказ"""
    try:
        # Проверяем, существует ли заказ
        order = db.connection.execute(
            "SELECT * FROM orders WHERE id = ?", (order_id,)
        ).fetchone()
        
        if not order:
            raise HTTPException(status_code=404, detail="Заказ не найден")
        
        # Удаляем заказ
        db.connection.execute(
            "DELETE FROM orders WHERE id = ?", (order_id,)
        )
        db.connection.commit()
        
        return {"message": f"Заказ {order_id} удален"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка удаления заказа: {str(e)}")

@router.get("/stats/overview", response_model=OrderStats)
async def get_order_stats(db: Database = Depends(get_database)):
    """Получить статистику заказов"""
    try:
        # Общее количество заказов
        total_orders = db.connection.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
        
        # Общая выручка
        total_revenue = db.connection.execute("SELECT SUM(order_amount) FROM orders").fetchone()[0] or 0
        
        # Средний чек
        average_order_value = total_revenue / total_orders if total_orders > 0 else 0
        
        return OrderStats(
            total_orders=total_orders,
            total_revenue=total_revenue,
            average_order_value=average_order_value
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения статистики: {str(e)}")

@router.get("/user/{user_id}/basket", response_model=BasketResponse)
async def get_user_basket(
    user_id: int,
    db: Database = Depends(get_database)
):
    """Получить корзину пользователя"""
    try:
        # Проверяем, существует ли пользователь
        if not db.check_users_user_exists(user_id):
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        # Получаем корзину
        if db.check_basket_exists(user_id):
            basket = db.get_basket(user_id)
            qr_scanned = db.get_qr_scanned(user_id)
            qr_id = db.get_qr_id(user_id)
        else:
            basket = {}
            qr_scanned = False
            qr_id = None
        
        return BasketResponse(
            user_id=user_id,
            basket=basket,
            qr_scanned=qr_scanned,
            qr_id=qr_id
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения корзины: {str(e)}")

@router.put("/user/{user_id}/basket")
async def update_user_basket(
    user_id: int,
    basket: dict,
    db: Database = Depends(get_database)
):
    """Обновить корзину пользователя"""
    try:
        # Проверяем, существует ли пользователь
        if not db.check_users_user_exists(user_id):
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        # Создаем или обновляем корзину
        if db.check_basket_exists(user_id):
            db.set_basket(user_id, basket)
        else:
            db.create_basket(user_id, basket)
        
        return {"message": "Корзина обновлена"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обновления корзины: {str(e)}")

@router.delete("/user/{user_id}/basket")
async def clear_user_basket(
    user_id: int,
    db: Database = Depends(get_database)
):
    """Очистить корзину пользователя"""
    try:
        # Проверяем, существует ли пользователь
        if not db.check_users_user_exists(user_id):
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        # Очищаем корзину
        if db.check_basket_exists(user_id):
            db.set_basket(user_id, {})
        
        return {"message": "Корзина очищена"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка очистки корзины: {str(e)}")

@router.get("/user/{user_id}/history", response_model=List[dict])
async def get_user_order_history(
    user_id: int,
    skip: int = Query(0, description="Количество пропущенных записей"),
    limit: int = Query(100, description="Максимальное количество записей"),
    db: Database = Depends(get_database)
):
    """Получить историю заказов пользователя"""
    try:
        # Проверяем, существует ли пользователь
        if not db.check_users_user_exists(user_id):
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        # Получаем историю заказов
        history = db.connection.execute(
            "SELECT * FROM orders_history WHERE user_id = ? ORDER BY id DESC LIMIT ? OFFSET ?",
            (user_id, limit, skip)
        ).fetchall()
        
        result = []
        for record in history:
            result.append({
                "id": record[0],
                "user_id": record[1],
                "restaurant": record[2],
                "basket": json.loads(record[3]) if record[3] else {}
            })
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения истории: {str(e)}")
