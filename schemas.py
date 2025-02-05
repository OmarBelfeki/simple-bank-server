import uuid
import calendar

from sqlalchemy import Column, String, Integer, create_engine, insert, Float
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///bank.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()


class UserDB(Base):
    __tablename__ = "userdb"

    id = Column(String, primary_key=True)
    username = Column(String)
    password = Column(String)


class CreditHist(Base):
    __tablename__ = "credithist"

    id = Column(String, primary_key=True)
    username = Column(String)
    credit_balance = Column(Integer)
    credit_paid = Column(Integer)
    credit_rolling = Column(Integer)


class SpendHist(Base):
    __tablename__ = "spendhist"

    id = Column(String, primary_key=True)
    username = Column(String)
    month = Column(String)
    total_spend = Column(Integer)
    liability = Column(Integer)
    assets = Column(Integer)


class UserBalance(Base):
    __tablename__ = "userbalance"

    id = Column(String, primary_key=True)
    username = Column(String)
    curr_balance = Column(Float)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)

    month = [i[:3] for i in calendar.month_name][1:]

    for i in range(5):
        user = UserDB(id=str(uuid.uuid4()), username=f"bar123{i}", password=f"bar123{i}")
        bal = UserBalance(id=str(uuid.uuid4()), username=f"bar123{i}", curr_balance=123.123)
        spend = SpendHist(id=str(uuid.uuid4()), username=f"bar123{i}", month=month[i], total_spend=15000, liability=4000, assets=1300)
        credit = CreditHist(id=str(uuid.uuid4()), username=f"bar123{i}", credit_balance=4500, credit_paid=3500, credit_rolling=400)
        session.add_all([user, bal, spend, credit])
        session.commit()
