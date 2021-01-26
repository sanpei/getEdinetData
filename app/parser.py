import os
import re
import csv
from xbrl import XBRLParser
import logging

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
    def __init__(self):
        self.list_dat_csv = self.__get_file_list()
        self.base_path = utils.get_base_path()

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

    def __dump_file(self, writer, info_dicts):
        i = 0
        while i < (len(info_dicts)):
            row_dict = info_dicts[i]
            writer.writerow(row_dict)
            i += 1

    def xbrl_to_csv(self):

        utils.delete_file(self.base_path, settings.eggs_file_name)

        for dat_csv in self.list_dat_csv:
            str_period = dat_csv.replace(".csv", "").replace(settings.download_file_name, "")
            eggs_file = f'{settings.eggs_file_name}{str_period}.csv'
            search_path = f'{self.base_path}/{settings.xbrl_dir_name}{str_period}/'
            with open(os.path.join(self.base_path, eggs_file), 'w', encoding=settings.encode_type) as of:
                resultCsvWriter = csv.DictWriter(of, default_tag+custom_tag, lineterminator='\n')
                resultCsvWriter.writeheader()
                list_xbrl_files = self.__find_all_files(search_path, str_period)
                for xbrl_file in list_xbrl_files:
                    xp = xbrlParser(xbrl_file)
                    info_dicts = xp.parse_xbrl()
                    self.__dump_file(resultCsvWriter, info_dicts)