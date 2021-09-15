import requests
import  db
import time
import functions

# Получение ответа методом excecute
def execute(code, token, version):
    url = "https://api.vk.com/method/execute?"
    data = dict(code=code, access_token=token, v=version)
    resp = requests.post(url=url, data=data)
    return resp.json()


# Получение списка методом excecute
def execute_list(code, token, version):
    url = "https://api.vk.com/method/execute?"
    data = dict(code=code, access_token=token, v=version)
    resp = requests.post(url=url, data=data)
    list = resp.json()
    return list['response'][0]['items']


# Поиск сообществ по запросу в конкретном городе
def groups_search(token, query, offset, city, country):
    community_type = ''
    fields = 'members_count, description'
    market = ''
    sort = ''
    version = '5.126'
    response = requests.get('https://api.vk.com/method/groups.search',
                            params={'access_token': token,
                                    'q': query,
                                    'city_id': city,
                                    'country_id': country,
                                    'type': community_type,
                                    'market': market,
                                    'fields': fields,
                                    'sort': sort,
                                    'v': version,
                                    'count': 1000,
                                    'offset': offset
                                    }
                            )
    return response.json()


# Поиск сообществ по запросу
def groups_search_empty(token, query, offset):
    community_type = ''
    fields = 'members_count, description'
    market = ''
    sort = ''
    version = '5.126'
    response = requests.get('https://api.vk.com/method/groups.search',
                            params={'access_token': token,
                                    'q': query,
                                    'type': community_type,
                                    'market': market,
                                    'fields': fields,
                                    'sort': sort,
                                    'v': version,
                                    'count': 1000,
                                    'offset': offset
                                    }
                            )
    return response.json()


# Получение информации о сообществе
def groups_get_by_id(token, id):
    fields = 'status,can_see_all_posts,can_post,description,members_count'
    version = '5.61'
    response = requests.get('https://api.vk.com/method/groups.getById',
                            params={'access_token': token,
                                    'group_id': id,
                                    'v': version,
                                    'fields': fields
                                    }
                            )
    return response.json()


# Получение стандартного ответа api get.Members
def groups_get_members(group_id, offset, token):
    try:
        fields = 'last_seen,sex,bdate,city,country,contacts,site,status'
        version = '5.61'
        response = requests.get('https://api.vk.com/method/groups.getMembers',
                                params={'access_token': token,
                                        'offset': offset,
                                        'group_id': group_id,
                                        'v': version,
                                        'fields': fields
                                        }
                                )
        object = response.json()
        return object['response']
    except Exception:
        return False


# Получение списка пользователей
def groups_get_members_list(group_id, offset, token):
    try:
        fields = 'sex,bdate,city,country,contacts,site,status'
        version = '5.61'
        response = requests.get('https://api.vk.com/method/groups.getMembers',
                                params={'access_token': token,
                                        'offset': offset,
                                        'group_id': group_id,
                                        'v': version,
                                        'fields': fields
                                        }
                                )
        object = response.json()
        return object['response']['items']
    except Exception:
        return False


# Получение количества пользователей
def groups_get_members_count(group_id, offset, token):
    try:
        version = '5.61'
        response = requests.get('https://api.vk.com/method/groups.getMembers',
                                params={'access_token': token,
                                        'count': 0,
                                        'offset': offset,
                                        'group_id': group_id,
                                        'v': version
                                        }
                                )
        object = response.json()
        return object['response']['count']
    except Exception:
        return False


def friends_get(user_id, offset, token):
    try:
        version = '5.61'
        fields = 'sex,bdate,city,country,contacts,site,status'
        response = requests.get('https://api.vk.com/method/friends.get',
                                params={'access_token': token,
                                        'count': 5000,
                                        'offset': offset,
                                        'user_id': user_id,
                                        'fields': fields,
                                        'v': version
                                        }
                                )
        object = response.json()
        return object['response']['items']
    except Exception:
        return False


def wall_get(group_id, token):
    try:
        version = '5.84'
        owner_id = '-' + str(group_id)
        fields = 'sex,bdate,city,country,contacts,site,status'
        response = requests.get('https://api.vk.com/method/wall.get',
                                params={'access_token': token,
                                        'owner_id': owner_id,
                                        'count': 100,
                                        'filter': all,
                                        'extended': 1,
                                        'fields': fields,
                                        'v': version
                                        }
                                )
        object = response.json()
        return object['response']['items']
    except Exception:
        return False
