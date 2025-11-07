#!/usr/bin/env python3
"""
Скрипт для запуска Food2Mood веб-сайта
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    # Проверяем, что мы в правильной директории
    web_dir = Path(__file__).parent / "web"
    
    if not web_dir.exists():
        print("❌ Папка 'web' не найдена!")
        print("Убедитесь, что скрипт запускается из корневой папки проекта")
        sys.exit(1)
    
    # Переходим в папку web
    os.chdir(web_dir)
    
    print("🚀 Запускаем Food2Mood веб-сайт...")
    print("📁 Рабочая директория:", web_dir.absolute())
    
    # Проверяем, установлен ли Node.js
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js найден: {result.stdout.strip()}")
        else:
            print("❌ Node.js не найден!")
            print("Установите Node.js с https://nodejs.org/")
            sys.exit(1)
    except FileNotFoundError:
        print("❌ Node.js не найден!")
        print("Установите Node.js с https://nodejs.org/")
        sys.exit(1)
    
    # Проверяем, установлены ли зависимости
    if not (web_dir / "node_modules").exists():
        print("📦 Устанавливаем зависимости...")
        try:
            subprocess.run(['npm', 'install'], check=True)
            print("✅ Зависимости установлены!")
        except subprocess.CalledProcessError:
            print("❌ Ошибка при установке зависимостей!")
            sys.exit(1)
    
    # Запускаем веб-сайт
    print("🌐 Запускаем веб-сайт на http://localhost:3000")
    print("📱 Откройте браузер и перейдите по адресу выше")
    print("🛑 Для остановки нажмите Ctrl+C")
    
    try:
        subprocess.run(['npm', 'run', 'dev'], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Веб-сайт остановлен")
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при запуске: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
