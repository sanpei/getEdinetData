import logging
import os
from datetime import timedelta
from datetime import date

from sqlalchemy import Column
from sqlalchemy import desc
from sqlalchemy import asc
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy.exc import IntegrityError

from app.base import Base
from app.base import session_scope
import pandas as pd

import utils

logger = logging.getLogger(__name__)

class Financial(Base):

    __tablename__ = 'financial'

    edinet_code = Column(String, primary_key=True, nullable=False)
    start_period = Column(DateTime, primary_key=True, nullable=False)
    end_period = Column(DateTime, primary_key=True, nullable=False)
    company_name = Column(String)
    submit_paper = Column(String)
    submit_date = Column(DateTime)
    shared_num = Column(Integer)
    operating_cash = Column(Float)
    financial_cash = Column(Float)
    investment_cash = Column(Float)
    net_income = Column(Float)
    sales_amt = Column(Float)
    bs_cash_amt_ttl = Column(Float)
    bs_liabilities_amt_ttl = Column(Float)
    securities_code = Column(Integer)
    industry = Column(String)
    revision = Column(String)
    annual = Column(String)
    file_name = Column(String)
    eps = Column(Float)

    @classmethod
    def create(cls, dict_result):
        financial = cls(
            edinet_code=dict_result['edinet_code'],
            start_period=utils.str_to_date(dict_result['年度開始日']),
            end_period=utils.str_to_date(dict_result['年度終了日']),
            company_name=dict_result['会社名'],
            submit_paper=dict_result['提出書類'],
            submit_date=utils.str_to_date(dict_result['提出日']),
            shared_num=dict_result['発行済み株式数'],
            operating_cash=dict_result['営業CF'],
            financial_cash=dict_result['財務CF'],
            investment_cash=dict_result['投資CF'],
            net_income=dict_result['純利益'],
            sales_amt=dict_result['売上高'],
            bs_cash_amt_ttl=dict_result['BS現金預金'],
            bs_liabilities_amt_ttl=dict_result['BS負債合計'],
            securities_code=dict_result['証券コード'],
            industry=dict_result['業種'],
            revision=dict_result['訂正'],
            annual=dict_result['annual'],
            file_name=dict_result['file_name'],
            eps=0.0
        )

        try:
            with session_scope() as session:
                session.add(financial)
            return financial
        except IntegrityError:
            return False

    def save(self):
        with session_scope() as session:
            session.add(self)

    def update(self, financial):
        with session_scope() as session:
            session.add(financial)


    '''
        get method 
        どのようにgetするか
        比較する場合は、四半期のget, 年度毎のget も作成するか
    '''

    @classmethod
    def get_all_financial(cls):

        with session_scope() as session:
            financial = session.query(cls).\
                order_by(cls.edinet_code.desc(), cls.start_period.desc()).all()
        if financial is None:
            return None
        return financial

    @classmethod
    def get_by_annual(cls, annual):
        with session_scope() as session:
            financial = session.query(cls).filter_by(annual=annual).\
                order_by(cls.edinet_code.desc()).all()

        return financial

    @classmethod
    def get_by_start_period(cls, edinet_code, start_period, annual):
        with session_scope() as session:
            start_period = session.query(cls).\
                filter_by(start_period=start_period).\
                filter_by(edinet_code=edinet_code).\
                filter_by(annual=annual).first()

        if start_period is None:
            return None
        return start_period

    def calc_eps(self, financials):
        if financials is None:
            return

        for financial in financials:
            eps = 0
            if not financial.shared_num is None and not financial.shared_num == 0:
                eps = round(financial.net_income / financial.shared_num, 2)
            financial.eps = eps
            self.update(financial)

    '''
        年間EPS比較
    '''
    def get_pre_annual_eps(self):
        financials = self.get_by_annual('T')

        if financials is None:
            return

        for financial in financials:
            start_period = self.get_by_start_period(financial.edinet_code,
                                                    financial.start_period - timedelta(days=365),
                                                    'T')
            if start_period:
                print(start_period.edinet_code)
                print(financial.eps, start_period.eps)


    '''
        年間売上高増加率
    '''
    def get_pre_annual_sales(self):
        financials = self.get_by_annual('T')

        if financials is None:
            return

        comped = 'F'
        pre_edinet_code = ''

        for financial in financials:

            if pre_edinet_code != financial.edinet_code:
                comped = 'F'

            #365日ではなく、3ヶ月の日付であるべき
            start_period = self.get_by_start_period(financial.edinet_code,
                                                    financial.start_period - timedelta(days=365),
                                                    'T')
            if start_period and comped == 'F':
                if start_period.sales_amt != 0:
                    if round(financial.sales_amt / start_period.sales_amt, 2) >= 1.4:
                        print(financial.edinet_code, financial.securities_code)
                comped = 'T'


            pre_edinet_code = financial.edinet_code


    '''
        テストデータがあるか確認のみ
    '''
    def dual_edinet(self, financials):
        pre_edinet_code = ''
        pre_start_period = ''
        pre_annual = ''

        com_indices = pd.DataFrame()

        for financial in financials:
            pre_data = {}
            data = {}
            if pre_edinet_code == financial.edinet_code:
                pre_data["edinet_code"] = pre_edinet_code
                pre_data["start_period"] = pre_start_period
                pre_data["annual"] = pre_annual
                raw = pd.DataFrame(pre_data, index=[financial.edinet_code])
                com_indices = pd.concat([com_indices, raw])

                data["edinet_code"] = financial.edinet_code
                data["start_period"] = financial.start_period
                data["annual"] = financial.annual
                raw = pd.DataFrame(data, index=[financial.edinet_code])
                com_indices = pd.concat([com_indices, raw])

            pre_edinet_code = financial.edinet_code
            pre_start_period = financial.start_period
            pre_annual = financial.annual
        com_indices.to_csv(os.path.join(os.getcwd(),'edinet_code_list'))




