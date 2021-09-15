#!/usr/bin/env python
# -*- coding: utf-8 -*-
# GroupsSearcher script
"""Импортирую всё необходимое
-----------------------------"""
import db
import api
import sys
import time
import argvs
import files
import tokens
import functions

"""Подключаюсь к базе данных
----------------------------"""
connect = db.connect()
""" Получаю номер сессии
________________________"""
session_isset = True
session_number = 0
while session_isset == True:
    session_number += 1
    session_check = db.check(connect, 'db_name', 'communitys', 'session', session_number)
    if session_check == 0:
        session_isset = False
""" Обрабатываю параметры командной строки
------------------------------------------"""
arguments = sys.argv
distr = argvs.argv_proc_gs(arguments)
"""Обрабатываю список токенов
-----------------------------"""
tokens_list = tokens.tokens_settings(distr)
preview = 0
exp = tokens.expenditure(tokens_list)
"""Выбираю рекламную кампанию
-----------------------------"""
company = db.campaing(connect)
length = len(company)
counter = 0
for camp in company:
    counter += 1
    print(str(counter) + ' - ' + camp)
print('Выберите кампанию: 1 - ' + str(length))
company_number = input('> ')
if company_number.isdigit():
    num = int(company_number)
    company_name = company[num - 1]
    company_name = company_name.split()
    company_name = company_name[0][:-1]
    print(company_name)
else:
    print('Введите целое число от 1 до ' + str(counter))
    quit()
"""Обрабатываю список ключевых слов
-----------------------------------"""
keywords = distr[7]
try:
    keyword = keywords[0].title()
except IndexError:
    print('Введите ключевые слова')
    quit()
