import logging,config,openai,asyncio
import asyncio
from supabase import create_client, Client
from telegram import Update,InlineKeyboardMarkup,InlineKeyboardButton
from telegram.ext import filters, MessageHandler,ApplicationBuilder, ContextTypes, CommandHandler,CallbackQueryHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
url = config.supaurl
key=config.supakey
supabase: Client = create_client(url, key)
openai.api_key = config.gptapi


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    keyboard=[
        [InlineKeyboardButton('French',callback_data=f'{user_id}:French')],
        [InlineKeyboardButton('Spanish',callback_data=f'{user_id}:Spanish')]

    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Which language you want to learn?",reply_markup=reply_markup

    )
def add_user_sinc(username, language):

    response = supabase.table('users').insert({
        'username': username,
        'language': language,
    }
    ).execute()


async def add_user(username,language):
    loop = asyncio.get_running_loop()  # Получаем текущий event loop
    result = await loop.run_in_executor(None, add_user_sinc,username,language)



def add_phrase_sync(user_id,phrase,translation):
    response=supabase.table('words').insert({
        'user_id':user_id,
        'word':phrase,
        'translation':translation,
    }
    ).execute()

async def add_phrase(user_id,phrase,translation):
    loop = asyncio.get_running_loop()  # Получаем текущий event loop
    result = await loop.run_in_executor(None, add_phrase_sync,user_id,phrase,translation)
def get_user_language_sync(user_id):
    response = supabase.table('users').select('language').eq('username', user_id).execute()

    if response.data:
        user_language = response.data[0]['language']
        return user_language
    else:
        return None

async def get_user_language(user_id):

    loop=asyncio.get_running_loop()
    result=await loop.run_in_executor(None,get_user_language_sync,user_id)
    return result
async def button(update, context):
    query = update.callback_query
    await query.answer()
    data=query.data.split(':')
    await add_user(data[0],data[1])
    await query.edit_message_text(text=f"Great I would help you to learn {data[1]}")

async def translate(text, target_lang):
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that translates text."},
            {"role": "user", "content": f"Translate the following text into {target_lang}: {text}"}
        ],
        max_tokens=60,
        temperature=0.7
    )
    return response['choices'][0]['message']['content'].strip()

async def replyWithTranslated(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg=update.message.text

    user=update.message.from_user
    user_id=user.id
    lang=await get_user_language(user_id)
    msg_translated =await translate(msg, lang)
    await add_phrase(user_id,msg,msg_translated)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg_translated)
def create_bot():
    url = config.supaurl
    key=config.supakey
    supabase: Client = create_client(url, key)
    openai.api_key = config.gptapi
    tgapi = config.tgapi
    application = ApplicationBuilder().token(tgapi).build()
    translation_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), replyWithTranslated)
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(translation_handler)
    return application