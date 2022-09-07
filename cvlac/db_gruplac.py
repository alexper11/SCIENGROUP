from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://postgres:admin@localhost/gruplacdb')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

