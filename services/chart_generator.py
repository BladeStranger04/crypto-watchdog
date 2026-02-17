import io
import pandas as pd
import matplotlib.pyplot as plt
from utils.logger import setup_logger

logger = setup_logger(__name__)

class ChartGenerator:
    @staticmethod
    def price_chart(klines, coin_name: str) -> io.BytesIO:
        """
        Преобразует сырые данные klines в график цены и возвращает BytesIO
        """

        try:
            df = pd.DataFrame(klines, columns=[
                'open_time', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_asset_volume', 'number_of_trades',
                'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
            ])

            df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
            df['close'] = df['close'].astype(float)

            plt.figure(figsize=(8, 4))
            plt.plot(df['open_time'], df['close'], marker='o', linestyle='-', color='#1f77b4')
            plt.title(f'{coin_name} – last {len(df)} days')
            plt.xlabel('Date')
            plt.ylabel('Price (USDT)')

            plt.grid(True, alpha=0.3)

            plt.tight_layout()

            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=100)
            buf.seek(0)
            plt.close()

            return buf
        
        except Exception as e:
            logger.error(f"Failed to generate chart for {coin_name}: {e}")
            raise