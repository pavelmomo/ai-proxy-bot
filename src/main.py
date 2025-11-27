import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import BackgroundTasks, FastAPI, Request, Response, status

from bot import bot, puter_ai
from config import LOGGING_CONFIG, settings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(application: FastAPI):
    puter_ai.login()
    logger.info("Login to Puter successful!")

    settings.VK_CONFIRMATION_CODE, settings.VK_SECRET_KEY = await bot.setup_webhook()
    logger.info("Setup webhook successful!")
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


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_config=LOGGING_CONFIG)
