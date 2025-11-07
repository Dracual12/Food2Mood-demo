# 🚀 Руководство по развертыванию Food2Mood API

Подробная инструкция по размещению API на сервере и его публикации в интернете.

## 📋 Содержание

1. [Выбор хостинга](#выбор-хостинга)
2. [Подготовка кода](#подготовка-кода)
3. [Развертывание на VPS](#развертывание-на-vps)
4. [Развертывание на облачных платформах](#развертывание-на-облачных-платформах)
5. [Настройка домена и SSL](#настройка-домена-и-ssl)
6. [Безопасность](#безопасность)
7. [Мониторинг и логирование](#мониторинг-и-логирование)

---

## 🖥️ Выбор хостинга

### Варианты развертывания:

#### 1. **VPS (Virtual Private Server)** - Рекомендуется
- **DigitalOcean**: от $6/месяц
- **Linode**: от $5/месяц
- **Vultr**: от $6/месяц
- **Hetzner**: от €4/месяц
- **AWS EC2**: от $5/месяц

**Плюсы**: Полный контроль, гибкость, низкая стоимость
**Минусы**: Требует настройки и обслуживания

#### 2. **Облачные платформы (PaaS)**
- **Heroku**: от $7/месяц (простой деплой)
- **Railway**: от $5/месяц
- **Render**: бесплатный тариф доступен
- **Fly.io**: бесплатный тариф доступен
- **PythonAnywhere**: от $5/месяц

**Плюсы**: Простота развертывания, автоматическое масштабирование
**Минусы**: Меньше контроля, может быть дороже

---

## 🔧 Подготовка кода

### 1. Создайте файл для продакшена

Создайте файл `api/main_prod.py`:

```python
"""
Food2Mood API - Production Configuration
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
db_path = os.getenv("DATABASE_PATH", "/app/files/databse.db")
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
    openapi_version="3.0.2"
)

# CORS middleware - настройте для вашего домена
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
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
        "docs": "/docs",
        "status": "online"
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
        return {
            "status": "degraded",
            "database": "error",
            "error": str(e)
        }
```

### 2. Создайте файл `.env` для переменных окружения

```bash
# .env
DATABASE_PATH=/app/files/databse.db
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
SECRET_KEY=your-secret-key-here
DEBUG=False
```

### 3. Создайте `Dockerfile` (опционально, но рекомендуется)

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Установка зависимостей
COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода
COPY . .

# Создание директории для БД
RUN mkdir -p /app/files

# Переменные окружения
ENV PYTHONUNBUFFERED=1

# Порт
EXPOSE 8000

# Запуск
CMD ["uvicorn", "api.main_prod:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 4. Создайте `.dockerignore`

```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info
dist
build
.git
.venv
venv/
env/
.env
```

---

## 🖥️ Развертывание на VPS

### Шаг 1: Подключение к серверу

```bash
ssh root@your-server-ip
```

### Шаг 2: Установка необходимого ПО

```bash
# Обновление системы
apt update && apt upgrade -y

# Установка Python и pip
apt install python3 python3-pip python3-venv -y

# Установка Git
apt install git -y

# Установка Nginx (для reverse proxy)
apt install nginx -y

# Установка Supervisor (для управления процессом)
apt install supervisor -y
```

### Шаг 3: Клонирование проекта

```bash
cd /opt
git clone https://github.com/yourusername/koreanchick.git
cd koreanchick
```

### Шаг 4: Создание виртуального окружения

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r api/requirements.txt
```

### Шаг 5: Настройка Supervisor

Создайте файл `/etc/supervisor/conf.d/food2mood-api.conf`:

```ini
[program:food2mood-api]
command=/opt/koreanchick/venv/bin/uvicorn api.main_prod:app --host 0.0.0.0 --port 8000
directory=/opt/koreanchick
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/food2mood-api/error.log
stdout_logfile=/var/log/food2mood-api/access.log
environment=PATH="/opt/koreanchick/venv/bin"
```

Создайте директорию для логов:
```bash
mkdir -p /var/log/food2mood-api
```

Запустите Supervisor:
```bash
supervisorctl reread
supervisorctl update
supervisorctl start food2mood-api
supervisorctl status
```

### Шаг 6: Настройка Nginx как Reverse Proxy

Создайте файл `/etc/nginx/sites-available/food2mood-api`:

```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    client_max_body_size 10M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Активируйте конфигурацию:
```bash
ln -s /etc/nginx/sites-available/food2mood-api /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

---

## ☁️ Развертывание на облачных платформах

### Heroku

1. Установите Heroku CLI
2. Создайте файл `Procfile`:
```
web: uvicorn api.main_prod:app --host 0.0.0.0 --port $PORT
```

3. Развертывание:
```bash
heroku login
heroku create food2mood-api
heroku config:set DATABASE_PATH=/app/files/databse.db
git push heroku main
```

### Railway

1. Подключите GitHub репозиторий
2. Railway автоматически определит Python проект
3. Настройте переменные окружения в панели
4. Railway автоматически развернет проект

### Render

1. Создайте новый Web Service
2. Подключите GitHub репозиторий
3. Настройки:
   - **Build Command**: `pip install -r api/requirements.txt`
   - **Start Command**: `uvicorn api.main_prod:app --host 0.0.0.0 --port $PORT`
4. Добавьте переменные окружения
5. Deploy!

---

## 🌐 Настройка домена и SSL

### 1. Настройка DNS

Добавьте A-запись в DNS вашего домена:
```
Type: A
Name: api (или @ для корневого домена)
Value: IP-адрес вашего сервера
TTL: 3600
```

### 2. Установка SSL сертификата (Let's Encrypt)

```bash
# Установка Certbot
apt install certbot python3-certbot-nginx -y

# Получение сертификата
certbot --nginx -d api.yourdomain.com

# Автоматическое обновление
certbot renew --dry-run
```

Certbot автоматически обновит конфигурацию Nginx для HTTPS.

### 3. Обновление конфигурации Nginx для HTTPS

После установки SSL, Nginx будет автоматически настроен. Пример конфигурации:

```nginx
server {
    listen 80;
    server_name api.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.yourdomain.com/privkey.pem;

    client_max_body_size 10M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 🔒 Безопасность

### 1. Ограничение CORS

Обновите `api/main_prod.py`:
```python
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS", 
    "https://yourdomain.com,https://www.yourdomain.com"
).split(",")
```

### 2. Rate Limiting

Установите `slowapi`:
```bash
pip install slowapi
```

Добавьте в `api/main_prod.py`:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/")
@limiter.limit("100/minute")
async def root(request: Request):
    ...
```

### 3. Защита от DDoS

Настройте fail2ban:
```bash
apt install fail2ban -y
```

### 4. Firewall

```bash
# Установка UFW
apt install ufw -y

# Разрешить SSH
ufw allow 22/tcp

# Разрешить HTTP и HTTPS
ufw allow 80/tcp
ufw allow 443/tcp

# Включить firewall
ufw enable
```

### 5. Обновление зависимостей

Регулярно обновляйте зависимости:
```bash
pip install --upgrade -r api/requirements.txt
```

---

## 📊 Мониторинг и логирование

### 1. Настройка логирования

Добавьте в `api/main_prod.py`:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/food2mood-api/app.log'),
        logging.StreamHandler()
    ]
)
```

### 2. Мониторинг с помощью Uptime Robot

1. Зарегистрируйтесь на https://uptimerobot.com
2. Добавьте монитор для `https://api.yourdomain.com/health`
3. Настройте уведомления

### 3. Логирование запросов

Добавьте middleware для логирования:
```python
import time
from fastapi import Request

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logging.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.4f}s"
    )
    return response
```

---

## 🔄 Обновление API

### Процесс обновления:

```bash
# На сервере
cd /opt/koreanchick
git pull origin main
source venv/bin/activate
pip install -r api/requirements.txt
supervisorctl restart food2mood-api
```

---

## 📝 Чеклист развертывания

- [ ] Выбрать хостинг
- [ ] Подготовить код для продакшена
- [ ] Настроить переменные окружения
- [ ] Развернуть на сервере
- [ ] Настроить Nginx
- [ ] Настроить домен и DNS
- [ ] Установить SSL сертификат
- [ ] Настроить CORS
- [ ] Настроить firewall
- [ ] Настроить мониторинг
- [ ] Протестировать API
- [ ] Создать документацию для пользователей

---

## 🆘 Решение проблем

### API не запускается
```bash
# Проверьте логи
supervisorctl tail -f food2mood-api stderr

# Проверьте статус
supervisorctl status food2mood-api
```

### Проблемы с Nginx
```bash
# Проверьте конфигурацию
nginx -t

# Перезагрузите Nginx
systemctl reload nginx

# Проверьте логи
tail -f /var/log/nginx/error.log
```

### Проблемы с базой данных
```bash
# Проверьте права доступа
ls -la /app/files/databse.db

# Проверьте подключение
python3 -c "from database.db import Database; db = Database('/app/files/databse.db'); print('OK')"
```

---

## 📞 Полезные команды

```bash
# Перезапуск API
supervisorctl restart food2mood-api

# Просмотр логов
tail -f /var/log/food2mood-api/access.log

# Проверка статуса
supervisorctl status food2mood-api

# Проверка портов
netstat -tulpn | grep 8000
```

---

**Удачи с развертыванием! 🚀**

