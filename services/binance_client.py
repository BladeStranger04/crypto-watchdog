import aiohttp
from utils.config import BINANCE_API_URL
from utils.logger import setup_logger

logger = setup_logger(__name__)

class BinanceClient:
    def __init__(self):
        self.base_url = BINANCE_API_URL

    async def get_klines(self, symbol: str, interval: str = "1d", limit: int = 6):
        """
        Получить исторические свечи для указанного символа
        Возвращает список свечей или бросает исключение при ошибке
        """

        url = f"{self.base_url}/klines"

        params = {
            "symbol": symbol.upper(),
            "interval": interval,
            "limit": limit
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params) as resp:
                    if resp.status != 200:
                        error_text = await resp.text()
                        logger.error(f"Binance API error {resp.status}: {error_text}")
                        raise Exception(f"API error: {resp.status}")

                    data = await resp.json()
                    logger.debug(f"Fetched {len(data)} klines for {symbol}")

                    return data

            except aiohttp.ClientError as e:
                logger.error(f"Network error while fetching {symbol}: {e}")
                raise