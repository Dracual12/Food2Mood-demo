"""
Эндпоинты для работы с официантами
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from api.models import WaiterResponse, WaiterCreate, WaiterUpdate, WaiterStats
from api.auth import create_access_token
from database.db import Database

router = APIRouter()

def get_database():
    from api.main import db
    return db

@router.post("/register", response_model=dict)
async def register_waiter(
    waiter_data: WaiterCreate,
    db: Database = Depends(get_database)
):
    """Регистрация нового официанта"""
    try:
        # Проверяем, существует ли официант
        if db.check_waiter_exists(waiter_data.waiter_id):
            raise HTTPException(status_code=400, detail="Официант уже зарегистрирован")
        
        # Создаем официанта
        db.add_waiter(
            user_id=waiter_data.waiter_id,
            user_link=waiter_data.waiter_link,
            user_name=waiter_data.waiter_name,
            user_last_name=waiter_data.waiter_last_name,
            user_first_name=waiter_data.waiter_first_name,
            user_surname=waiter_data.waiter_surname,
            score=waiter_data.waiter_score
        )
        
        # Создаем токен для официанта
        token = create_access_token(waiter_data.waiter_id, "waiter")
        
        return {
            "message": "Официант успешно зарегистрирован",
            "waiter_id": waiter_data.waiter_id,
            "token": token
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка регистрации: {str(e)}")

@router.post("/login", response_model=dict)
async def login_waiter(
    waiter_id: int,
    db: Database = Depends(get_database)
):
    """Вход официанта в систему"""
    try:
        # Проверяем, существует ли официант
        if not db.check_waiter_exists(waiter_id):
            raise HTTPException(status_code=404, detail="Официант не найден")
        
        # Создаем токен
        token = create_access_token(waiter_id, "waiter")
        
        return {
            "message": "Успешный вход в систему",
            "waiter_id": waiter_id,
            "token": token
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка входа: {str(e)}")

@router.get("/", response_model=List[WaiterResponse])
async def get_all_waiters(
    skip: int = Query(0, description="Количество пропущенных записей"),
    limit: int = Query(100, description="Максимальное количество записей"),
    db: Database = Depends(get_database)
):
    """Получить список всех официантов"""
    try:
        waiters = db.connection.execute(
            "SELECT * FROM waiters ORDER BY waiter_id LIMIT ? OFFSET ?",
            (limit, skip)
        ).fetchall()
        
        result = []
        for waiter in waiters:
            result.append(WaiterResponse(
                waiter_id=waiter[0],  # waiter_id
                waiter_name=waiter[2],  # waiter_name
                waiter_first_name=waiter[4],  # waiter_first_name
                waiter_last_name=waiter[3],  # waiter_last_name
                waiter_surname=waiter[5],  # waiter_surname
                waiter_link=waiter[1],  # waiter_link
                waiter_rest="Food2Mood",  # Фиксированное значение
                waiter_score=waiter[6],  # waiter_score
                waiter_current_earnings=waiter[8],  # waiter_current_earnings
                waiter_remark=waiter[7] if len(waiter) > 7 else ""  # waiter_remark
            ))
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения официантов: {str(e)}")

@router.get("/{waiter_id}", response_model=WaiterResponse)
async def get_waiter_by_id(
    waiter_id: int,
    db: Database = Depends(get_database)
):
    """Получить официанта по ID"""
    try:
        waiter = db.connection.execute(
            "SELECT * FROM waiters WHERE waiter_id = ?", (waiter_id,)
        ).fetchone()
        
        if not waiter:
            raise HTTPException(status_code=404, detail="Официант не найден")
        
        return WaiterResponse(
            waiter_id=waiter[1],
            waiter_name=waiter[3],
            waiter_first_name=waiter[5],
            waiter_last_name=waiter[4],
            waiter_surname=waiter[6],
            waiter_link=waiter[2],
            waiter_rest=waiter[8] if len(waiter) > 8 else None,
            waiter_score=waiter[7],
            waiter_current_earnings=waiter[9] if len(waiter) > 9 else 0,
            waiter_remark=waiter[10] if len(waiter) > 10 else ""
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения официанта: {str(e)}")

@router.put("/{waiter_id}", response_model=dict)
async def update_waiter(
    waiter_id: int,
    waiter_update: WaiterUpdate,
    db: Database = Depends(get_database)
):
    """Обновить информацию об официанте"""
    try:
        # Проверяем, существует ли официант
        if not db.check_waiter_exists(waiter_id):
            raise HTTPException(status_code=404, detail="Официант не найден")
        
        # Обновляем информацию
        if waiter_update.waiter_name is not None:
            db.connection.execute(
                "UPDATE waiters SET waiter_name = ? WHERE waiter_id = ?",
                (waiter_update.waiter_name, waiter_id)
            )
        
        if waiter_update.waiter_first_name is not None:
            db.connection.execute(
                "UPDATE waiters SET waiter_first_name = ? WHERE waiter_id = ?",
                (waiter_update.waiter_first_name, waiter_id)
            )
        
        if waiter_update.waiter_last_name is not None:
            db.connection.execute(
                "UPDATE waiters SET waiter_last_name = ? WHERE waiter_id = ?",
                (waiter_update.waiter_last_name, waiter_id)
            )
        
        if waiter_update.waiter_surname is not None:
            db.connection.execute(
                "UPDATE waiters SET waiter_surname = ? WHERE waiter_id = ?",
                (waiter_update.waiter_surname, waiter_id)
            )
        
        if waiter_update.waiter_rest is not None:
            db.connection.execute(
                "UPDATE waiters SET waiter_rest = ? WHERE waiter_id = ?",
                (waiter_update.waiter_rest, waiter_id)
            )
        
        if waiter_update.waiter_score is not None:
            db.set_waiter_score(waiter_id, waiter_update.waiter_score)
        
        if waiter_update.waiter_current_earnings is not None:
            db.set_current_earnings(waiter_update.waiter_current_earnings, waiter_id)
        
        if waiter_update.waiter_remark is not None:
            db.set_remark(waiter_id, waiter_update.waiter_remark)
        
        db.connection.commit()
        
        return {"message": "Информация об официанте обновлена"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обновления: {str(e)}")

@router.delete("/{waiter_id}")
async def delete_waiter(
    waiter_id: int,
    db: Database = Depends(get_database)
):
    """Удалить официанта"""
    try:
        # Проверяем, существует ли официант
        if not db.check_waiter_exists(waiter_id):
            raise HTTPException(status_code=404, detail="Официант не найден")
        
        # Удаляем официанта
        db.del_waiter(waiter_id)
        
        return {"message": f"Официант {waiter_id} удален"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка удаления: {str(e)}")

@router.get("/stats/overview", response_model=WaiterStats)
async def get_waiter_stats(db: Database = Depends(get_database)):
    """Получить статистику официантов"""
    try:
        # Общее количество официантов
        total_waiters = db.connection.execute("SELECT COUNT(*) FROM waiters").fetchone()[0]
        
        # Количество активных официантов (с текущими заработками > 0)
        active_waiters = db.connection.execute(
            "SELECT COUNT(*) FROM waiters WHERE waiter_current_earnings > 0"
        ).fetchone()[0]
        
        # Общие заработки
        total_earnings = db.connection.execute(
            "SELECT SUM(waiter_current_earnings) FROM waiters"
        ).fetchone()[0] or 0
        
        return WaiterStats(
            total_waiters=total_waiters,
            active_waiters=active_waiters,
            total_earnings=total_earnings
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения статистики: {str(e)}")

@router.get("/{waiter_id}/stats", response_model=dict)
async def get_waiter_personal_stats(
    waiter_id: int,
    db: Database = Depends(get_database)
):
    """Получить персональную статистику официанта"""
    try:
        # Проверяем, существует ли официант
        if not db.check_waiter_exists(waiter_id):
            raise HTTPException(status_code=404, detail="Официант не найден")
        
        # Получаем статистику
        current_guests = db.get_current_waiter_guests(waiter_id)
        current_sales = db.get_current_waiter_sells(waiter_id)
        current_earnings = db.get_current_earnings(waiter_id)
        
        return {
            "waiter_id": waiter_id,
            "current_guests": current_guests,
            "current_sales": current_sales,
            "current_earnings": current_earnings
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения статистики: {str(e)}")

@router.post("/{waiter_id}/earnings")
async def update_waiter_earnings(
    waiter_id: int,
    amount: int,
    db: Database = Depends(get_database)
):
    """Обновить заработки официанта"""
    try:
        # Проверяем, существует ли официант
        if not db.check_waiter_exists(waiter_id):
            raise HTTPException(status_code=404, detail="Официант не найден")
        
        # Обновляем заработки
        db.set_current_earnings(amount, waiter_id)
        
        return {"message": f"Заработки официанта {waiter_id} обновлены на {amount}"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обновления заработков: {str(e)}")

@router.post("/{waiter_id}/score")
async def update_waiter_score(
    waiter_id: int,
    score: str,
    db: Database = Depends(get_database)
):
    """Обновить рейтинг официанта"""
    try:
        # Проверяем, существует ли официант
        if not db.check_waiter_exists(waiter_id):
            raise HTTPException(status_code=404, detail="Официант не найден")
        
        # Обновляем рейтинг
        db.set_waiter_score(waiter_id, score)
        
        return {"message": f"Рейтинг официанта {waiter_id} обновлен"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обновления рейтинга: {str(e)}")

@router.post("/{waiter_id}/remark")
async def update_waiter_remark(
    waiter_id: int,
    remark: str,
    db: Database = Depends(get_database)
):
    """Обновить заметку об официанте"""
    try:
        # Проверяем, существует ли официант
        if not db.check_waiter_exists(waiter_id):
            raise HTTPException(status_code=404, detail="Официант не найден")
        
        # Обновляем заметку
        db.set_remark(waiter_id, remark)
        
        return {"message": f"Заметка об официанте {waiter_id} обновлена"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обновления заметки: {str(e)}")

@router.delete("/{waiter_id}/remark")
async def clear_waiter_remark(
    waiter_id: int,
    db: Database = Depends(get_database)
):
    """Очистить заметку об официанте"""
    try:
        # Проверяем, существует ли официант
        if not db.check_waiter_exists(waiter_id):
            raise HTTPException(status_code=404, detail="Официант не найден")
        
        # Очищаем заметку
        db.clear_remark(waiter_id)
        
        return {"message": f"Заметка об официанте {waiter_id} очищена"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка очистки заметки: {str(e)}")
