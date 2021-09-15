import files
import pymongo


# Соединение с базой
def connect():
    connection = 'mongodb://' + files.config('settings.conf', 'user') \
                 + ':' + files.config('settings.conf', 'password') \
                 + '@' + files.config('settings.conf', 'server') \
                 + ':' + files.config('settings.conf', 'port') \
                 + '/' + files.config('settings.conf', 'db')
    return pymongo.MongoClient(connection)


# Проверка записи на существование
def check(connect, db_name, coll_name, key, value):
    db = connect[db_name]
    coll = db[coll_name]
    data = coll.count_documents({key: value})
    return data


# Поиск множества записей по ключу
def data(connect, db_name, coll_name, key, value):
    result = []
    db = connect[db_name]
    coll = db[coll_name]
    data = coll.find()
    for d in data:
        param = d[key]
        if param == value:
            result.append(d)
    return result


# Поиск по массиву ключей
def array(connect, db_name, coll_name, key, value):
    result = []
    db = connect[db_name]
    coll = db[coll_name]
    filter = {key: value}
    for d in coll.find(filter):
        result.append(d)
    return result


# Поиск одной записи
def find(connect, db_name, coll_name, key, value):
    db = connect[db_name]
    coll = db[coll_name]
    data = coll.find_one({key: value})
    return data


# Добавление новой записи
def insert(connect, db_name, coll_name, string):
    db = connect[db_name]
    coll = db[coll_name]
    data = coll.insert_one(string)
    return data


# Добавление множества записей
def inserts(connect, db_name, coll_name, array):
    db = connect[db_name]
    coll = db[coll_name]
    data = coll.insert_many(array)
    return data


# Обновление одной записи
def update(connect, db_name, coll_name, key, value, parameter, new_value):
    db = connect[db_name]
    coll = db[coll_name]
    data = coll.update_one({key: value}, {"$set": {parameter: new_value}})
    return data


# Обновление записи пользователя
def user_update(connect, db_name, coll_name, user):
    database = connect[db_name]
    coll = database[coll_name]
    data = coll.update_one({
        "_id": user['_id']
    }, {
        "$set": {
        "last_parsing": user["last_parsing"],
        "campaings": user['campaings'],
        "keywords": user['keywords'],
        "communitys": user['communitys'],
        "communitys_counter": user["communitys_counter"]
        }})
    return data


# Обновление множества записей
def updates(connect, db_name, coll_name, string):
    db = connect[db_name]
    coll = db[coll_name]
    data = coll.update_many(string)
    return data


# Добавление данных в одну запись
def push(connect, db_name, coll_name, key, value, parameter, new_value):
    db = connect[db_name]
    coll = db[coll_name]
    data = coll.update_one({key: value}, {"$push": {parameter: new_value}})
    return data


# Вывод коллекций по запросу
def collection(connect, db_name, coll_name, params_name, keyword):
    result = []
    db = connect[db_name]
    coll = db[coll_name]
    data = coll.find()
    for d in data:
        param = d[params_name]
        keywds = d[keyword]
        string = ''
        for key in keywds:
            string = string + key + ', '
        string = string[:-2]
        result.append(param + ': ' + string)
    return result


# Вывод всех имеющихся кампаний
def campaing(connect):
    return collection(connect, 'db_name', 'campaigns', 'company', 'keywords')