from app.models import User
from app.db import Session, Base, engine
from sqlalchemy import inspect

# def test_connection():
#     try:
#         inspector = inspect(engine)
#         print("Connection successful")
#     except Exception as e:
#         print(f"Connection failed: {e}")

# if __name__ == "__main__":
#     test_connection()


# drop and rebuild tables
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)



# @retry(stop_max_attempt_number=5, wait_fixed=2000)
# def run_seed_database():
#     session = Session()
#     try: 
#         seed_database(session)
#         session.commit()
#     except OperationalError as e:
#         session.rollback()
#         print(f"OperationalError occurred: {e}. Retrying...")
#         raise
#     finally:
#         session.close()

# if __name__ == "__main__":
#     run_seed_database()            

# This is where the db variables that you created earlier come into play. The code uses the Base class together with the engine connection variable to do two things. First, it drops all the existing tables. Second, it creates any tables that Base mapped, in a class that inherits Base (like User).