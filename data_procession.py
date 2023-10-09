import requests
import json
import time
from datetime import datetime
from dateutil.parser import parse

def get_data(offset):
    url = f"https://sef.podkolzin.consulting/api/users/lastSeen?offset={offset}"
    response = requests.get(url)
    data = response.json()
    return data['data']

def update_user_data(user, previous_state):
    if user['isOnline']:
        if user['userId'] not in previous_state or not previous_state[user['userId']]['isOnline']:
            user['onlinePeriods'] = previous_state.get(user['userId'], {}).get('onlinePeriods', [])
            user['onlinePeriods'].append([datetime.now().isoformat(), None])
        else:
            user['onlinePeriods'] = previous_state[user['userId']]['onlinePeriods']
    else:
        if user['userId'] in previous_state and previous_state[user['userId']]['isOnline']:
            last_online_period = previous_state[user['userId']]['onlinePeriods'][-1]
            last_online_period[1] = datetime.now().isoformat()
            user['onlinePeriods'] = previous_state[user['userId']]['onlinePeriods']
        else:
            user['onlinePeriods'] = previous_state.get(user['userId'], {}).get('onlinePeriods', [])
    return user

previous_state = {} 

def fetch_and_update_data():
    offset = 0
    all_data = []
    counter = 0

    while True:
        data = get_data(offset)

        if not data or counter > 1000: 
            break

        for d in data:
            user = { 'userId': d['userId'], 'isOnline': d['isOnline'], 'lastSeenDate': d['lastSeenDate'] }
            updated_user = update_user_data(user, previous_state)
            user['totalSecondsOnline'] = calculate_online_time(user)

            if updated_user['userId'] not in [user['userId'] for user in all_data]:
                all_data.append(updated_user)

            previous_state[updated_user['userId']] = updated_user

        offset += len(data)
        counter += 1


    with open('all_data.json', 'w') as f:
        json.dump(all_data, f)
        
def calculate_online_time(user):
    total_seconds_online = 0
    for period in user['onlinePeriods']:
        start_time = parse(period[0])
        end_time = parse(period[1]) if period[1] else datetime.now()
        total_seconds_online += (end_time - start_time).total_seconds()
    return total_seconds_online


if __name__ == "__main__":
    while True:
        fetch_and_update_data()
        time.sleep(10)