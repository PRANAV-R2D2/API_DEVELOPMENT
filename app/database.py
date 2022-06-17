from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}' 

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Sessionlocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()


#dependency
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally: 
        db.close()


### if wanted to try raw sql


# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# while True:

#     try:
#         conne = psycopg2.connect(host='localhost',database='fastapi_db',user='postgres',password='postgress123',cursor_factory=RealDictCursor)
#         cursors = conne.cursor()
#         print("database connected")
#         break
#     except Exception as error:
#         print("connecting to database failed")
#         print("Error :",error)
#         time.sleep(5)

