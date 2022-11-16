from aiogram import Bot, Dispatcher, executor

from config import TELEGRAM_TOKEN

bot = Bot(TELEGRAM_TOKEN)
dp = Dispatcher(bot)


async def on_startup(_):
    print('Bot has been started.')

if __name__ == '__main__':
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_startup
    )
