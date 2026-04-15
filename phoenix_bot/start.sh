#!/bin/bash
set -e

# Запускаем FastAPI в фоне
uvicorn api:app --host 0.0.0.0 --port ${PORT:-8000} &

# Запускаем Telegram-бота (основной процесс)
python main.py
