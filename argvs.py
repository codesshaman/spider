import files

"""Параметры в массиве:
No| Опция groupssearcher | Опция userssearcher
0 | C - страна           | C - страна
1 | c - id города        | c - id города
2 | c - название города  | c - название города
3 | id страны            | id страны
4 | q - запрос           | s - стартовый город
5 | p - население        | m - число участников
6 | t - токен            | t - токен
7 | k - keywords         | k - keywords
8 | s - стартовый город  |
"""


"""Создаёт пустой массив массивов"""
def argvs_comp(number):
    # Заполнение (completion) массива
    # аргументов пустыми значениями
    array = []
    for index in range(0, number):
        array.append([])
    return array


"""Выводит количество аргументов заданного флага"""
def argvs_number(arguments, value):
    length = 0
    arg_string = (' '.join(map(str, arguments)))
    arg_string = arg_string[1:]
    arr_string = arg_string.split('-')
    for arr in arr_string:
        arr = arr.strip()
        array = arr.split(' ')
        flag = array[0]
        values = array[1:]
        if flag == value:
            length = len(values)
    if length == 0:
        return 0
    else:
        return int(length)


"""Выводит список аргументов заданного флага"""
def argv_split(arguments, value):
    arg_string = (' '.join(map(str, arguments)))
    arg_string = arg_string[1:]
    arr_string = arg_string.split('-')
    for arr in arr_string:
        arr = arr.strip()
        array = arr.split(' ')
        flag = array[0]
        values = array[1:]
        if flag == value:
            return values


"""Исправляет значения ключевых слов"""
def keywords_proc(arguments, value):
    arg_string = (' '.join(map(str, arguments)))
    arg_string = arg_string[1:]
    arr_string = arg_string.split('-')
    title_arr = []
    for arr in arr_string:
        arr = arr.strip()
        array = arr.split(' ')
        flag = array[0]
        values = array[1:]
        if flag == value:
            for val in values:
                title_arr.append(val.title())
    return title_arr


"""Исправляет значения городов"""
def cities_correct(arguments):
    json_file = files.open_json('cities.json')
    arr = argv_split(arguments, 'c')
    new_arr = []
    for city_input in arr:
        city = city_input.title()
        if city.isdigit():
            new_arr.append(int(city))
        else:
            for element in json_file:
                if element['city'] == city:
                    new_arr.append(int(element['_id']))
    return list(set(new_arr))


"""Возвращает город по идентификатору"""
def citi_name_by_id(arguments):
    array = cities_correct(arguments)
    json_file = files.open_json('cities.json')
    new_arr = []
    for city in array:
        for element in json_file:
            if element['_id'] == city:
                new_arr.append(element['city'])
    return new_arr


"""Город по идентификатору из массива"""
def citi_name_by_id_array(array):
    json_file = files.open_json('cities.json')
    new_arr = []
    for city in array:
        for element in json_file:
            if element['_id'] == city:
                new_arr.append(element['city'])
    return new_arr


"""Возвращает идентификатор по названию города"""
def citi_id_by_name(arguments):
    json_file = files.open_json('cities.json')
    new_arr = []
    for city in arguments:
        for element in json_file:
            if element['city'] == city:
                new_arr.append(int(element['_id']))
    return new_arr


"""Возвращает страну по идентификатору города"""
def country_by_city(arguments):
    array = cities_correct(arguments)
    json_file = files.open_json('cities.json')
    new_arr = []
    for city in array:
        for element in json_file:
            if element['_id'] == city:
                new_arr.append(int(element['country']))
    return new_arr


"""Страна по идентификатору города из массива"""
def country_by_city_array(array):
    json_file = files.open_json('cities.json')
    new_arr = []
    for city in array:
        for element in json_file:
            if element['_id'] == city:
                new_arr.append(int(element['country']))
    return new_arr


"""Обрабатывает страну"""
def country_proc(array):
    new_arr = []
    for country in array:
        if country.isdigit():
            new_arr.append(int(country))
        else:
            if country == 'Россия':
                new_arr.append(int('1'))
            if country == 'РФ':
                new_arr.append(int('1'))
            if country == 'рф':
                new_arr.append(int('1'))
            if country == 'укр':
                new_arr.append(int('2'))
            if country == 'УКР':
                new_arr.append(int('2'))
            if country == 'Укр':
                new_arr.append(int('2'))
            if country == 'Украина':
                new_arr.append(int('2'))
            if country == 'РБ':
                new_arr.append(int('3'))
            if country == 'Бел':
                new_arr.append(int('3'))
            if country == 'бел':
                new_arr.append(int('3'))
            if country == 'Белоруссия':
                new_arr.append(int('3'))
            if country == 'Беларусь':
                new_arr.append(int('3'))
            if country == 'КЗ':
                new_arr.append(int('4'))
            if country == 'кз':
                new_arr.append(int('4'))
            if country == 'Казахстан':
                new_arr.append(int('4'))
    return list(set(new_arr))


"""Обрабатывает число жителей"""
def population_proc(arguments):
    population_arr = []
    population = argv_split(arguments, 'p')
    pop = population[0]
    if pop.isdigit():
        population_arr.append(int(pop))
    else:
        population_arr.append(1000000)
    return population_arr


