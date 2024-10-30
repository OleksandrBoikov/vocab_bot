from datetime import datetime,timedelta
from supabase import Client,create_client
import config,requests,schedule,time
from dateutil.relativedelta import relativedelta
SUPABASE_URL=config.SUPABASE_URL
SUPABASE_KEY=config.SUPABASE_KEY
supabase:Client=create_client(SUPABASE_URL,SUPABASE_KEY)


DAYS_CNT=0
def get_new_users(days):
    past_time=datetime.now()-timedelta(days=days)
    

    lis_users=supabase.table('users').select('tg_user_name').gt('created_at',past_time).execute()

    return len(lis_users.data)


def get_new_cards():
    past_time = datetime.now() - timedelta(days=7)
    lis_users = supabase.table('words').select('tg_user_id').gt('created_at', past_time).execute()

    return len(lis_users.data)

def get_practice_usage():
    pastweek = datetime.now() - timedelta(days=7)
    lis_users = supabase.table('events').select('tg_user_id').eq('event_name',"/practice").gt('created_at', pastweek).execute()

    return len(lis_users.data)
def get_practiced_once():
    data=supabase.rpc('unique_users_weekly').execute()

    return data.data
def get_unique_cards():
    data = supabase.rpc('unique_cards_weekly').execute()
    return data.data
def get_active_users():
    data=supabase.rpc('most_active_users').execute()
    return data.data

def send_message():
    global DAYS_CNT
    if DAYS_CNT%7==0:
        API_TOKEN = config.STAT_TOKEN
        CHAT_ID=config.CHAT_ID
        new_users=get_new_users(7)
        new_cards=get_new_cards()
        practice_used=get_practice_usage()
        uniequ_practice=get_practiced_once()
        active_users=get_active_users()
        unique_cards=get_unique_cards()

        MESSAGE=f'''For last week we got {new_users} new users,
{new_cards} cards been created, 
button "/practice" been used {practice_used} times,
users who used practise {uniequ_practice},
{unique_cards} people used cards,
MOST active users are {active_users}
            '''
        url = f'https://api.telegram.org/bot{API_TOKEN}/sendMessage'
        params = {
            'chat_id': CHAT_ID,
        'text': MESSAGE
        }
        response = requests.get(url, params=params)
        
        
    daily_info=get_new_users(1)
    if len(daily_info)!=0:
        MESSAGE=f"We got {len(daily_info)} new users "
    DAYS_CNT+=1




schedule.every(1).days.do(send_message)


# Бесконечный цикл для работы расписания
while True:
    schedule.run_pending()
    time.sleep(1)


