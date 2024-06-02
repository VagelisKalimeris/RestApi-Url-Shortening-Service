from os import environ

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


load_dotenv()
postgres_user = environ['POSTGRES_USER']
postgres_password = environ['POSTGRES_PASSWORD']

SQLALCHEMY_DATABASE_URL = f'postgresql://shortener:{postgres_password}@postgres-container/urls_db'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
