from fastapi import FastAPI,Request
from telegram import Update
from tgbot import create_bot
import config
app=FastAPI()
application = create_bot()


@app.on_event("startup")
async def on_startup():
    await application.initialize()
    await application.bot.set_webhook("https://2ba1-116-240-116-37.ngrok-free.app/webhook")
    await application.start()


@app.post("/webhook")
async def tg_wbhook(request: Request):
    json_data = await request.json()
    update = Update.de_json(json_data, application.bot)
    await application.process_update(update)
    return {"status": "ok"}


@app.on_event("shutdown")
async def on_shutdown():

    await application.stop()