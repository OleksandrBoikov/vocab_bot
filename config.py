import os
if os.path.exists(".env"):
    # if we see the .env file, load it
    from dotenv import load_dotenv
    load_dotenv()

# now we have them as a handy python strings!
BOT_TOKEN = os.getenv('BOT_TOKEN')
TELEGRAM_API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/'
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
BOT_TOKEN_PROD = os.getenv('BOT_TOKEN_PROD')
STAT_TOKEN=os.getenv('STAT_TOKEN')
OPENAI_KEY = os.getenv('OPENAI_KEY')
OPENAI_ORG = os.getenv('OPENAI_ORG')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
CHAT_ID=os.getenv('CHAT_ID')

DEEPL_KEY = os.getenv('DEEPL_KEY')
GOOGLE_TTS_KEY= os.getenv('GOOGLE_TTS_KEY')
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')