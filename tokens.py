import os
import random
import files
import crypto


def tokens_settings(data):
    tokens_list = []
    if len(data[6]) > 1:
        if data[6][0] == 'file':
            file = data[6][1]
            path = os.getcwd() + "/" + file
            password = files.config('settings.conf', 'token_pass')
            token_list = files.read_to_list(path)
            for token in token_list:
                tkn = crypto.get_decode(token, password)
                tokens_list.append(tkn)
            return tokens_list
        if data[6][0][0] == 'cmd':
            tokens_list = data[6][0][1:]
            return tokens_list
    else:
        print('Token is empty!')


def token(list, prew):
    length = len(list) - 1
    index = random.randint(0, length)
    counter = True
    while counter:
        if index == prew:
            counter = True
            index = random.randint(0, length)
        else:
            counter = False
    return index


def expenditure(list):
    exp = []
    for i in list:
        exp.append(0)
    return exp