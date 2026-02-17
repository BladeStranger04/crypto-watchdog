# Crypto Market Bot

Асинхронный Telegram-бот для отслеживания курса криптовалют с использованием Binance API.

## Особенности
- Просмотр текущей цены и графика за последние 6 дней для популярных монет (BTC, ETH, BNB и др.).
- Режим **Screener** – автоматическое уведомление об изменении цены более чем на 1% (проверка каждую минуту).
- Полностью асинхронная архитектура на `aiogram` и `aiohttp`.
- Логирует все ключевые события.

## Технологии
- Python 3.10+
- aiogram 3.x
- aiohttp
- pandas, matplotlib
- python-dotenv

## Установка и запуск

1. Клонируй репозиторий:
```bash
   git clone https://github.com/BladeStranger04/crypto-bot.git
   cd crypto-bot
  ```


2. Создай виртуальное окружение и активируй:

```bash
  python -m venv venv

  source venv/bin/activate  # для Linux/Mac
  venv\Scripts\activate     # для Windows
```

3. Установи зависимости:

```bash
  pip install -r requirements.txt
```

4. Скопируй .env.example в .env и укажи свой BOT_TOKEN (его получи у @BotFather)

```bash
  cp .env.example .env
```

5. Запусти бота:
```bash
  python -m bot.main
```