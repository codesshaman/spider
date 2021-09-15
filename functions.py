import time
import db
from tokens import token


# Функция определения, сохранять пользователя в БД или нет
def users_save_check(connect, user, unixtime, campaing, keyword, community):
    save = True
    # Проверяем, не занесён ли пользователь в blacklist:
    blackcheck = db.check(connect, 'db_name', 'your_blacklist_db', '_id', user['id'])
    if blackcheck == 0:
        save = True
    if blackcheck == 1:
        save = False
    # Проверяем, есть ли unixtime последнего входа
    if 'last_seen' in user:
        last_seen = int(user["last_seen"]["time"])
    else:
        last_seen = unixtime
    # Проверяем, не удалял ли пользователь страницу
    if user["first_name"] == 'DELETED':
        save = False
    # Проверяем, не удалён ли пользователь
    if 'deactivated' in user:
        save = False
    # Проверяем, не заброшена ли страница
    if unixtime - last_seen > 7776000:
        save = False
    if save:
        # Проверяем, существует ли пользователь в базе
        user_data = db.find(connect, 'db_name', 'your_users_db', '_id', user['id'])
        if user_data is None:
            final_record = user_save(user, unixtime, campaing, keyword, community)
            return [0, user['id'], final_record]
        else:
            record = user_update(connect, user_data, unixtime, campaing, keyword, community)
            if record:
                return [1, user_data['_id'], record]
    else:
        return save


# Функция формирования данных пользователя для сохранения
def user_save(user, unixtime, campaing, keyword, community):
    set = {}
    set['_id'] = user["id"]
    set['name'] = user['first_name']
    set['last_name'] = user['last_name']
    set['sex'] = user['sex']
    if 'bdate' in user:
        set['bdate'] = user['bdate']
    if 'city' in user:
        set['city'] = user['city']['id']
    if 'city' in user:
        set['city_name'] = user['city']['title']
    if 'country' in user:
        set['country'] = user['country']['id']
    if 'country' in user:
        set['country_name'] = user['country']['title']
    if 'status' in user:
        if len(user['status']) > 0:
            set['status'] = user['status'].replace("'", '"').replace('\n', ' ')
    if 'contacts' in user:
        set['contacts'] = user['contacts']
    if 'site' in user:
        if len(user['site']) > 0:
            set['site'] = user['site']
    if 'mobile_phone' in user:
        if len(user['mobile_phone']) > 0:
            set['mobile_phone'] = user['mobile_phone']
    if 'home_phone' in user:
        if len(user['home_phone']) > 0:
            set['home_phone'] = user['home_phone']
    if 'last_seen' in user:
        set['last_seen'] = user['last_seen']['time']
        if 'platform' in user['last_seen']:
            set['platform'] = user['last_seen']['platform']
    set['last_parsing'] = unixtime
    set['campaings'] = [campaing]
    set['keywords'] = [keyword]
    set['communitys'] = [community]
    set['communitys_counter'] = 1
    return set


# Функция обновления данных пользователя
def user_update(connect, user, unixtime, campaing, keyword, community):
    refresh = False
    if campaing not in user['campaings']:
        refresh = True
        user['campaings'].append(campaing)
    if community not in user['communitys']:
        refresh = True
        user['communitys'].append(community)
        user["communitys_counter"] = len(user['communitys'])
    if keyword not in user["keywords"]:
        refresh = True
        user['keywords'].append(keyword)
    if refresh:
        user["last_parsing"] = unixtime
        data = db.user_update(connect, 'db_name', 'your_users_db', user)
        print(data)
        return data


def print_community(item):
    print('Адрес:     | https://vk.com/public' + str(item['id']))
    print('Название:  | ' + item['name'])
    print('Статус :   | ' + item['status'])
    print('Описание:  | ' + item['description'])
    if item['can_see_all_posts'] == 0:
        print('Стена:     | закрытая')
    if item['can_see_all_posts'] == 1:
        print('Стена:     | открытая')
    if item['can_post'] == 0:
        print('Постинг:   | запрещён')
    if item['can_post'] == 1:
        print('Постинг:   | разрешён')
    print('Название:  | ' + item['name'])
    print('Участники: | ' + str(item['members_count']))


def add_community(connect, item, session_number, keyword, city, city_name, country, unixtime, company_name):
    set = {
        '_id': item['id'],
        'session': session_number,
        'name': item['name'].replace("'", '"').replace('\n', ''),
        'description': item['description'].replace("'", '"').replace('\n', ' '),
        'keywords': [keyword],
        'city': city,
        'city_name': city_name,
        'country': country,
        'users_hidden': 0,
        'parsed_counter': 0,
        'create_time': unixtime,
        'users': [item['members_count']],
        'parsing_times': [unixtime],
        'campaing': [company_name]
    }
    print('Добавляю в базу сообщество "' + item['name'] + '"')
    ins = db.insert(connect, 'db_name', 'communitys', set)
    print(ins)


def update_community(connect, item, unixtime, company_name, keyword):
    print('Обновляю информацию о сообществе "' + item['name'] + '"')
    record = db.find(connect, 'db_name', 'communitys', '_id', item['id'])
    members = record["users"]
    camparr = record["campaing"]
    if company_name not in camparr:
        db.push(connect, 'db_name', 'communitys', '_id', item['id'], 'campaing', company_name)
    key = record["keywords"]
    if keyword not in key:
        db.push(connect, 'db_name', 'communitys', '_id', item['id'], 'keywords', keyword)
    camp = record["campaing"]
    if company_name not in camp:
        db.push(connect, 'db_name', 'communitys', '_id', item['id'], 'campaing', company_name)
    db.push(connect, 'db_name', 'communitys', '_id', item['id'], 'users', item['members_count'])
    db.push(connect, 'db_name', 'communitys', '_id', item['id'], 'parsing_times', unixtime)

# Проверка группы на
# соответствие лимитам
def limits(group, limits):
    users = group['users'][0]
    now = int(users)
    limit = int(limits[0])
    if limit <= now:
        return True
    else:
        return False