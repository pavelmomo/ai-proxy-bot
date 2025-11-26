from contextlib import asynccontextmanager

from fastapi import BackgroundTasks, FastAPI, Request, Response, status
from loguru import logger

from bot import bot
from config import settings


@asynccontextmanager
async def lifespan(application: FastAPI):
    logger.info("Setup webhook")
    settings.VK_CONFIRMATION_CODE, settings.VK_SECRET_KEY = await bot.setup_webhook()
    yield


app = FastAPI(lifespan=lifespan)


@app.post(settings.CALLBACK_PATH)
async def vk_handler(req: Request, background_task: BackgroundTasks):
    try:
        data = await req.json()
    except Exception:
        logger.warning("Empty request")
        return Response("Empty request", status_code=status.HTTP_403_FORBIDDEN)

    if data["type"] == "confirmation":
        logger.info("Send confirmation token: {}", settings.VK_CONFIRMATION_CODE)
        return Response(settings.VK_CONFIRMATION_CODE)

    # If the secrets match, then the message definitely came from our bot
    if data["secret"] == settings.VK_SECRET_KEY:
        # Running the process in the background, because the logic can be complicated
        background_task.add_task(bot.process_event, data)
    return Response("Ok")
