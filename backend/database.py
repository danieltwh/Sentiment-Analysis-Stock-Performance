from venv import create
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# from dotenv import load_dotenv

# if os.path.exists(".env"):
#     load_dotenv(".env")
    

# from key import HEROKU_POSTGRE_PASSWORD

# SQLALCHEMY_DATABASE_URL = f"postgresql://fdyjxmoknqhbkk:{HEROKU_POSTGRE_PASSWORD}@ec2-18-209-78-11.compute-1.amazonaws.com/d7ul40jkdp08kb"
SQLALCHEMY_DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(
    url = SQLALCHEMY_DATABASE_URL,
    # connect_args = {"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()