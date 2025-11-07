"""
Food2Mood API
Основной файл API для ресторанного бота
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import Database
from api.models import *
from api.endpoints import menu, users, questionnaire

# Инициализация базы данных
db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'files', 'databse.db')
try:
    db = Database(db_path)
except Exception as e:
    print(f"⚠️ Предупреждение при инициализации БД: {e}")
    db = None

# Создание FastAPI приложения
app = FastAPI(
    title="Food2Mood API",
    description="API для системы рекомендаций блюд Food2Mood",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_version="3.0.2"  # Используем стабильную версию OpenAPI
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене лучше указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency для получения базы данных
def get_database():
    return db

# Включение роутеров
app.include_router(menu.router, prefix="/api/v1/menu", tags=["menu"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(questionnaire.router, prefix="/api/v1", tags=["questionnaire"])

@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "message": "Food2Mood API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Проверка здоровья API"""
    try:
        if db is None:
            return {
                "status": "degraded",
                "database": "not_initialized"
            }
        # Проверяем подключение к базе данных
        db.connection.execute("SELECT 1")
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "degraded",
            "database": "error",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
