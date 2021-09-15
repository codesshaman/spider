# UsersActyvitys Script
import db
import api
import sys
import time
import argvs
import tokens
import threads
import threading
import functions
import xlsxwriter

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
                    if functions.limits(group, distr[5]):               # Если группа подходит под описание
                        if keyword in group['keywords']:                # Если соответствуют ключевые слова
                            all_groups.append(group)                    # ДОБАВЛЯЕМ ГРУППУ В СПИСОК
                else:                                                   # Если число пользователей отсутствует
                    if keyword in group['keywords']:                    # Если соответствуют ключевые слова
                        all_groups.append(group)                        # ДОБАВЛЯЕМ ГРУППУ В СПИСОК
        if len(distr[1]) > 0:                                           # Если указан город
            if group['city'] in distr[1]:                               # Если город совпадает с указанным
                if len(distr[5]) > 0:                                   # Если указано число пользователей
                    if functions.limits(group, distr[5]):               # Если группа подходит под описание
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
print("Найдено " + str(len(all_groups)) + ' целевых сообществ с тематикой "' + keyword + '"')
print("Enter - продолжить, exit - прервать")
check = input('> ')
if check == 'exit':
    sys.exit()
eternal_counter = 0
counter = len(all_groups)
print("Предварительная обработка целевых сообществ займёт некоторое время. Ожидайте.")
for group in all_groups:
    group_id = group['_id']
    """Получаю рандомный токен"""
    token_index = tokens.token(tokens_list, preview)
    token = tokens_list[int(token_index)]
    preview = token_index
    exp[token_index] += 1
    response = api.wall_get(group_id, token)
    for post in response:
        post_id = post["id"]
        from_id = post["from_id"]
        posting_time = post["date"]
        post_text = post["text"]
        comments_count = post["comments"]["count"]
        post_link = "https://vk.com/public" + str(group_id) + "?w=wall-" + str(group_id) + "_" + str(post_id)
        print(response)