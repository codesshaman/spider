import db
import api
import sys
import time
import functions
import threading


class UsersGet(threading.Thread):
    def __init__(self, connect, name, num, threads, count, repeats, token, group_id, campaing, keyword):
        threading.Thread.__init__(self)
        print(name + " запущен!")
        self.connect = connect  # объект соединения
        self.name = name  # Имя потока
        self.num = num  # Номер потока
        self.trd = threads  # Количество потоков
        self.count = count  # Число пользователей
        self.rep = repeats  # Число повторений
        self.tkn = token  # Токен доступа
        self.id = group_id  # ИД сообщества
        self.camp = campaing  # Имя кампании
        self.kwd = keyword    # ключевое слово

    def run(self):
        # Сначала подсчитываем количество запросов
        array = []  # Массив для записи всех смещений
        skip = self.trd * 1000  # Столько нужно пропустить
        for i in range(self.rep):
            offset = i * skip + self.num * 1000
            if offset < self.count:
                array.append(offset)
        print(array)
        for i in range(len(array)):
            print(self.name + ": парсинг пользователей")
            max_pars = offset + 1000
            print("Парсинг " + str(offset) + '-' + str(max_pars) + " из " + str(self.count) + " пользователей")
            update_list = []
            insert_list = []
            offset = array[i]  # Получаем текущее смещение
            # Делаем запрос
            users = api.groups_get_members_list(self.id, offset, self.tkn)
            unixtime = int(time.time())
            for user in users:
                save_check = functions.users_save_check(self.connect, user, unixtime, self.camp, self.kwd, self.id)
                if save_check:
                    if save_check[0] == 0:
                        insert_list.append(save_check[2])
                    if save_check[0] == 1:
                        update_list.append(save_check[2])
            if len(insert_list) > 0:
                data = db.inserts(self.connect, 'db_name', 'users', insert_list)
                print('Добавлено ' + str(len(insert_list)) + ' пользователей')
                print(data)
            if len(update_list) > 0:
                print("Обновлено " + str(len(update_list)) + " пользователей")
            time.sleep(1)
        sys.exit()


def create_get_users(connect, group_id, members_count, tokens_list, campaing, keyword, exp):
    # Определяем число потоков
    trd = len(tokens_list)
    # Получаем количество запросов
    divider = (members_count - 1) // 1000
    if divider <= trd:
        threads = divider + 1
        repeats = 2
        if trd - divider >= 1:
            repeats = 1
    else:
        # получаем количество запросов от каждого токена
        repeats = divider // trd + 1
        threads = trd
    for num in range(threads):
        # Получаем токен
        token = tokens_list[num - 1]
        name = "Поток #%s" % (num + 1)
        exp[num - 1] += repeats
        users_thread = UsersGet(connect, name, num, threads, members_count, repeats,
                                token, group_id, campaing, keyword)
        users_thread.start()
        print("Парсинг всех потоков окончен!")
    return exp


def threads_start(connect, group_id, members_count, tokens_list, campaing, keyword, exp):
    new_exp = create_get_users(connect, group_id, members_count, tokens_list, campaing, keyword, exp)
    return new_exp