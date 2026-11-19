from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# import psycopg2
# from psycopg2.extras import RealDictCursor
from .config import settings



SQLALCHEMY_DATABASE_URL =  f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# engine is repsonsible establishing the connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# when we actually want to talk to the DB we actually have to make use of the session

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# to extend the baseclass 
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database = 'fastapi', user = 'postgres', password = '9743692132', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("The database connection was successful!")
#         break
#     except Exception as error:
#         print("Connecting to the database is failed")
#         print("Error:", error)
