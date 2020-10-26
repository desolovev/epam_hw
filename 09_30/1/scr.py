#!/usr/bin/env python3

import sys
import hashlib
from os import listdir, remove, link
from os.path import isfile, join

# Строим хранилище объектов. Напишите программу, которая по заданному пути на файловой системе
# находит все одинаковые файлы и заменяет их на хардлинки.

# python3 scr.py dir_name func_name
# python3 scr.py examples find
# python3 scr.py examples replace


try:
    dir_name = sys.argv[1]
    command = sys.argv[2]
except (NameError, IndexError):
    raise NameError('Укажите аргумент')


def find_duplicates(dir):
    #
    # return a dictionary of duplicates (dict)
    #
    paths = []
    hashes = []
    files_list = [f for f in listdir(dir) if isfile(join(dir, f))]
    files_list.sort()
    for file in files_list:
        path = join(dir, file.lstrip("/"))
        paths.append(path)
    for path in paths:
        hash_md5 = hashlib.md5()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        hashes.append(hash_md5.hexdigest())
    zip_dict = dict(zip(paths, hashes))
    rev_multidict = {}
    for key, value in zip_dict.items():
        rev_multidict.setdefault(value, set()).add(key)
        duplicates_dict = [values for key, values in rev_multidict.items() if len(values) > 1]
    return duplicates_dict


def replace_duplicates(original_dict):
    #
    # function replaces duplicates with hardlinks
    #
    last_elements = []
    last_el = ''
    # find the last element of every dict
    for el in range(len(original_dict)):
        last_el = list(original_dict[el])
        last_elements.append(last_el[-1])
        original_dict[el] = list(original_dict[el])

    # replace with hardlinks
    for el_id in range(len(last_elements)):
        while len(original_dict[el_id]) > 1:
            for value in original_dict[el_id]:
                remove(value)
                link(last_elements[el_id], value)
                original_dict[el_id].remove(value)
                print(value, 'replaced by hardlink')
    return original_dict


if __name__ == '__main__':
    if command == 'find':
        # get a dict of copies of files in dir
        print(find_duplicates(dir_name))

    elif command == 'replace':
        # replace copies with hardlinks
        replace_duplicates(find_duplicates(dir_name))
