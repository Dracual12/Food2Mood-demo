"""
Food2Mood API - Production Configuration
"""
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
import logging
import time

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import Database
from api.models import *
from api.endpoints import menu, users, questionnaire

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Инициализация базы данных
db_path = os.getenv("DATABASE_PATH", os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
    'files', 
    'databse.db'
))
try:
    db = Database(db_path)
    logger.info(f"База данных инициализирована: {db_path}")
except Exception as e:
    logger.error(f"Ошибка инициализации БД: {e}")
    db = None

# CORS middleware - настройте для вашего домена
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
if allowed_origins == ["*"]:
    logger.warning("⚠️ CORS настроен на разрешение всех источников. В продакшене укажите конкретные домены!")

# Создание FastAPI приложения
app = FastAPI(
    title="Food2Mood API",
    description="API для системы рекомендаций блюд Food2Mood",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_version="3.0.2"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware для логирования запросов
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.4f}s - "
        f"IP: {request.client.host if request.client else 'unknown'}"
    )
    return response

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
        "docs": "/docs",
        "status": "online",
        "environment": os.getenv("ENVIRONMENT", "production")
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
        db.connection.execute("SELECT 1")
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "degraded",
            "database": "error",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "api.main_prod:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )

