from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Shop:
    SHOP_ID = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    TITLE = Column(String(64), nullable=False)