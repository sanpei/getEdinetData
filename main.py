import logging
import sys

import app.getdata as gt

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

if __name__ == '__main__':
    #EDINETへの接続Linkを取得し、Jsonファイルへのアクセスリストをダウンロード
    # edinet = edinet.Catcher()
    # edinet.create_xbrl_url_json()

    #JsonファイルへのアクセスリストからXBRLファイルをダウンロード
    # eggs = eggs.Downloader()
    # eggs.download()

    #ダウンロードしたXrblファイルを構成要素毎にcsvファイルへ変換
    # parser = parser.Parser_Operator()
    # parser.xbrl_to_csv()

    #DBファイルを作成する
    #DBファイルからデータを取得,DFファイルへ持っておく

    #変換したファイルとelementIDをマッチさせ、AMOUNTを取得するまで
    eggs_crt = gt.Eggs_Operator()
    eggs_crt.get_elements()

