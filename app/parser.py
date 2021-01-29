import os
import re
import csv
from xbrl import XBRLParser
import logging

import pandas as pd

import settings
import utils

logger = logging.getLogger(__name__)

'''
    XBRLファイルを探索し、Parserにて変換
    変換結果にてCSVを作成
'''

default_tag = ['file_name', 'element_id', 'amount']
custom_tag = ['unit_ref', 'decimals', 'contextref']

class xbrlParser(object):
    def __init__(self, xbrl_file):
        self.xbrl_file = xbrl_file

    def ignore_pattern(self, node):
        if 'xsi:nil' in node.attrs:
            if node.attrs['xsi:nil'] == 'true':
                return True
        if not isinstance(node.string, str):
            return True
        if str(node.string).find(u'\n') > -1:
            return True
        if u'textblock' in str(node.name):
            return True

    def get_attrib_value(self, node, attrib):
        if attrib in node.attrs.keys():
            return node.attrs[attrib]
        else:
            return None

    def parse_xbrl(self):
        with open(self.xbrl_file, 'r', encoding=settings.encode_type) as of:
            xbrl = XBRLParser.parse(of)

        result_dicts = {}
        _idx = 0
        name_space = 'jp*'

        for node in xbrl.find_all(name=re.compile(name_space+':*')):
            if self.ignore_pattern(node):
                continue

            row_dict = {}
            row_dict['file_name'] = self.xbrl_file.rsplit(os.sep, 1)[1]
            row_dict['element_id'] = node.name
            row_dict['amount'] = node.string

            for tag in custom_tag:
                row_dict[tag] = self.get_attrib_value(node, tag)

            result_dicts[_idx] = row_dict
            _idx += 1

        return result_dicts

class Parser_Operator(object):
    def __init__(self, dict_result):
        self.list_dat_csv = self.__get_file_list()
        self.base_path = utils.get_base_path()
        self.dict_result = dict_result

    def __get_file_list(self):
        file_list = []
        file_name = f'{utils.get_file_name(settings.download_file_name)}.csv'
        file_list.append(file_name)
        return file_list

    def __find_all_files(self, search_path, str_period):
        result = []
        for root, dirs, files in os.walk(search_path):
            for file in files:
                if not self.__is_xbrl_file(root, file, str_period):
                    continue
                result.append(os.path.join(root, file))
        return result

    def __is_xbrl_file(self, root_path, file_name, str_period):
        if not file_name.endswith('.xbrl'):
            return False
        if u'AuditDoc' in str(root_path):
            return False
        if 'xbrl_files_' + str_period in str(root_path):
            return True


    # def __dump_file(self, writer, info_dicts):
    #     i = 0
    #     while i < (len(info_dicts)):
    #         row_dict = info_dicts[i]
    #         writer.writerow(row_dict)
    #         i += 1

    def create_pandas_data(self, info_dicts):
        result_elements = pd.DataFrame(default_tag.append(custom_tag))
        i = 0
        while i < len(info_dicts):
            row_dict = pd.DataFrame(info_dicts[i].values(), index=info_dicts[i].keys()).T
            result_elements = result_elements.append(row_dict,ignore_index=True)
            i += 1
        return result_elements


    def xbrl_to_csv(self):

        if not self.dict_result:
            return

        all_results = pd.DataFrame(default_tag.append(custom_tag))

        search_path = f'{self.base_path}/{settings.xbrl_dir_name}{settings.since}/'
        list_xbrl_files = self.__find_all_files(search_path, settings.since)
        for xbrl_file in list_xbrl_files:
            xp = xbrlParser(xbrl_file)
            info_dicts = xp.parse_xbrl()
            all_results = all_results.append(self.create_pandas_data(info_dicts), ignore_index=False)
        return all_results