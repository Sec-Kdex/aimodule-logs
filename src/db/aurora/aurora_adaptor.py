from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
SQLALCHEMY_DATABASE_URL = "postgresql://"+os.environ.get("DB_USER")+":"+os.environ.get("DB_PASSWORD")+"@"+os.environ.get("DB_HOST")+":"+os.environ.get("DB_PORT")+"/"+os.environ.get("DB_NAME")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

print("-------------------------------------")
print("-------------------------------------")
print("-------------------------------------")
print(engine.table_names(), SQLALCHEMY_DATABASE_URL)
print("-------------------------------------")
print("-------------------------------------")
print("-------------------------------------")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)




