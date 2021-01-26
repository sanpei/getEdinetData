import os
import shutil
import datetime

import settings

def str_to_date(dtstr):
    return datetime.datetime.strptime(dtstr, '%Y-%m-%d')

def date_to_str(dt):
    return dt.strftime('%Y-%m-%d')

def get_base_path():
    return os.getcwd()

def get_file_name(str):
    return f'{str}{settings.since}'

def delete_dir(path):
    files = os.listdir(path)
    files_dir = [f for f in files if settings.xbrl_dir_name in f]
    if files_dir:
        print(True)
     # shutil.remove(path)


def delete_file(path, file_name):
    files = os.listdir(path)
    files = [f for f in files if file_name in f]
    if files:
        print(True)
    # os.remove(path, file_name)