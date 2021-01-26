import configparser

conf = configparser.ConfigParser()
conf.read('settings.ini')

since = conf['pyinfo']['since'].lower()
until = conf['pyinfo']['until'].lower()
base_url = conf['pyinfo']['base_url']
download_file_name = conf['pyinfo']['download_file_name']
eggs_file_name = conf['pyinfo']['eggs_file_name']
xbrl_dir_name = conf['pyinfo']['xbrl_dir_name']
edinet_code_file_name = conf['pyinfo']['edinet_code_file_name']

com_cover_page = conf['elementinfo']['com_cover_page']

encode_type=conf['system']['encode_type']

db_name=conf['db']['db_name']

dict_cols = {
      '会社名'           : {'element_id' : ['companynamecoverpage'] }
    , '提出書類'         : {'element_id' : ['documenttitlecoverpage'] }
    , '提出日'           : {'element_id' : ['filingdatecoverpage'] }
    , '年度開始日'       : {'element_id' : ['currentfiscalyearstartdatedei'] }
    , '年度終了日'       : {'element_id' : ['currentfiscalyearenddatedei'] }
    #---ここまで必須---
    #以下は 'contextref' が必須
    , '発行済み株式数'   : {'element_id' : ['totalnumberofissuedsharessummaryofbusinessresults'
                                            ,'totalnumberofissuedsharescommonstocksummaryofbusinessresults'
                                            ,'totalnumberofissuedshares']
                            ,'contextref' : 'CurrentYearInstant' }
    , '営業CF'           : {'element_id' : ['netcashprovidedbyusedinoperatingactivitiessummaryofbusinessresults'
                                            ,'cashflowsfromusedinoperatingactivitiesifrssummaryofbusinessresults'
                                            ,'CashFlowsFromUsedInOperatingActivitiesUSGAAPSummaryOfBusinessResults']
                            ,'contextref' : 'CurrentYearDuration' }
    , '財務CF'           : {'element_id' : ['netcashprovidedbyusedinfinancingactivitiessummaryofbusinessresults'
                                            ,'cashflowsfromusedinfinancingactivitiesifrssummaryofbusinessresults'
                                            ,'CashFlowsFromUsedInFinancingActivitiesUSGAAPSummaryOfBusinessResults']
                            ,'contextref' : 'CurrentYearDuration' }
    , '投資CF'           : {'element_id' : ['netcashprovidedbyusedininvestingactivitiessummaryofbusinessresults'
                                            ,'cashflowsfromusedininvestingactivitiesifrssummaryofbusinessresults'
                                            ,'CashFlowsFromUsedInInvestingActivitiesUSGAAPSummaryOfBusinessResults']
                            ,'contextref' : 'CurrentYearDuration' }
    , '純利益'           : {'element_id' : ['profitlossattributabletoownersofparentsummaryofbusinessresults'
                                            ,'ProfitLossAttributableToOwnersOfParentIFRSSummaryOfBusinessResults'
                                            ,'NetIncomeLossAttributableToOwnersOfParentUSGAAPSummaryOfBusinessResults'
                                            ,'netincomelosssummaryofbusinessresults']
                            ,'contextref' : 'CurrentYearDuration' }
    , '売上高'           : {'element_id' : ['netsalessummaryofbusinessresults'
                                            ,'NetSalesIFRSSummaryOfBusinessResults'
                                            ,'RevenuesUSGAAPSummaryOfBusinessResults'
                                            ,'operatingrevenue1summaryofbusinessresults'
                                            ,'revenueifrssummaryofbusinessresults'
                                            ,'netoperatingrevenuesummaryofbusinessresults'
                                            ,'businessrevenuesummaryofbusinessresults']
                            ,'contextref' : 'CurrentYearDuration' }
    , 'BS現金預金'      : {'element_id' : ['cashanddeposits']
                            ,'contextref' : 'CurrentYearInstant' }
    , 'BS負債合計'      : {'element_id' : ['liabilities']
                            ,'contextref' : 'CurrentYearInstant' }
    }