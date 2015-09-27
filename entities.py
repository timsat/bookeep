# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, Integer, String, Numeric, ForeignKey, SmallInteger
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///data.sqlite', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Agent(Base) :
    __tablename__ = 'agents'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class BankAccount(Base) :
    __tablename__ = 'bankaccounts'
    id = Column(Integer, primary_key=True)
    bname = Column(String)
    bik = Column(String)
    num = Column(String)
    kpp = Column(String)
    agentId = Column(Integer, ForeignKey('agents.id'))

class Transaction(Base) :
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    accId = Column(Integer, ForeignKey('transactions.id'))
    amount = Column(Numeric(precision=2),)
    type = Column(SmallInteger)
    date = Column(Integer)

def createDb() :
    Base.metadata.create_all(engine)
