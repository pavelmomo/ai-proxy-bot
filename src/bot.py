from vkbottle import Bot
from vkbottle.bot import Message
from vkbottle.callback import BotCallback

from config import settings

bot_calback = BotCallback(url=settings.CALLBACK_URL)
bot = Bot(token=settings.VK_TOKEN, callback=bot_calback)


@bot.on.message()
async def hi_handler(message: Message):
    users_info = await bot.api.users.get(user_ids=[message.from_id])
    await message.answer(f"Hello, {users_info[0].first_name}")
