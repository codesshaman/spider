import json


def readfile(path):
    file = open(path)
    content = file.read()
    file.close()
    return content


def read_to_list(path):
    lines = [line.rstrip('\n') for line in open(path)]
    return lines


def read_to_int_list(path):
    lines = [int(line.rstrip('\n')) for line in open(path)]
    return lines


def open_json(path):
    json_file = open(path, 'r', encoding='utf-8')
    json_content = json.load(json_file)
    json_file.close()
    return json_content


def config(path, setting):
    result = 'Опция "' + setting + '" отсутствует в файле ' + path
    settings = read_to_list(path)
    for line in settings:
        clean_line = line.strip()
        first = clean_line[0]
        if first != '#':
            args = clean_line.split('=')
            var = args[0].strip()
            val = args[1].strip()
            if var == setting:
                result = val
                break
    return result