"""Обрабатывает число пользователей"""
def members_proc(arguments):
    members_arr = []
    members = argv_split(arguments, 'm')
    pop = members[0]
    if pop.isdigit():
        members_arr.append(int(pop))
    else:
        members_arr.append(100000)
    return members_arr


"""Выводит города по числу жителей"""
def population_cities(arguments):
    values = argv_split(arguments, 'C')
    countries = country_proc(values)
    population = population_proc(arguments)[0]
    json_file = files.open_json('cities.json')
    new_arr = []
    for country in countries:
        for element in json_file:
            if element['country'] == country:
                if element['population'] >= population:
                    new_arr.append(int(element['_id']))
    return new_arr


"""Выводит все города в базе по стране"""
def all_cities(arguments):
    values = argv_split(arguments, 'C')
    countries = country_proc(values)
    json_file = files.open_json('cities.json')
    new_arr = []
    for country in countries:
        for element in json_file:
            if element['country'] == country:
                new_arr.append(int(element['_id']))
    return new_arr


"""Определяет стартовый город, с которого
начинается перебор городов"""
def start_city(arguments, city_names, city_ids):
    value_arr = argv_split(arguments, 's')
    value = value_arr[0]
    counter = 0
    if value.isdigit():
        if value not in city_ids:
            print("Стартовый город отсутствует в списке!")
            exit()
        else:
            for city_id in city_ids:
                if city_id != value:
                    counter += 1
                else:
                    break
            del city_names[0:counter]
            del city_ids[0:counter]
            searching_city = city_ids[0]
    else:
        if value not in city_names:
            print("Стартовый город отсутствует в списке!")
            exit()
        else:
            for city_name in city_names:
                if city_name != value:
                    counter += 1
                else:
                    break
            del city_names[0:counter]
            del city_ids[0:counter]
            searching_city = city_ids[0]
    return [searching_city, city_ids, city_names]


"""Формирует список атрибутов,
полученных в командной строке
для поиска целевых сообществ"""
def argv_proc_gs(arguments):
    values_array = argvs_comp(9)
    if argvs_number(arguments, 'C') != 0:
        countries = argv_split(arguments, 'C')
        values_array[0] = country_proc(countries)
        values_array[1] = all_cities(arguments)
        values_array[2] = citi_name_by_id_array(values_array[1])
        values_array[3] = country_by_city_array(values_array[1])
    if argvs_number(arguments, 'c') != 0:
        values_array[3] = country_by_city(arguments)
        values_array[2] = citi_name_by_id(arguments)
        values_array[1] = citi_id_by_name(values_array[2])
    if argvs_number(arguments, 'c') == 0 and argvs_number(arguments, 'C') == 0:
        values_array[1] = [1,2,49,60,99,123,158,151,73,110,119,95,104,10,42,314,280,292,650,282,183,14]
        values_array[2] = ['Москва', 'Санкт-Петербург', 'Екатеринбург', 'Казань', 'Новосибирск', 'Самара', 'Челябинск',
                         'Уфа', 'Красноярск', 'Пермь', 'Ростов-на-Дону', 'Нижний Новгород', 'Омск', 'Волгоград',
                         'Воронеж', 'Киев', 'Харьков', 'Одесса', 'Днепропетровск', 'Минск', 'Алма-Ата', 'Астана']
        values_array[3] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 4, 4]
    if argvs_number(arguments, 'q') != 0:
        values_array[4] = argv_split(arguments, 'q')
    if argvs_number(arguments, 'q') == 0:
        values_array[4] = ['SMM', 'Маркетинг']
    if argvs_number(arguments, 'p') != 0:
        values_array[5] = population_proc(arguments)
        if argvs_number(arguments, 'C') != 0:
            values_array[1] = population_cities(arguments)
            values_array[2] = citi_name_by_id_array(values_array[1])
            values_array[3] = country_by_city_array(values_array[1])
    if argvs_number(arguments, 't') != 0:
        values_array[6] = argv_split(arguments, 't')
    if argvs_number(arguments, 't') == 0:
        values_array[6] = ['file', 'tokensfile.txt']
    if argvs_number(arguments, 'k') != 0:
        values_array[7] = keywords_proc(arguments, 'k')
    if argvs_number(arguments, 's') != 0:
        values_array[8] = start_city(arguments, values_array[2], values_array[1])
        values_array[2] = values_array[8].pop()
        values_array[1] = values_array[8].pop()
    return values_array


"""Формирует список атрибутов,
полученных в командной строке
для парсинга участников сообществ"""
def argv_proc_us(arguments, campaings):
    values_array = argvs_comp(8)
    if argvs_number(arguments, 'C') != 0:
        countries = argv_split(arguments, 'C')
        values_array[0] = country_proc(countries)
    if argvs_number(arguments, 'c') != 0:
        values_array[3] = country_by_city(arguments)
        values_array[2] = citi_name_by_id(arguments)
        values_array[1] = citi_id_by_name(values_array[2])
    values_array[4] = campaings
    if argvs_number(arguments, 'm') != 0:
        values_array[5] = members_proc(arguments)
    if argvs_number(arguments, 't') != 0:
        values_array[6] = argv_split(arguments, 't')
    if argvs_number(arguments, 't') == 0:
        values_array[6] = ['file', 'tokensfile.txt']
    if argvs_number(arguments, 'k') != 0:
        values_array[7] = keywords_proc(arguments, 'k')
    return values_array