import logging

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy.exc import IntegrityError

from app.base import Base
from app.base import session_scope

import utils

logger = logging.getLogger(__name__)

class Financial(Base):

    __tablename__ = 'financial_quarter'

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
    file_name = Column(String)

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
            file_name=dict_result['file_name']
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


    '''
        get method 
        どのようにgetするか
        比較する場合は、四半期のget, 年度毎のget も作成するか
    '''


