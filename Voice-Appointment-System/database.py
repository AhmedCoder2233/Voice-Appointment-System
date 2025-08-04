from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DB_URL")

engine = create_engine(DATABASE_URL)

LocalSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()