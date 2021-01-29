import codecs
import logging
import os
import re

import pandas as pd
from tqdm import tqdm

import settings
import utils
from app.financial import Financial

logger = logging.getLogger(__name__)

def get_dict_code(index='ＥＤＩＮＥＴコード'):
    file_path = f'{utils.get_base_path()}/{settings.edinet_code_file_name}.csv'

    with codecs.open(file_path, 'r', encoding='shift-jis', errors='ignore') as file:
        df = pd.read_csv(file, skiprows=[0], usecols=['ＥＤＩＮＥＴコード', '提出者名', '証券コード', '提出者業種'])

    df = df.loc[df['証券コード'] > 0, : ]
    df['証券コード'] = df['証券コード'] / 10
    df['証券コード'] = df['証券コード'].astype(int)
    result = df.set_index(index).T.to_dict()

    logger.info(f'対象銘柄:{len(result)}')

    return result

'''
 below is not process definition
'''

def make_element_ids_csv(egg_file_name):
    base_path = os.getcwd()
    result_file_name = f'element_ids({ egg_file_name }).csv'
    df_egg = pd.read_csv(os.path.join(base_path, egg_file_name)).drop_duplicates()
    df_egg.loc[:, 'element_id'].drop_duplicates().to_csv(os.path.join(base_path, result_file_name))

def make_sample_data_csv(egg_file_name, edinet_code):
    base_path = os.getcwd()
    result_file_name = f'sample_data({egg_file_name}{edinet_code}).csv'
    df_egg = pd.read_csv(os.path.join(base_path, egg_file_name)).drop_duplicates()
    check1 = df_egg[( df_egg['file_nm'].str.contains(edinet_code))]
    if len(check1) > 0:
        check1.to_csv(os.path.join(base_path, result_file_name))
    else:
        logger.info(f'{edinet_code} is none')

class Eggs_Operator(object):
    def __init__(self, list_df_eggs , result_file_name=f'com_indices{settings.since}.csv'):
        self.base_path = os.getcwd()
        self.result_file_name = result_file_name
        # self.list_df_eggs = [pd.read_csv(os.path.join(self.base_path, egg_file_name)).drop_duplicates()
        # for egg_file_name in self.get_list_eggs()]
        self.list_df_eggs = [list_df_eggs.drop_duplicates()]
        self.dict_codes = get_dict_code()
        self.dict_cols = settings.dict_cols

    def get_list_eggs(self):
        list_eggs = []
        list_eggs.append(f'{utils.get_file_name(settings.eggs_file_name)}.csv')
        return list_eggs

    def get_element(self, df, col):
        element_ids = self.dict_cols[col]['element_id']
        if col in ['会社名', '提出書類', '提出日', '年度開始日', '年度終了日']:
            check1 = df[df['element_id'].str.contains(element_ids[0].lower())]
            if len(check1) == 1:
                return check1['amount'].values[0]
            else:
                return 0
        else:
            contextref = self.dict_cols[col]['contextref']

            for element_id in element_ids:
                check1 = df[df['element_id'].str.contains(element_id.lower())]
                check2 = check1[check1['contextref'] == contextref].copy() #連結
                if len(check2) == 1:
                    return check2['amount'].values[0]
                elif len(check2) > 2:
                    check2['str_len'] = check2['element_id'].apply(lambda x: len(str(x)))
                    return check2.loc[check2['str_len'] == check2['str_len'].min(), 'amount'].values[0]
            for element_id in element_ids:
                check1 = df[df['element_id'].str.contains(element_id.lower())]
                check2 = check1[check1['contextref'] == f'{contextref}_NonConsolidatedMember'].copy() #個別
                if len(check2) == 1:
                    return check2['amount'].values[0]
                elif len(check2) > 1:
                    check2['str_len'] = check2['element_id'].apply(lambda x: len(str(x)))
                    return check2.loc[check2['str_len'] == check2['str_len'].min(), 'amount'].values[0]
            return 0

    def get_elements(self):
        com_indices = pd.DataFrame()
        for df_eggs in self.list_df_eggs:
            file_names = df_eggs[df_eggs['element_id'] == settings.com_cover_page].drop_duplicates()['file_name'].values
            for file_name in tqdm(file_names):
                edinet_code = re.search(r'E[0-9]{5}', file_name).group(0)
                if not edinet_code in self.dict_codes:
                    continue
                df_target = df_eggs[df_eggs['file_name'] == file_name]
                data = {col: self.get_element(df_target, col) for col in self.dict_cols}
                data['証券コード'] = self.dict_codes[edinet_code]['証券コード']
                data['業種'] = self.dict_codes[edinet_code]['提出者業種']
                data['訂正'] = 1 if '訂正' in data['提出書類'] else 0
                data['file_name'] = file_name
                data['edinet_code'] = edinet_code
                data['annual'] = 'T' if utils.get_yuho_text(f'{data["提出書類"]}{data["会社名"]}') else 'F'

                Financial.create(dict_result=data)

                raw = pd.DataFrame(data, index=[edinet_code])
                com_indices = pd.concat([com_indices, raw])


        # com_indices.to_csv(os.path.join(self.base_path, self.result_file_name))