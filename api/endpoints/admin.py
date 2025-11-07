"""
Эндпоинты для администраторов
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional, Dict, Any
from api.models import AdminResponse, AdminCreate, LoggingResponse, StopListResponse, StopListItem
from api.auth import create_access_token
from database.db import Database
import json

router = APIRouter()

def get_database():
    from api.main import db
    return db

@router.post("/register", response_model=dict)
async def register_admin(
    admin_data: AdminCreate,
    db: Database = Depends(get_database)
):
    """Регистрация нового администратора"""
    try:
        # Проверяем, существует ли администратор
        if db.check_admin_exists(admin_data.admin_id):
            raise HTTPException(status_code=400, detail="Администратор уже зарегистрирован")
        
        # Создаем администратора
        db.add_admin(
            user_id=admin_data.admin_id,
            user_rest=admin_data.temp_rest
        )
        
        # Создаем токен для администратора
        token = create_access_token(admin_data.admin_id, "admin")
        
        return {
            "message": "Администратор успешно зарегистрирован",
            "admin_id": admin_data.admin_id,
            "token": token
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка регистрации: {str(e)}")

@router.post("/login", response_model=dict)
async def login_admin(
    admin_id: int,
    db: Database = Depends(get_database)
):
    """Вход администратора в систему"""
    try:
        # Проверяем, существует ли администратор
        if not db.check_admin_exists(admin_id):
            raise HTTPException(status_code=404, detail="Администратор не найден")
        
        # Создаем токен
        token = create_access_token(admin_id, "admin")
        
        return {
            "message": "Успешный вход в систему",
            "admin_id": admin_id,
            "token": token
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка входа: {str(e)}")

@router.get("/", response_model=List[AdminResponse])
async def get_all_admins(
    skip: int = Query(0, description="Количество пропущенных записей"),
    limit: int = Query(100, description="Максимальное количество записей"),
    db: Database = Depends(get_database)
):
    """Получить список всех администраторов"""
    try:
        admins = db.connection.execute(
            "SELECT * FROM admins ORDER BY admin_id LIMIT ? OFFSET ?",
            (limit, skip)
        ).fetchall()
        
        result = []
        for admin in admins:
            result.append(AdminResponse(
                admin_id=admin[1],
                temp_rest=admin[2]
            ))
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения администраторов: {str(e)}")

@router.get("/{admin_id}", response_model=AdminResponse)
async def get_admin_by_id(
    admin_id: int,
    db: Database = Depends(get_database)
):
    """Получить администратора по ID"""
    try:
        admin = db.connection.execute(
            "SELECT * FROM admins WHERE admin_id = ?", (admin_id,)
        ).fetchone()
        
        if not admin:
            raise HTTPException(status_code=404, detail="Администратор не найден")
        
        return AdminResponse(
            admin_id=admin[1],
            temp_rest=admin[2]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения администратора: {str(e)}")

@router.put("/{admin_id}/restaurant")
async def update_admin_restaurant(
    admin_id: int,
    restaurant: str,
    db: Database = Depends(get_database)
):
    """Обновить ресторан администратора"""
    try:
        # Проверяем, существует ли администратор
        if not db.check_admin_exists(admin_id):
            raise HTTPException(status_code=404, detail="Администратор не найден")
        
        # Обновляем ресторан
        db.set_admin_rest(admin_id, restaurant)
        
        return {"message": f"Ресторан администратора {admin_id} обновлен на {restaurant}"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обновления ресторана: {str(e)}")

@router.delete("/{admin_id}")
async def delete_admin(
    admin_id: int,
    db: Database = Depends(get_database)
):
    """Удалить администратора"""
    try:
        # Проверяем, существует ли администратор
        if not db.check_admin_exists(admin_id):
            raise HTTPException(status_code=404, detail="Администратор не найден")
        
        # Удаляем администратора
        db.del_admin(admin_id)
        
        return {"message": f"Администратор {admin_id} удален"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка удаления: {str(e)}")

@router.get("/logs/", response_model=List[LoggingResponse])
async def get_logs(
    user_id: Optional[str] = Query(None, description="Фильтр по пользователю"),
    date: Optional[str] = Query(None, description="Фильтр по дате"),
    skip: int = Query(0, description="Количество пропущенных записей"),
    limit: int = Query(100, description="Максимальное количество записей"),
    db: Database = Depends(get_database)
):
    """Получить логи системы"""
    try:
        if user_id:
            logs = db.get_logging_by_user_id(user_id)
        elif date:
            logs = db.get_logging_by_date(date)
        else:
            logs = db.get_logging_all()
        
        # Применяем пагинацию
        logs = logs[skip:skip + limit]
        
        result = []
        for log in logs:
            result.append(LoggingResponse(
                id=log[0],
                user_id=log[1],
                date=log[2],
                fio=log[3],
                phone=log[4],
                mood=log[5],
                hungry=log[6],
                style=log[7],
                sex=log[8],
                age=log[9],
                dish_style=log[10],
                ccal=log[11],
                dislike=log[12],
                like=log[13],
                order=log[14],
                sum=log[15]
            ))
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения логов: {str(e)}")

@router.get("/logs/{log_id}", response_model=LoggingResponse)
async def get_log_by_id(
    log_id: int,
    db: Database = Depends(get_database)
):
    """Получить лог по ID"""
    try:
        log = db.get_logging_by_id(log_id)
        
        if not log:
            raise HTTPException(status_code=404, detail="Лог не найден")
        
        return LoggingResponse(
            id=log[0],
            user_id=log[1],
            date=log[2],
            fio=log[3],
            phone=log[4],
            mood=log[5],
            hungry=log[6],
            style=log[7],
            sex=log[8],
            age=log[9],
            dish_style=log[10],
            ccal=log[11],
            dislike=log[12],
            like=log[13],
            order=log[14],
            sum=log[15]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения лога: {str(e)}")

@router.put("/logs/{log_id}/fio")
async def update_log_fio(
    log_id: int,
    fio: str,
    db: Database = Depends(get_database)
):
    """Обновить ФИО в логе"""
    try:
        db.update_logging_fio(log_id, fio)
        return {"message": "ФИО обновлено"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обновления ФИО: {str(e)}")

@router.put("/logs/{log_id}/phone")
async def update_log_phone(
    log_id: int,
    phone: str,
    db: Database = Depends(get_database)
):
    """Обновить телефон в логе"""
    try:
        db.update_logging_phone(log_id, phone)
        return {"message": "Телефон обновлен"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обновления телефона: {str(e)}")

@router.delete("/logs/{log_id}")
async def delete_log(
    log_id: int,
    db: Database = Depends(get_database)
):
    """Удалить лог"""
    try:
        db.delete_logging_entry(log_id)
        return {"message": f"Лог {log_id} удален"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка удаления лога: {str(e)}")

@router.get("/stop-lists/", response_model=List[StopListResponse])
async def get_stop_lists(
    restaurant: Optional[str] = Query(None, description="Фильтр по ресторану"),
    db: Database = Depends(get_database)
):
    """Получить стоп-листы"""
    try:
        if restaurant:
            stop_list_data = db.get_stop_list(restaurant)
            return [StopListResponse(
                restaurant=restaurant,
                items=json.loads(stop_list_data) if stop_list_data else [],
                updated_at="2024-01-01 00:00:00"  # В реальной реализации нужно получать время обновления
            )]
        else:
            # Получаем все стоп-листы
            stop_lists = db.connection.execute("SELECT * FROM stop_lists").fetchall()
            result = []
            for stop_list in stop_lists:
                result.append(StopListResponse(
                    restaurant=stop_list[1],
                    items=json.loads(stop_list[2]) if stop_list[2] else [],
                    updated_at="2024-01-01 00:00:00"
                ))
            return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения стоп-листов: {str(e)}")

@router.put("/stop-lists/{restaurant}")
async def update_stop_list(
    restaurant: str,
    items: List[StopListItem],
    db: Database = Depends(get_database)
):
    """Обновить стоп-лист ресторана"""
    try:
        # Преобразуем в JSON
        stop_list_json = json.dumps([item.dict() for item in items])
        
        # Обновляем стоп-лист
        if db.check_stop_list_exists():
            db.set_stop_list(stop_list_json)
        else:
            db.create_stop_list(restaurant, stop_list_json)
        
        return {"message": f"Стоп-лист ресторана {restaurant} обновлен"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обновления стоп-листа: {str(e)}")

@router.delete("/stop-lists/{restaurant}")
async def delete_stop_list(
    restaurant: str,
    db: Database = Depends(get_database)
):
    """Удалить стоп-лист ресторана"""
    try:
        db.del_stop_list(restaurant)
        return {"message": f"Стоп-лист ресторана {restaurant} удален"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка удаления стоп-листа: {str(e)}")

@router.get("/stats/overview", response_model=Dict[str, Any])
async def get_admin_stats(db: Database = Depends(get_database)):
    """Получить общую статистику системы"""
    try:
        # Статистика пользователей
        total_users = db.connection.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        active_users = db.connection.execute("SELECT COUNT(*) FROM users WHERE ban = 0").fetchone()[0]
        
        # Статистика заказов
        total_orders = db.connection.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
        total_revenue = db.connection.execute("SELECT SUM(order_amount) FROM orders").fetchone()[0] or 0
        
        # Статистика официантов
        total_waiters = db.connection.execute("SELECT COUNT(*) FROM waiters").fetchone()[0]
        
        # Статистика логов
        total_logs = db.get_logging_count()
        
        return {
            "users": {
                "total": total_users,
                "active": active_users,
                "banned": total_users - active_users
            },
            "orders": {
                "total": total_orders,
                "revenue": total_revenue,
                "average_order_value": total_revenue / total_orders if total_orders > 0 else 0
            },
            "waiters": {
                "total": total_waiters
            },
            "logs": {
                "total": total_logs
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения статистики: {str(e)}")

@router.get("/reports/export")
async def export_data(
    table: str = Query(..., description="Таблица для экспорта"),
    format: str = Query("json", description="Формат экспорта (json, csv)"),
    db: Database = Depends(get_database)
):
    """Экспорт данных из системы"""
    try:
        # Получаем данные из указанной таблицы
        data = db.connection.execute(f"SELECT * FROM {table}").fetchall()
        
        if format == "json":
            # Преобразуем в JSON
            result = []
            for row in data:
                result.append(dict(row))
            return {"data": result, "table": table, "format": format}
        elif format == "csv":
            # В реальной реализации нужно создать CSV файл
            return {"message": "CSV экспорт будет реализован", "table": table, "format": format}
        else:
            raise HTTPException(status_code=400, detail="Неподдерживаемый формат")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка экспорта: {str(e)}")
