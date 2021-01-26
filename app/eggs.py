import os
import io
import time
import requests
import pandas as pd
from tqdm import tqdm
from zipfile import ZipFile
import logging

import settings
import utils

logger = logging.getLogger(__name__)

class Downloader(object):

    '''
        XBRLファイルを一括ダウンロード
    '''

    def __init__(self):
        self.base_path = os.getcwd()

    def __get_file_list(self):
        file_list = []
        file_name = f'{utils.get_file_name(settings.download_file_name)}.csv'
        file_list.append(file_name)
        return file_list

    def __make_directory(self, dir_path):
        os.makedirs(dir_path, exist_ok=True)

    def __download_and_unzip(self, url, ir_path):
        count = 0
        retry = 3

        while True:
            rsp = requests.get(url, params={'type': 1})
            time.sleep(3)
            if rsp.status_code == 200:
                z = ZipFile(io.BytesIO(rsp.content))
                z.extractall(ir_path)
                break
            else:
                logger.info(f'error= download failed {count}: {url}')
                if count < retry:
                    count += 1
                    continue
                else:
                    raise

    def __download_xbrl_file(self, info_dicts, dir_path):
        for no in tqdm(info_dicts):
            info_dict = info_dicts[no]
            company_path = f'{dir_path}{info_dict["code"]}/'
            ir_path = f'{company_path}{info_dict["id"]}'
            self.__make_directory(company_path)
            self.__make_directory(ir_path)
            self.__download_and_unzip(info_dict['url'], ir_path)
            no += 1

    def __download_all_xbrl_files(self, info_df, dir_path):
        count = 0
        mp_dict = {}
        for index, row in info_df.iterrows():
            mp_dict[count] = row.to_dict()
            count += 1
        self.__download_xbrl_file(mp_dict, dir_path)

    def download(self):

        utils.delete_dir(self.base_path)

        list_dat_csv = self.__get_file_list()
        if not list_dat_csv:
            return

        for dat_csv in list_dat_csv:
            info_df = pd.read_csv(os.path.join(self.base_path, dat_csv), parse_dates=['update'])
            if len(info_df) > 0:
                dir_path = f'{self.base_path}/{settings.xbrl_dir_name}{dat_csv.replace(".csv","").replace(settings.download_file_name,"")}/'
                self.__make_directory(dir_path)
                self.__download_all_xbrl_files(info_df, dir_path)
