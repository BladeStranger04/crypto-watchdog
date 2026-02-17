from aiogram import Router, types, F
from aiogram.filters import Command
from bot.keyboards import main_menu_keyboard, currency_list_keyboard
from services.binance_client import BinanceClient
from services.chart_generator import ChartGenerator
from utils.logger import setup_logger
from bot.scheduler import ScreenerManager

router = Router()
logger = setup_logger(__name__)

# список монет
COINS = [
    {"name": "Bitcoin", "ticker": "BTCUSDT"},
    {"name": "Ethereum", "ticker": "ETHUSDT"},
    {"name": "Binance Coin", "ticker": "BNBUSDT"},
    {"name": "Cardano", "ticker": "ADAUSDT"},
    {"name": "Dogecoin", "ticker": "DOGEUSDT"},
    {"name": "Polkadot", "ticker": "DOTUSDT"},
    {"name": "Chainlink", "ticker": "LINKUSDT"},
    {"name": "Litecoin", "ticker": "LTCUSDT"},
    {"name": "Ripple", "ticker": "XRPUSDT"},
]

binance = BinanceClient()
chart_gen = ChartGenerator()

# менеджер скринера (будет определён в scheduler.py, передадим при старте)
screener_manager = None

def init_screener(manager):
    global screener_manager
    screener_manager = manager

@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "Привет! Я бот для отслеживания курса криптовалют\n"
        "Выбери режим:",
        reply_markup=main_menu_keyboard()
    )

@router.message(F.text == "Currency Tracker")
async def currency_tracker_mode(message: types.Message):

    # останавливаем скринер, если он был запущен
    if screener_manager:
        await screener_manager.stop_for_chat(message.chat.id)

    names = [coin["name"] for coin in COINS]
    await message.answer(
        "Выбери монету для просмотра курса:",
        reply_markup=currency_list_keyboard(names)
    )

@router.message(F.text == "Screener")
async def screener_mode(message: types.Message):

    if not screener_manager:
        await message.answer("Скринер временно недоступен (x)")
        return

    await screener_manager.start_for_chat(message.chat.id)

    await message.answer(
        "Режим скринера включён. Я буду уведомлять тебя об изменениях цены больше 1%",
        reply_markup=main_menu_keyboard()
    )

@router.message(F.text == "Back to menu ->")
async def back_to_menu(message: types.Message):

    if screener_manager:
        await screener_manager.stop_for_chat(message.chat.id)

    await message.answer("Главное меню:", reply_markup=main_menu_keyboard())

@router.message(F.text.in_([coin["name"] for coin in COINS]))
async def show_coin_info(message: types.Message):
    coin_name = message.text
    coin = next((c for c in COINS if c["name"] == coin_name), None)

    if not coin:
        return

    try:
        klines = await binance.get_klines(coin["ticker"])
        current_price = float(klines[-1][4])  # close price последней свечи

        # генерим график
        chart_buf = chart_gen.price_chart(klines, coin_name)

        await message.answer_photo(
            photo=types.BufferedInputFile(chart_buf.getvalue(), filename="chart.png"),
            caption=f"*{coin_name}* – {current_price:,.2f} USDT",
            parse_mode="Markdown"
        )

    except Exception as e:
        logger.error(f"Error processing {coin_name}: {e}")
        await message.answer("⚠Не удалось получить данные. Попробуй позже")