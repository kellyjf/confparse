#!/usr/bin/env python

import flask

from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Column, String, Integer, Date, Numeric, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship

from datetime import datetime as dt
from decimal import Decimal
from csv import reader

Model = declarative_base()

class Category(Model):
	__tablename__ = 'categories'
	id   = Column(Integer,primary_key=True)
	name = Column(String(128))
	transactions=relationship('Transaction', backref='category')
	
class Transaction(Model):
	__tablename__ = 'transactions'
	id = Column(Integer,primary_key=True)
	date = Column(Date)
	amount = Column(Numeric)
	payee =  Column(String(128))
	comment =  Column(String(256))
	category_id = Column(Integer, ForeignKey('categories.id'))	


eng=create_engine("sqlite:///test.sqlite")

Model.metadata.create_all(eng)

Cursor=sessionmaker(eng)
curs=Cursor()

with open("Checking1.csv", 'rb') as c:
	cfile=reader(c)
	for rec in cfile:
		date,amt,star,num,comm=rec

		trn=Transaction(date=dt.strptime(date,'%m/%d/%Y'),
			amount=Decimal(amt), 
			comment=comm)
		curs.add(trn)
curs.commit()



	


