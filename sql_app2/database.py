from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists
from sqlalchemy_utils.functions.database import create_database


import os
from dotenv import load_dotenv
load_dotenv('DB.env')

USERNAME = os.environ.get("DB_USERNAME")
PASSWORD = os.environ.get("DB_PASSWORD")
HOST = os.environ.get("DB_HOST")
DATABASE = os.environ.get("DB_DATABASE")

##########

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app2.db"
#SQLALCHEMY_DATABASE_URL = "mysql+pymysql://" + USERNAME + ":" + PASSWORD + "@" + HOST + "/" + DATABASE
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
if not database_exists(engine.url):
    create_database(engine.url)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()