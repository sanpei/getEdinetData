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
        shutil.rmtree(os.path.join(path, files_dir[0]))

def delete_file(path, file_name):
    files = os.listdir(path)
    files = [f for f in files if file_name in f]
    if files:
        print(True)
    # os.remove(path, file_name)

def get_yuho_text(title):
    if all((s in str(title)) for s in ['有価証券報告書', '株式会社']) and '受益証券' not in str(title):
        return True
    return False

def get_shihanki_text(title):
    if all((s in str(title)) for s in ['四半期報告書', '株式会社']) and '受益証券' not in str(title):
        return True
    return False