from os import getenv
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from dotenv import load_dotenv
import logging
from sqlalchemy.exc import OperationalError
from retrying import retry 

load_dotenv()


# connect to database using env variable
engine = create_engine(getenv('DB_URL'), echo=True, pool_pre_ping=True, pool_size=20, max_overflow=0, pool_recycle=3600)
Session = sessionmaker(bind=engine)
Base = declarative_base()



# @retry(stop_max_attempt_number=5, wait_fixed=2000)
# def run_transaction(session, func, *args, **kwargs):
#     try: 
#         result = func(session, *args, **kwargs)
#         session.commit()
#         return result
#     except OperationalError as e:
#         session.rollback()
#         print(f"OperationalError occurred: {e}. Retrying...")
#         raise
#     finally:
#         session.close()

# The engine variable manages the overall connection to the database.
# The Session variable generates temporary connections for performing create, read, update, and delete (CRUD) operations.
# The Base class variable helps us map the models to real MySQL tables.
# pool_recycle=3600: This recycles the connections every hour (3600 seconds). It helps to avoid issues where the database server might drop idle connections after a certain period.
# pool_pre_ping=True: This pre-pings the connection to ensure it is still valid before using it. If the connection is invalid, it will be replaced with a new one.