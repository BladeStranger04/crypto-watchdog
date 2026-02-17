import asyncio
from aiogram import Bot
from services.binance_client import BinanceClient
from utils.logger import setup_logger

logger = setup_logger(__name__)

class ScreenerManager:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.tasks = {}
        self.client = BinanceClient()
        self.coins = [] # список монет, будет задан извне
        self.threshold = 1.0 # порог изменения в процентах

    def set_coins(self, coins: list):
        self.coins = coins

    async def _monitor(self, chat_id: int):
        """Фоновая задача для одного чата"""

        # храним предыдущие цены
        last_prices = {}

        while True:
            try:
                for coin in self.coins:
                    ticker = coin["ticker"]
                    klines = await self.client.get_klines(ticker, interval="1m", limit=1)

                    current_price = float(klines[-1][4])

                    if ticker in last_prices:
                        old = last_prices[ticker]
                        change = (current_price - old) / old * 100

                        if abs(change) >= self.threshold:

                            sign = "+" if change > 0 else ""

                            await self.bot.send_message(
                                chat_id,
                                f"*{coin['name']}* changed  {sign}{change:.2f}% (was {old:.2f}, now {current_price:.2f})",
                                parse_mode="Markdown"
                            )
                    last_prices[ticker] = current_price
            except Exception as e:
                logger.error(f"Screener error for chat {chat_id}: {e}")

            await asyncio.sleep(60)  # проверка каждую минуту

    async def start_for_chat(self, chat_id: int):
        if chat_id in self.tasks:
            self.tasks[chat_id].cancel()

        task = asyncio.create_task(self._monitor(chat_id))
        self.tasks[chat_id] = task

        logger.info(f"Screener started for chat {chat_id}")

    async def stop_for_chat(self, chat_id: int):
        if chat_id in self.tasks:
            self.tasks[chat_id].cancel()

            del self.tasks[chat_id]

            logger.info(f"Screener stopped for chat {chat_id}")