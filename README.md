# 🤖 Tender Automation System

Полностью бесплатная система автоматизации работы с тендерами.

## 🚀 Быстрый старт

### 1. Установите зависимости
```bash
pip install -r requirements.txt
```

### 2. Настройте переменные окружения
```bash
cp .env.example .env
# Отредактируйте .env и добавьте свои данные
```

### 3. Создайте Telegram бота
- Откройте @BotFather в Telegram
- Создайте бота командой /newbot
- Скопируйте токен в .env

### 4. Запустите мониторинг
```bash
python main.py monitor
```

## 📋 Команды

- `python main.py monitor` - поиск новых тендеров
- `python main.py analyze` - анализ документов
- `python main.py generate` - генерация КП
- `python main.py check` - проверка статусов

## 🔧 GitHub Actions

Для автоматической работы в облаке:

1. Создайте форк этого репозитория
2. Добавьте секреты в Settings → Secrets:
   - `TELEGRAM_TOKEN`
   - `TELEGRAM_CHAT_ID`
3. Активируйте Actions

## 📞 Поддержка

Создайте Issue если нужна помощь!
