#!/usr/bin/env python
# -*- coding: utf-8 -*-
import db
import os
import xlsxwriter
home = os.getenv("HOME")

# Создаю файл
cityname = input("Введите название города:")
path = 'Документы/XLS_Writer'
writefile = xlsxwriter.Workbook(home + '/' + path + '/filename.xlsx')
worksheet = writefile.add_worksheet()
connect = db.connect()
array = db.array(connect, "db_name", "users", "city_name", cityname)
print(len(array))
selection = []
for user in array:
    if user["communitys_counter"] > 20:
        selection.append(user)
print(len(selection))
string_counter = 0
for user in selection:
    worksheet.write_url(string_counter, 0, 'https://vk.com/id' + str(user['_id']))
    worksheet.write(string_counter, 1, user['name'])
    worksheet.write(string_counter, 2, user['last_name'])
    if user["sex"] == 1:
        worksheet.write(string_counter, 3, "Ж")
    if user["sex"] == 2:
        worksheet.write(string_counter, 3, "М")
    worksheet.write(string_counter, 4, user['city_name'])
    worksheet.write(string_counter, 5, user['communitys_counter'])
    worksheet.write(string_counter, 6, ', '.join(user['keywords']))
    worksheet.write(string_counter, 7, ', '.join(user['campaings']))
    communitys_counter = 8
    for community in user['communitys']:
        worksheet.write_url(string_counter, communitys_counter, 'https://vk.com/public' + str(community))
        communitys_counter += 1
    string_counter += 1
writefile.close()