import os
import random
import sys
import requests
import time
import urllib.parse
import json
import base64
import socket
from datetime import datetime



headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.9',
    'Content-Type': 'application/json',
    'Origin': 'https://major.bot',
    'Priority': 'u=1, i',
}

def make_request(method, url, headers, json=None, params=None, data=None):
    retry_count = 0
    while True:
        time.sleep(2)
        if method.upper() == "GET":
            if params:
                response = requests.get(url, headers=headers, params=params)
            elif json:
                response = requests.get(url, headers=headers, json=json)
            else:
                response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            if json:
                response = requests.post(url, headers=headers, json=json)
            elif data:
                response = requests.post(url, headers=headers, data=data)
            else:
                response = requests.post(url, headers=headers)
        elif method.upper() == "PUT":
            if json:
                response = requests.put(url, headers=headers, json=json)
            elif data:
                response = requests.put(url, headers=headers, data=data)
            else:
                response = requests.put(url, headers=headers)
        else:
            raise ValueError("Invalid method. Only GET, PUT and POST are supported.")
        if response.status_code >= 500:
            if retry_count >= 4:
                print_(f"Status Code : {response.status_code} | Server Down/Something")
                return None
            retry_count += 1
        elif response.status_code >= 400:
            print_(f"Status Code : {response.status_code} | Failed to get Coin")
            return None
        elif response.status_code >= 200:
            return response.json()

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_credentials():
    try:
        with open('query_id.txt', 'r') as f:
            queries = [line.strip() for line in f.readlines()]
        return queries
    except FileNotFoundError:
        print_("File query_id.txt tidak ditemukan.")
        return [  ]
    except Exception as e:
        print_("Terjadi kesalahan saat memuat token:", str(e))
        return [  ]

def getuseragent(index):
    try:
        with open('useragent.txt', 'r') as f:
            useragent = [line.strip() for line in f.readlines()]
        if index < len(useragent):
            return useragent[index]
        else:
            return "Index out of range"
    except FileNotFoundError:
        return 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'
    except Exception as e:
        return 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'



def postauth(query):
    url = 'https://major.bot/api/auth/tg/'
    data = {
        'init_data': query,
    }
    try:
        response = make_request('post', url, headers, json=data)
        return response
    except requests.exceptions.RequestException as e:
        print_(f'Error making request: {e}')
        return None
    
def getdaily(token):
    url ='https://major.bot/api/tasks/?is_daily=true'
    headers['Authorization'] = f"Bearer {token}"
    try:
        response = make_request('get', url, headers)
        return response
    except requests.exceptions.RequestException as e:
        print_(f'Error making request: {e}')
        return None

def gettask(token):
    url ='https://major.bot/api/tasks/?is_daily=false'
    headers['Authorization'] = f"Bearer {token}"
    try:
        response = make_request('get', url, headers)
        return response
    except requests.exceptions.RequestException as e:
        print_(f'Error making request: {e}')
        return None

def donetask(token, payload):
    url = 'https://major.bot/api/tasks/'
    headers['Authorization'] = f"Bearer {token}"
    try:
        response = make_request('post', url, headers, json=payload)
        return response
    except requests.exceptions.RequestException as e:
        print_(f'Error making request: {e}')
        return None

def visit(token):
    url = 'https://major.bot/api/user-visits/visit/?'
    headers['Authorization'] = f"Bearer {token}"
    try:
        response = make_request('post', url, headers)
        return response
    except requests.exceptions.RequestException as e:
        print_(f'Error making request: {e}')
        return None
    
