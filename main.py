from datetime import datetime,timedelta
from supabase import Client,create_client
import config,requests,schedule,time
from dateutil.relativedelta import relativedelta
SUPABASE_URL=config.SUPABASE_URL
SUPABASE_KEY=config.SUPABASE_KEY
supabase:Client=create_client(SUPABASE_URL,SUPABASE_KEY)

def get_new_users():
    #pastweek=datetime.now()-timedelta(days=7)
    pastweek = (datetime.now() - relativedelta(months=2)).date()

    lis_users=supabase.table('users').select('tg_user_name').gt('created_at',pastweek).execute()

    return len(lis_users.data)


def get_new_cards():
    pastweek = datetime.now() - timedelta(days=7)
    lis_users = supabase.table('words').select('tg_user_id').gt('created_at', pastweek).execute()

    return len(lis_users.data)

def get_practice_usage():
    pastweek = datetime.now() - timedelta(days=7)
    lis_users = supabase.table('events').select('tg_user_id').eq('event_name',"/practice").gt('created_at', pastweek).execute()

    return len(lis_users.data)
def get_practiced_once():
    cnt=supabase.rpc('most_active_users').execute()

    return cnt


def send_message():
    API_TOKEN = config.STAT_TOKEN
    CHAT_ID=config.CHAT_ID
    new_users=get_new_users()
    new_cards=get_new_cards()
    practice_used=get_practice_usage()
    uniequ_practice=get_practiced_once()

    MESSAGE=f'''For last week we got {new_users} new users,{new_cards} cards been created, button "/practice" been used {practice_used} times,users who used practise{uniequ_practice}
MOST active users
'''
    url = f'https://api.telegram.org/bot{API_TOKEN}/sendMessage'
    params = {
        'chat_id': CHAT_ID,
        'text': MESSAGE
    }
    response = requests.get(url, params=params)

schedule.every(1).minutes.do(send_message)
pars=get_practiced_once()
print(pars.data)
pass
# Бесконечный цикл для работы расписания
#while True:
#schedule.run_pending()
    #time.sleep(1)


