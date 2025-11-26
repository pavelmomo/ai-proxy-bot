from puter import PuterAI, PuterAPIError
from vkbottle import Bot
from vkbottle.bot import Message
from vkbottle.callback import BotCallback

from config import settings

bot_calback = BotCallback(url=settings.CALLBACK_URL)
bot = Bot(token=settings.VK_TOKEN, callback=bot_calback)

puter_ai = PuterAI(settings.PUTER_USERNAME, settings.PUTER_PASSWORD)
USERS_HISTORIES: dict[int, list] = {}


@bot.on.private_message()
async def proxy_messages(message: Message):
    user_id = message.from_id

    if user_id not in USERS_HISTORIES:
        USERS_HISTORIES[user_id] = []

    puter_ai.chat_history = USERS_HISTORIES[user_id]
    try:
        response = await puter_ai.async_chat(message.text)
        await message.answer(response)
    except PuterAPIError:
        await message.answer("Ошибка обработки запроса")


@bot.on.private_message(text="/очистка")
async def clear_history(message: Message):
    if message.from_id in USERS_HISTORIES:
        del USERS_HISTORIES[message.from_id]
    await message.answer("Выполнена очистка истории")