def donate(token, amount):
    url = 'https://major.bot/api/invoices/'
    payload = {"amount":amount, 
               "buy_for_user_id":6057140648}
    headers['Authorization'] = f"Bearer {token}"
    try:
        response_codes_done = range(200, 241)
        response_code_failed = range(500, 540)
        response_code_notfound = range(400, 440)
        response = requests.post(url, headers, payload)
        if response.status_code in response_codes_done:
            return response.json()
        elif response.status_code in response_code_failed:
            print_(f"Response Code : {response.status_code} | Server Down")
            return None
        elif response.status_code in response_code_notfound:
            print_(response.text)
            return None
        else:
            raise Exception(f'Unexpected status code: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print_(f'Error making request: {e}')
        return None

def roulette(token):
    url ='https://major.bot/api/roulette/'
    headers['Authorization'] = f"Bearer {token}"

    try:
        response = make_request('post', url, headers)
        return response
    except requests.exceptions.RequestException as e:
        print_(f'Error making request: {e}')
        return None

def join_squad(token):
    url = 'https://major.bot/api/squads/2139244595/join/?'
    headers['Authorization'] = f"Bearer {token}"

    try:
        response = make_request('post', url, headers)
        return response
    except requests.exceptions.RequestException as e:
        print_(f'Error making request: {e}')
        return None

def get_squad(token):
    url = 'https://major.bot/api/squads/2139244595?'
    headers['Authorization'] = f"Bearer {token}"

    try:
        response = make_request('get', url, headers)
        return response
    except requests.exceptions.RequestException as e:
        print_(f'Error making request: {e}')
        return None

def claim_coins(token):
    url = 'https://major.bot/api/bonuses/coins/'
    coins = 915
    payload = {"coins":coins}
    headers['Authorization'] = f"Bearer {token}"
    try:
        response = make_request('post', url, headers, json=payload)
        if response is not None:
            if response.get('success') == True:
                print_(f"Success Claim Hold Coin {coins} Coins ")
            return response
    except requests.exceptions.RequestException as e:
        print_(f'Error making request: {e}')
        return None

def swipe_coin(token):
    url = 'https://major.bot/api/swipe_coin/'
    coins = random.randint(2500,3000)
    payload = {"coins":coins}
    headers['Authorization'] = f"Bearer {token}"
    try:
        response = make_request('post', url, headers, json=payload)
        if response is not None:
            if response.get('success') == True:
                print_(f"Success Claim Swipe Coin {coins} Coins ")
            return response
    except requests.exceptions.RequestException as e:
        print_(f'Error making request: {e}')
        return None
    
def get_detail(token, tgid):
    url = f'https://major.bot/api/users/{tgid}/'
    headers['Authorization'] = f"Bearer {token}"
    try:
        response = make_request('get', url, headers)
        return response
    except requests.exceptions.RequestException as e:
        print_(f'Error making request: {e}')
        return None

def durev_combo(token, payload):
    url = 'https://major.bot/api/durov/'
    headers['Authorization'] = f"Bearer {token}"
    try:
        response = make_request('post', url, headers, json=payload)
        if response is not None:
            correct = response.get('correct',[])
            ds = len(correct)
            if ds == 4:
                print_(f'Combo Done !! Reward 5000')
            else:
                print_(f'Combo Failed !! combo : {correct}')
            return response
    except requests.exceptions.RequestException as e:
        print_(f'Error making request: {e}')
        return None

def print_(word):
    now = datetime.now().isoformat(" ").split(".")[0]
    print(f"[{now}] {word}")

def convert_time(unix_time):
    formatted_time = time.strftime("%H:%M:%S", time.gmtime(unix_time))
    return formatted_time

def main():
    while True:
        majors = 0
        delay_time = (8 * 3900)
        start_time = time.time()
        queries = load_credentials()
        sum = len(queries)
        for index, query in enumerate(queries):
            useragent = getuseragent(index)
            headers['User-Agent'] = useragent
            print_(f"========== Account {index+1} ==========")
            time.sleep(1)
            data_auth = postauth(query)
            print_(f"refresh token....")
            time.sleep(2)
            if data_auth is not None:
                token = data_auth.get('access_token')
                user = data_auth.get('user')
                ratings = user.get('rating')
                id = user.get('id')
                squad_id = user.get('squad_id')

                detail = get_detail(token, id)
                if detail is not None:
                    ratings = detail.get('rating', 0)
                print_(f"TGID : {user.get('id')} | Name : {user.get('first_name')} {user.get('last_name')} | point : {ratings}")
                majors += ratings

                time.sleep(2)
                if squad_id == None:
                    print_('No Have Squad')
                    time.sleep(2)
                    print_('Joining Squad....')
                    time.sleep(2)
                    data_squad = join_squad(token)
                    if data_squad is not None:
                        print_("Join Squad Done")
                else:
                    data_squad = get_squad(token)
                    if data_squad is not None:
                        print_(f"Squad : {data_squad.get('name')} | Member : {data_squad.get('members_count')} | Ratings : {data_squad.get('rating')}")

                time.sleep(1)
                data_visit = visit(token)
                if data_visit is not None:
                    print_(f"Login Streak : {data_visit.get('streak')}")
                    time.sleep(1)
                print_('Start Hold Coin')
                time.sleep(2)
                claim_coins(token)
                print_('Start Swipe Coin')
                time.sleep(2)
                swipe_coin(token)
                time.sleep(1)

                print_("Spin Roulette")
                data_roulette = roulette(token)
                if data_roulette is not None:
                    time.sleep(3)
                    reward = data_roulette.get('rating_award')
                    if reward is not None:
                        print_(f"Success Reward Roulette : {data_roulette.get('rating_award')}")
                
                print_('Get daily Task')
                data_daily = getdaily(token)
                if data_daily is not None:
                    if len(data_daily) > 0:
                        for daily in reversed(data_daily):
                            id = daily.get('id')
                            type = daily.get('type')
                            title = daily.get('title')
                            is_completed = daily.get('is_completed')
                            if title not in ["Donate rating", "Invite more Friends", "Boost Major channel",
                                              "Promote TON blockchain", "Promote TON blockchain #2", "Promote TON blockchain #3",
                                              "Stars Purchase", "Extra Stars Purchase", "Boost Roxman channel"]:
                                if is_completed == False:
                                    time.sleep(2)
                                    payload = {
                                        'task_id': id
                                    }
                                    data_done = donetask(token, payload)
                                    if data_done is not None:
                                        print_(f"Task : {daily.get('title')} | Reward : {daily.get('award')} | Status: {data_done.get('is_completed')}")
                    else:
                        print_('No have daily task')

                print_('Get Single Task')
                data_task = gettask(token)
                if data_task is not None:
                    if len(data_task) > 0:
                        for task in data_task:
                            id = task.get('id')
                            type = task.get('type')
                            title = task.get('title')
                            if title not in ["One-time Stars Purchase", "Binance x TON", "Status Purchase"]:
                                time.sleep(2)
                                if type == 'code':
                                        payload = {"task_id":id,"payload":{"code":""}}
                                else:
                                    payload = {
                                                'task_id': id
                                            }
                                data_done = donetask(token, payload)
                                if data_done is not None:
                                        print_(f"Task : {title} | Reward : {task.get('award')} | Status: {data_done.get('is_completed')}")
                    else:
                        print_('No have single task')
                time.sleep(3)
                # if index != 0:
                #     if ratings >= 2500:
                #         amount = 2500
                #     elif ratings >= 1000:
                #         amount = 1000
                #     elif ratings >= 500:
                #         amount = 500
                #     elif ratings >= 250:
                #         amount = 250
                #     else:
                #         amount = 100
                #     data_donate = donate(token, amount)
                #     if data_donate is not None:
                #         print_(f"Donate amount {amount}")
            else:
                print_('User Not Found')
        end_time = time.time()
        total_time = delay_time - (end_time-start_time)
        print_(" ======================================================")
        print_(f"Total Account : {sum} | Total Ratings Majors: {majors}")
        print_(" ======================================================")
        print_delay(total_time)

def print_delay(delay):
    while delay > 0:
        now = datetime.now().isoformat(" ").split(".")[0]
        hours, remainder = divmod(delay, 3600)
        minutes, seconds = divmod(remainder, 60)
        sys.stdout.write(f"\r{now} | Waiting Time: {round(hours)} hours, {round(minutes)} minutes, and {round(seconds)} seconds")
        sys.stdout.flush()
        time.sleep(1)
        delay -= 1
    print_("\nWaiting Done, Starting....\n")

def quest_main():
    queries = load_credentials()
    input_string = input("input number (ex:14,2,3,4) : ").strip().lower()
    input_youtube = input("input code from youtube : ").strip().lower()
    if input_string != 'n':
        input_data = [int(x) for x in input_string.split(",")]
        payload = {"choice_{}".format(i+1): value for i, value in enumerate(input_data)}
    for index, query in enumerate(queries):
        useragent = getuseragent(index)
        headers['User-Agent'] = useragent
        print_(f"========== Account {index+1} ==========")
        time.sleep(1)
        data_auth = postauth(query)
        print_(f"refresh token....")
        time.sleep(2)
        if data_auth is not None:
            token = data_auth.get('access_token')
            user = data_auth.get('user')
            ratings = user.get('rating')
            id = user.get('id')
            squad_id = user.get('squad_id')
            detail = get_detail(token, id)
            if detail is not None:
                ratings = detail.get('rating', 0)
            print_(f"TGID : {user.get('id')} | Name : {user.get('first_name')} {user.get('last_name')} | point : {ratings}")
            if input_string != 'n' :
                data_combo = durev_combo(token, payload)
            if input_youtube != 'n':
                print_('Get Single Task')
                data_task = gettask(token)
                if data_task is not None:
                    if len(data_task) > 0:
                        for task in data_task:
                            id = task.get('id')
                            type = task.get('type')
                            title = task.get('title')
                            if title not in ["One-time Stars Purchase", "Binance x TON", "Status Purchase"]:
                                time.sleep(2)
                                if type == 'code':
                                        payload = {"task_id":id,"payload":{"code":input_youtube}}
                                else:
                                    payload = {
                                                'task_id': id
                                            }
                                if 'youtube' in title.lower():
                                    data_done = donetask(token, payload)
                                    if data_done is not None:
                                            print_(f"Task : {title} | Reward : {task.get('award')} | Status: {data_done.get('is_completed')}")
                else:
                    print_('No have single task')

def start():
    print(r"""
        
                    MAJOR BOT
    find new airdrop & bot here: t.me/sansxgroup
              
        select this one :
        1. claim daily
        2. clear quest game  
          
          """)
    selector = input("Select the one  : ").strip().lower()

    if selector == '1':
        main()
    elif selector == '2':
        quest_main()
    else:
        exit()

if __name__ == "__main__":
    start()
