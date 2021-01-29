import logging
import sys
import pandas as pd

import app.getdata as gt
import app.edinet as edinet
import app.eggs as eggs
import app.parser as parser
import app.financial as financial

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

if __name__ == '__main__':
    #EDINETへの接続Linkを取得し、Jsonファイルへのアクセスリストをダウンロード
    # edinet = edinet.Catcher()
    # dict_result = edinet.create_xbrl_url_json()

    #JsonファイルへのアクセスリストからXBRLファイルをダウンロード
    # eggs = eggs.Downloader(dict_result)
    # eggs.download()
    #
    # if not dict_result:
    #     logging.ERROR(f'data=dict_result count=0')
    #
    # ダウンロードしたXrblファイルを構成要素毎にcsvファイルへ変換
    # parser = parser.Parser_Operator(dict_result)
    # all_elements = parser.xbrl_to_csv()
    #
    # 変換したファイルとelementIDをマッチさせ、AMOUNTを取得するまで
    # eggs_crt = gt.Eggs_Operator(all_elements)
    # eggs_crt.get_elements()

    financials = financial.Financial()
    # test = financials.get_all_financial()
    # financials.calc_eps(test)
    # financials.dual_edinet(test)
    financials.get_pre_annual_sales()
