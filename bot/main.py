import asyncio
from aiogram import Bot, Dispatcher
from utils.config import BOT_TOKEN
from utils.logger import setup_logger
from bot.handlers import router, init_screener
from bot.scheduler import ScreenerManager
from bot.handlers import COINS

logger = setup_logger(__name__)

async def main():
    logger.info("Starting bot...")

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # инициализируем менеджер скринера и передадим ему список монет
    screener_manager = ScreenerManager(bot)
    screener_manager.set_coins(COINS)

    # передаём менеджер в обработчики
    init_screener(screener_manager)

    dp.include_router(router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())