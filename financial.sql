SQLite format 3   @                                                                     .G�� k k�                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           �G//�=tablefinancial_quarterfinancial_quarterCREATE TABLE financial_quarter (
	edinet_code VARCHAR NOT NULL, 
	start_period DATETIME NOT NULL, 
	end_period DATETIME NOT NULL, 
	company_name VARCHAR, 
	submit_paper VARCHAR, 
	submit_date DATETIME, 
	shared_num INTEGER, 
	operating_cash FLOAT, 
	financial_cash FLOAT, 
	investment_cash FLOAT, 
	net_income FLOAT, 
	sales_amt FLOAT, 
	bs_cash_amt_ttl FLOAT, 
	bs_liabilities_amt_ttl FLOAT, 
	securities_code INTEGER, 
	industry VARCHAR, 
	revision VARCHAR, 
	file_name VARCHAR, 
	PRIMARY KEY (edinet_code, start_period, end_period)
)AU/ indexsqlite_autoindex_financial_quarter_1financial_quarter          �  ���
�
	<Sp���                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 �cAAU1A�E008552019-12-01 00:00:00.0000002020-11-30 00:00:00.000000大阪有機化学工業株式会社四半期報告書2020-04-03 00:00:00.000000[化学0jpcrp040300-q1r-001_E00855-000_2020-02-29_01_2020-04-03.xbrl�AA�1A+�E007102019-06-01 00:00:00.0000002020-05-31 00:00:00.000000株式会社TAKARA & COMPANY（旧会社名 宝印刷株式会社）四半期報告書2020-04-06 00:00:00.000000�その他製品0jpcrp040300-q3r-001_E00710-000_2020-02-29_01_2020-04-06.xbrl�TAA11A�E027222019-11-21 00:00:00.0000002020-11-20 00:00:00.000000北恵株式会社四半期報告書2020-04-03 00:00:00.000000&�卸売業0jpcrp040300-q1r-001_E02722-000_2020-02-20_01_2020-04-03.xbrl�`
AAI1A�E276932019-12-01 00:00:00.0000002020-11-30 00:00:00.000000株式会社ネクステージ四半期報告書2020-04-03 00:00:00.000000r小売業0jpcrp040300-q1r-001_E27693-000_2020-02-29_01_2020-04-03.xbrl�f	AAO1A%�E023952019-11-21 00:00:00.0000002020-11-20 00:00:00.000000象印マホービン株式会社四半期報告書2020-04-03 00:00:00.000000電気機器0jpcrp040300-q1r-001_E02395-000_2020-02-20_01_2020-04-03.xbrl�`AAI1A�E029952019-08-21 00:00:00.0000002020-08-20 00:00:00.000000ケイティケイ株式会社四半期報告書2020-04-03 00:00:00.000000�卸売業0jpcrp040300-q2r-001_E02995-000_2020-02-20_01_2020-04-03.xbrl�fAAO1A%�E013702019-12-01 00:00:00.0000002020-11-30 00:00:00.000000日本フイルコン株式会社四半期報告書2020-04-03 00:00:00.0000006金属製品0jpcrp040300-q1r-001_E01370-000_2020-02-29_01_2020-04-03.xbrl�lAAO1A1�E000062019-06-01 00:00:00.0000002020-05-31 00:00:00.000000株式会社　サカタのタネ四半期報告書2020-04-06 00:00:00.000000a水産・農林業0jpcrp040300-q3r-001_E00006-000_2020-02-29_01_2020-04-06.xbrl�]AA=1A%�E018562019-05-21 00:00:00.0000002020-05-20 00:00:00.000000コーセル株式会社四半期報告書2020-04-03 00:00:00.000000�電気機器0jpcrp040300-q3r-001_E01856-000_2020-02-20_01_2020-04-03.xbrl�TAA71A�E016032019-12-01 00:00:00.0000002020-11-30 00:00:00.000000株式会社不二越四半期報告書2020-04-02 00:00:00.000000J機械0jpcrp040300-q1r-001_E01603-000_2020-02-29_01_2020-04-02.xbrl�6AA=�=AI�E037602019-04-01 00:00:00.0000002020-03-31 00:00:00.000000丸三証券株式会社四半期報告書(2020年４月６日付け訂正報告書の添付インラインXBRL)2019-08-13 00:00:00.000000!�証券、商品先物取引業1jpcrp040300-q1r-001_E03760-000_2019-06-30_02_2020-04-06.xbrl�6AA=�=AI�E037602018-04-01 00:00:00.0000002019-03-31 00:00:00.000000丸三証券株式会社四半期報告書(2020年４月６日付け訂正報告書の添付インラインXBRL)2018-11-13 00:00:00.000000!�証券、商品先物取引業1jpcrp040300-q2r-001_E03760-000_2018-09-30_02_2020-04-06.xbrl�]AA=1A%�E268312019-06-01 00:00:00.0000002020-05-31 00:00:00.000000三協立山株式会社四半期報告書2020-04-06 00:00:00.000000,金属製品0jpcrp040300-q3r-001_E26831-000_2020-02-29_01_2020-04-06.xbrl
   � {��:���6�>�w                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  @AAE008552019-12-01 00:00:00.0000002020-11-30 00:00:00.000000@AAE007102019-06-01 00:00:00.0000002020-05-31 00:00:00.000000@AAE027222019-11-21 00:00:00.0000002020-11-20 00:00:00.000000@AAE276932019-12-01 00:00:00.0000002020-11-30 00:00:00.000000
@AAE023952019-11-21 00:00:00.0000002020-11-20 00:00:00.000000	@AAE029952019-08-21 00:00:00.0000002020-08-20 00:00:00.000000@AAE013702019-12-01 00:00:00.0000002020-11-30 00:00:00.000000@AAE000062019-06-01 00:00:00.0000002020-05-31 00:00:00.000000@AAE018562019-05-21 00:00:00.0000002020-05-20 00:00:00.000000@AAE016032019-12-01 00:00:00.0000002020-11-30 00:00:00.000000@AAE037602019-04-01 00:00:00.0000002020-03-31 00:00:00.000000@AAE037602018-04-01 00:00:00.0000002019-03-31 00:00:00.000000?AA	E268312019-06-01 00:00:00.0000002020-05-31 00:00:00.000000