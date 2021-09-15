# UsersSearcher Script
import db
import api
import sys
import time
import argvs
import tokens
import threads
import functions

"""Подключаюсь к базе данных
----------------------------"""
connect = db.connect()
"""Выбираю рекламную кампанию
-----------------------------"""
company = db.campaing(connect)
length = len(company)
counter = 0
for camp in company:
    counter += 1
    print(str(counter) + ' - ' + camp)
print('Выберите кампании (одну или несколько):' + str(length))
company_number = input('> ')
company_number = company_number.split()
campaings = []
for camp in company_number:
    if camp.isdigit():
        num = int(camp)
        company_name = company[num - 1]
        company_name = company_name.split()
        company_name = company_name[0][:-1]
        campaings.append(company_name)
        print('Выбрана кампания: ' + company_name)
    else:
        print('Введите целое число от 1 до ' + str(counter))
        quit()
""" Обрабатываю параметры командной строки
------------------------------------------"""
arguments = sys.argv
distr = argvs.argv_proc_us(arguments, campaings)
print(distr)
"""Обрабатываю список ключевых слов
-----------------------------------"""
keywords = distr[7]
try:
    keyword = keywords[0].title()
except IndexError:
    print('Введите ключевые слова')
    quit()
"""Обрабатываю список токенов
-----------------------------"""
tokens_list = tokens.tokens_settings(distr)
preview = 0
exp = tokens.expenditure(tokens_list)
print(exp)
"""Выбираю из базы целевые сообщества
-------------------------------------"""
all_groups = []
for campany in campaings:
    groups = db.array(connect, 'db_name', 'communitys', 'campaing', campany)
    for group in groups:                                                # Для каждого сообщества
        if len(distr[0]) > 0:                                           # Если указана страна
            if group['country'] in distr[0]:                            # Если страна совпадает с указанной
                if len(distr[5]) > 0:                                   # Если указано число пользователей
                    if functions.limits(group, distr[5]):               # Если группа подъходит под описание
                        if keyword in group['keywords']:                # Если соответствуют ключевые слова
                            all_groups.append(group)                    # ДОБАВЛЯЕМ ГРУППУ В СПИСОК
                else:                                                   # Если число пользователей отсутствует
                    if keyword in group['keywords']:                    # Если соответствуют ключевые слова
                        all_groups.append(group)                        # ДОБАВЛЯЕМ ГРУППУ В СПИСОК
        if len(distr[1]) > 0:                                           # Если указан город
            if group['city'] in distr[1]:                               # Если город совпадает с указанным
                if len(distr[5]) > 0:                                   # Если указано число пользователей
                    if functions.limits(group, distr[5]):               # Если группа подъходит под описание
                        if keyword in group['keywords']:                # Если соответствуют ключевые слова
                            all_groups.append(group)                    # ДОБАВЛЯЕМ ГРУППУ В СПИСОК
                else:                                                   # Если число пользователей отсутствует
                    if keyword in group['keywords']:                    # Если соответствуют ключевые слова
                        all_groups.append(group)                        # ДОБАВЛЯЕМ ГРУППУ В СПИСОК
        if len(distr[0]) + len(distr[1]) == 0:                          # Если нет ни страны, ни города
            if len(distr[5]) > 0:                                       # Если указано число пользователей
                if functions.limits(group, distr[5]):                   # Если группа подъходит под описание
                    if keyword in group['keywords']:                    # Если соответствуют ключевые слова
                        all_groups.append(group)                        # ДОБАВЛЯЕМ ГРУППУ В СПИСОК
            else:                                                       # Если число пользователей отсутствует
                if keyword in group['keywords']:                        # Если соответствуют ключевые слова
                    all_groups.append(group)                            # ДОБАВЛЯЕМ ГРУППУ В СПИСОК
"""Обрабатываю в цикле целевые сообщества
-----------------------------------------"""
parsed_counter = []
for group in all_groups:
    parsed_num = group['parsed_counter']
    if parsed_num not in parsed_counter:
        parsed_counter.append(parsed_num)
print(parsed_counter)
"""Обрабатываю время последнего парсинга
________________________________________"""
print("Какое количество раз осуществлялся парсинг?")
print("(для завершения старых задач по парсингу указывайте наименьшее число)")
string = ''
for parsing in parsed_counter:
    string + str(parsing)
print(string)
num = input('> ')
if not num.isnumeric():
    print("Выберите правильное число")
    quit()
if int(num) not in parsed_counter:
    print("Выберите правильное число")
    quit()
else:
    new_arr = []
    for group in all_groups:
        if group['parsed_counter'] == int(num):
            if group['users_hidden'] == 0:
                new_arr.append(group)
all_groups = new_arr
new_arr = []
print("Найдено " + str(len(all_groups)) + ' целевых сообществ с тематикой "' + keyword + '"')
print("Enter - продолжить, exit - прервать")
check = input('> ')
if check == 'exit':
    sys.exit()
counter = 0
eternal_counter = 0
for group in all_groups:
    counter += 1
    eternal_counter += 1
    if counter > 99:
        counter = 0
        print(exp)
        input()
    group_id = group['_id']
    group_name = group['name']
    group_members = group['users'][0]
    campaing = group['campaing'][0]
    comm = group['_id']
    """Получаю идентификатор сообщества
    ___________________________________"""
    group_id = group['_id']
    parsed_counter = group['parsed_counter']
    parsed = parsed_counter =+ 1
    print("Выполнить поиск в сообществе " + group_name + " (y/n)?")
    print('Пользователей: ' + str(group_members))
    answer = input('> ')
    if answer == 'exit':
        print("Расходование токенов:")
        print(exp)
        sys.exit()
    if (answer == '' or answer == 'y' or answer == 'yes'):
        """Получаю рандомный токен
        __________________________"""
        token_index = tokens.token(tokens_list, preview)
        token = tokens_list[int(token_index)]
        preview = token_index
        exp[token_index] += 1
        response = api.groups_get_members(group_id, 0, token)
        unixtime = int(time.time())
        """Если пользователи скрыты, обновляю инфу о сообществе"""
        if response == False:
            db.update(connect, "db_name", "communitys", "_id", group_id, "users_hidden", 1)
            print("Пользователи сообщества " + group_name + " скрыты!")
            """Если не скрыты, начинаю парсинг:"""
        else:
            """Если пользователей более 1000"""
            if int(response["count"]) > 1000:
                print("Запускаем потоки")
                count = response["count"]
                exp = threads.threads_start(connect, comm, count, tokens_list, campaing, keyword, exp)
                print("Расходование токенов:")
                print(exp)
                db.update(connect, 'db_name', 'communitys', '_id', group_id, 'parsed_counter', parsed)
                """Если пользователей не более 1000"""
            else:
                print("Парсим пользователей")
                update_list = []
                insert_list = []
                users = response["items"]
                for user in users:
                    save_check = functions.users_save_check(connect, user, unixtime, campaing, keyword, comm)
                    if save_check:
                        if save_check[0] == 0:
                            insert_list.append(save_check[2])
                        if save_check[0] == 1:
                            update_list.append(save_check[2])
                if len(insert_list) > 0:
                    data = db.inserts(connect, 'db_name', 'users', insert_list)
                    db.update(connect, 'db_name', 'communitys', '_id', group_id, 'parsed_counter', parsed)
                    print('Добавлено ' + str(len(insert_list)) + ' пользователей')
                    print(data)
                if len(update_list) > 0:
                    print("Обновлено " + str(len(update_list)) + " пользователей")
                time.sleep(2)
                print("Расходование токенов:")
                print(exp)