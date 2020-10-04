#!/usr/bin/env python

import subprocess
import sys
import os
import hashlib


# Строим хранилище объектов. Напишите программу, которая по заданному пути на файловой системе находит все одинаковые файлы и заменяет их на хардлинки.

# python3 scr.py dir_name par_1
# python3 scr.py examples find
# python3 scr.py examples replace


try:
	dir_name = sys.argv[1]
	par_1 = sys.argv[2]
except (NameError, IndexError):
	raise NameError('Укажите аргумент')

def get_files(dir_name):
	ls = subprocess.check_output(["ls", dir_name]).decode("utf-8")
	files = ls.split("\n")
	files.pop()
	return files


def get_path(dir_name, file):
	partial = file.lstrip("/")
	path = os.path.join(dir_name, partial)
	return path


def get_paths(dir_name, files):
	paths = []
	for file in files:
		path = get_path(dir_name, file)
		paths.append(path)

	return paths


def md5(file):
    hash_md5 = hashlib.md5()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()	


def get_hashes(paths):
	files_hashes = []
	for path in paths:
		gh = md5(path)
		files_hashes.append(gh)
	return files_hashes

def get_zip(paths, hashes):
	res = dict(zip(paths, hashes))
	return res

def find_same(zip_dict):
	# could be many dicts
	rev_multidict = {}
	for key, value in zip_dict.items():
		rev_multidict.setdefault(value, set()).add(key)
		res = [values for key, values in rev_multidict.items() if len(values) > 1]
	return res

def delete_copies(original_dict):
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
				os.remove(value)
				os.link(last_elements[el_id], value)
				original_dict[el_id].remove(value)
				print(value, 'replaced by hardlink')
	return original_dict



if par_1 == 'mds':
	# get a list hashes of files in dir
	p = get_paths(dir_name, get_files(dir_name))
	print(get_hashes(p))

elif par_1 == 'zip':
	# get a dict of names:hashes of files in dir
	p = get_paths(dir_name, get_files(dir_name))
	h = get_hashes(p)
	print(get_zip(p,h))

elif par_1 == 'find':
	# get a dict of copies of files in dir
	p = get_paths(dir_name, get_files(dir_name))
	h = get_hashes(p)
	z = get_zip(p,h)
	print(find_same(z))

elif par_1 == 'replace':
	# replace copies with hardlinks
	p = get_paths(dir_name, get_files(dir_name))
	h = get_hashes(p)
	z = get_zip(p,h)
	f = find_same(z)
	delete_copies(f)

elif par_1 == 'ls':
	# get a list of files in a dir
	print(get_files(dir_name))

elif par_1 == 'paths':
	# get a list of paths in a dir
	print(get_paths(dir_name, get_files(dir_name)))