"""Получаю список запросов и города
-----------------------------------"""
query_index = 0
querys = distr[4]
cities = distr[1]
cityes_names = distr[2]
countries = distr[3]
min = int(files.config('settings.conf', 'members'))
auto = False
"""Перебираю все запросы в основном цикле
-----------------------------------------"""
for q in range(len(querys)):
    query = querys[query_index]
    try:
        keyword = keywords[query_index]
    except IndexError:
        keyword = keywords[0]
    print('Обрабатывается запрос: "' + str(query) + '"')
    print('Ключевое слово: "' + str(query) + '"')
    query_index += 1
    city_index = 0
    """Перебираю все города в вложенном цикле
    -----------------------------------------"""
    print("Осуществляется поиск в следующих городах:")
    print(cityes_names)
    city_counter = 0
    for city in cities:
        city_name = cityes_names[city_counter]
        country = countries[city_counter]
        if auto == False:
            print('Выполнить поиск в городе ' + city_name + "? y/n (n - next city)")
            answer = input('> ')
        if auto == True:
            answer = 'y'
        city_counter += 1
        if answer == 'n':
            print("Перехожу к следующему городу")
        if answer == 'auto':
            auto = True
        if answer != 'n' and answer != 'exit':
            query_list = []
            """************************************************"""
            """******************Цикл запросов*****************"""
            """************************************************"""
            """Обрабатываю все группы из данного города"""
            all_groups = db.data(connect, "db_name", "communitys", 'city', city)
            existing_ids = []
            for existing_group in all_groups:
                existing_ids.append(existing_group['_id'])
            all_groups = []
            """Получаю рандомный токен"""
            token_index = tokens.token(tokens_list, preview)
            token = tokens_list[int(token_index)]
            preview = token_index
            exp[token_index] += 1
            resp = api.groups_search(token, query, 0, city, distr[3])
            check = resp.get('error')  # Проверяю наличие ошибок
            if check == None:  # Если их нет, начинаю цикл
                items = resp['response']['items']
                for item in items:  # Обрабатываю все сообщества
                    group_id = item['id']
                    if 'members_count' in item:
                        members_count = item['members_count']
                        if min < members_count:
                            if group_id not in existing_ids:
                                query_list.append(item)
                            else:
                                print('Сообщество "' + item["name"] + '" уже есть в базе данных!')
            print("Расходование токенов:")
            print(exp)
            all = str(len(query_list))
            print("В городе " + city_name + " найдено " + all + " подходящих групп по запросу " + query)
            if not auto:
                check = input("> ")
            print("Начинаю обработку найденных сообществ!")
            if check == 'exit':
                print("Расходование токенов:")
                print(exp)
                sys.exit()
            if int(all) > 0:
                cycle_rolling = True
            if int(all) == 0:
                cycle_rolling = False
            counter = 0
            while cycle_rolling:
                community = query_list[counter]
                counter += 1
                id = community['id']
                print(str(counter) + " Адрес:     https://vk.com/public" + str(community['id']))
                print("Название:    | " + community['name'])
                print("Участников:  | " + str(community['members_count']))
                print("Вывести детальную информацию о сообществе? y/n")
                save_check = input('> ')
                if (save_check == '' or save_check == 'y' or save_check == 'yes'):
                    unixtime = int(time.time())
                    """Получаю рандомный токен"""
                    token_index = tokens.token(tokens_list, preview)
                    token = tokens_list[int(token_index)]
                    preview = token_index
                    exp[token_index] += 1
                    response = api.groups_get_by_id(token, id)
                    item = response['response'][0]
                    functions.print_community(item)
                    print("Сохранить сообщество в базу? y/n")
                    save_check = input('> ')
                    if (save_check == '' or save_check == 'y' or save_check == 'yes'):
                        community_check = db.check(connect, 'db_name', 'communitys', '_id', id)
                        if community_check == 0:
                            functions.add_community(connect, item, session_number, keyword, city,
                                                    city_name, country, unixtime, company_name)
                        if community_check == 1:
                            functions.update_community(connect, item, unixtime, company_name, keyword)
                        print("Расходование токенов:")
                        print(exp)
                    else:
                        print("Пропускаю сообщество!")
                    if save_check == 'back':
                        counter -= 2
                    if save_check == 'next':
                        cycle_rolling = False
                    if save_check == 'exit':
                        print("Расходование токенов:")
                        print(exp)
                        sys.exit()
                if save_check == 'back':
                    counter -= 2
                if save_check == 'next':
                    cycle_rolling = False
                if save_check == 'exit':
                    print("Расходование токенов:")
                    print(exp)
                    sys.exit()
                if counter == int(all):
                    print("Все выбранные сообщества в городе " + city_name + " успешно сохранены!")
                    cycle_rolling = False
        if answer == 'exit':
            print("Расходование токенов:")
            print(exp)
            sys.exit()
        print("Расходование токенов:")
        print(exp)
        print("Перехожу к следующему городу")
        """************************************************"""
        """*******************Конец цикла******************"""
        """************************************************"""
    """____________________________________________________________________"""
    answer = input("Все города сохранены. Начать поиск сообществ без указания города y/n?")
    if (answer == '' or answer == 'y' or answer == 'yes'):
        auto = True
        city = 0
        city_name = None
        country = 0
        counter = 0
        all_groups = db.array(connect, "db_name", "communitys", 'keywords', keyword)
        existing_ids = []
        for existing_group in all_groups:
            existing_ids.append(existing_group['_id'])
        """Получаю рандомный токен"""
        token_index = tokens.token(tokens_list, preview)
        token = tokens_list[int(token_index)]
        preview = token_index
        exp[token_index] += 1
        response = api.groups_search_empty(token, query, 0)
        check = response.get('error')  # Проверяю наличие ошибок
        if check == None:  # Если их нет, начинаю цикл
            groups_count = response["response"]["count"]
            query_list = []
            if groups_count > 1000:
                offset_counter = (groups_count // 1000) + 1
            else:
                offset_counter = 0
            groups = response["response"]["items"]
            for group in groups: # Обрабатываю все сообщества
                group_id = group['id']
                if 'members_count' in group:
                    members_count = group['members_count']
                    if min < members_count:
                        if group_id not in existing_ids:
                            query_list.append(group)
                        else:
                            print('Сообщество "' + group["name"] + '" уже есть в базе данных!')
            all = str(len(query_list))
            print("Найдено " + all + " подходящих групп по запросу " + query)
            if not auto:
                check = input("> ")
            print("Начинаю обработку найденных сообществ!")
            if check == 'exit':
                print("Расходование токенов:")
                print(exp)
                sys.exit()
            if int(all) > 0:
                cycle_rolling = True
            if int(all) == 0:
                cycle_rolling = False
            while cycle_rolling:
                community = query_list[counter]
                counter += 1
                id = community['id']
                print(str(counter) + " Адрес:     https://vk.com/public" + str(community['id']))
                print("Название:    | " + community['name'])
                print("Участников:  | " + str(community['members_count']))
                print("Вывести детальную информацию о сообществе? y/n")
                save_check = input('> ')
                if (save_check == '' or save_check == 'y' or save_check == 'yes'):
                    unixtime = int(time.time())
                    """Получаю рандомный токен"""
                    token_index = tokens.token(tokens_list, preview)
                    token = tokens_list[int(token_index)]
                    preview = token_index
                    exp[token_index] += 1
                    response = api.groups_get_by_id(token, id)
                    item = response['response'][0]
                    functions.print_community(item)
                    print("Сохранить сообщество в базу? y/n")
                    save_check = input('> ')
                    if (save_check == '' or save_check == 'y' or save_check == 'yes'):
                        community_check = db.check(connect, 'db_name', 'communitys', '_id', id)
                        if community_check == 0:
                            functions.add_community(connect, item, session_number, keyword, city,
                                                    city_name, country, unixtime, company_name)
                        if community_check == 1:
                            functions.update_community(connect, item, unixtime, company_name, keyword)
                        print("Расходование токенов:")
                        print(exp)
                    else:
                        print("Пропускаю сообщество!")
                    if save_check == 'back':
                        counter -= 2
                    if save_check == 'next':
                        cycle_rolling = False
                    if save_check == 'exit':
                        print("Расходование токенов:")
                        print(exp)
                        sys.exit()
                if save_check == 'back':
                    counter -= 2
                if save_check == 'next':
                    cycle_rolling = False
                if save_check == 'exit':
                    print("Расходование токенов:")
                    print(exp)
                    sys.exit()
                if counter == int(all):
                    print("Все выбранные сообщества успешно сохранены!")
                    cycle_rolling = False
    print("Перехожу к следующему запросу")
print("Все интересующие Вас сообщества сохранены!")