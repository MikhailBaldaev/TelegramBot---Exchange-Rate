import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, sessionmaker
from config import *


Base = declarative_base()

DSN = DSN
engine = sq.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()


class USD_Rates(Base):
    __tablename__ = "USD_rates"

    id = sq.Column(sq.Integer, primary_key=True)
    date = sq.Column(sq.String(length=40), unique=True, nullable=False)
    rate = sq.Column(sq.String(length=60))


def create_tables(engine):
    Base.metadata.create_all(engine)


def find_rate(date):
    result = session.query(USD_Rates.rate).filter(USD_Rates.date == date).all()
    session.commit()
    return result


def find_period(date_list):
    result = []
    for i in date_list:
        inquiry = session.query(USD_Rates.rate).filter(USD_Rates.date == i).all()[0][0]
        result.append({i: inquiry})
    session.commit()
    return result


def insert(date, rate):
    if session.query(USD_Rates.date).filter(USD_Rates.date == date).all():
        pass
    else:
        row = USD_Rates(date=date, rate=rate)
        session.add(row)
    session.commit()


create_tables(engine)
