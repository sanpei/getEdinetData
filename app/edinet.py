import logging
import urllib3
from urllib3.exceptions import InsecureRequestWarning
import time
import requests
import json
import os
import csv
from datetime import timedelta

import settings
import utils

logger = logging.getLogger(__name__)

class Catcher(object):

    '''
        対象Jsonファイルを取得するためのURL一覧を取得する
    '''

    def __init__(self):
        self.csv_tag = ['id', 'title', 'url', 'code', 'update', 'period_start', 'period_end']
        self.encode_type = 'utf-8'
        self.file_name = f'{utils.get_file_name(settings.download_file_name)}.csv'
        self.base_path = f'{utils.get_base_path()}'
        urllib3.disable_warnings(InsecureRequestWarning)

    def get_yuho_text(self, title):
        if all((s in str(title)) for s in ['有価証券報告書', '株式会社']) and '受益証券' not in str(title):
            return True
        return False

    def get_shihanki_text(self, title):
        if all((s in str(title)) for s in ['四半期', '株式会社']) and '受益証券' not in str(title):
            return True
        return False

    def get_link_info_str(self, str_date):

        url = settings.base_url
        params = {"date": str_date, "type": 2}

        count = 0
        retry = 3

        while True:
            try:
                resp = requests.get(f'{url}.json', params=params, verify=False)
                return resp.text
            except Exception as e:
                if count <= retry:
                    count += 1
                    continue
                logging.error(f'action=catcher error={e}')
                raise

    def get_link(self, target_list):
        edinet_dict = {}

        for target_dict in target_list:

            title = f'{target_dict["filerName"]} {target_dict["docDescription"]}'

            # if not self.get_yuho_text(title):
            #     continue

            if not self.get_shihanki_text(title):
                continue

            docID = target_dict['docID']
            id_url = f'{settings.base_url}/{docID}'
            edinet_code = target_dict['edinetCode']
            updated = target_dict['submitDateTime']
            period_start = target_dict['periodStart']
            period_end = target_dict['periodEnd']
            edinet_dict[docID] = {'id': docID, 'title': title, 'url': id_url, 'code': edinet_code, 'update': updated,
                                  'period_start': period_start, 'period_end': period_end}

        return edinet_dict

    def __json_parse(self, str):
        rec_dict = json.loads(str)

        if rec_dict['metadata']['status'] == '400':
            logger.info(f'action= info=not get contents')
            return None
        return rec_dict['results']

    def dump_file(self, result_dict):
        with open(os.path.join(self.base_path, self.file_name), 'w', encoding=self.encode_type) as of:
            writer = csv.DictWriter(of, self.csv_tag, lineterminator='\n')
            writer.writeheader()

            for key in result_dict:
                writer.writerow(result_dict[key])

    def create_xbrl_url_json(self):
        result_dict = {}
        target_date = utils.str_to_date(settings.since)

        count = 0

        while True:
            response_string = self.get_link_info_str(utils.date_to_str(target_date))
            target_list = self.__json_parse(response_string)
            if not target_list:
                target_date = target_date + timedelta(days=1)
                continue

            info_dict = self.get_link(target_list)
            result_dict.update(info_dict)

            time.sleep(1)
            target_date = target_date + timedelta(days=1)
            count += 1
            logger.info(f'action=create_xbrl_url_json count={count}')

            if target_date >= utils.str_to_date(settings.until):
                break

        utils.delete_file(self.base_path, settings.download_file_name)
        self.dump_file(result_dict)
