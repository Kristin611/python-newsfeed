from os import getenv
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 
from dotenv import load_dotenv
from flask import g 

load_dotenv()


# connect to database using env variable
engine = create_engine(getenv('DB_URL'), echo=True, pool_pre_ping=True, pool_size=20, max_overflow=0, pool_recycle=3600)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# initialize db connection & create tables in sqlalchemy
def init_db(app):
  print("Initializing database...")
  Base.metadata.create_all(engine)
  print("Database initialized.")

  # when context is destroyed, run close_db function  
  app.teardown_appcontext(close_db)

# manages db connections: each call to get_db returns a new Session instance, which is important for ensuring that database operations are executed within the context of a transaction and that each operation has its own session. By creating a new Session for each operation, you ensure that each session operates independently, avoiding conflicts between concurrent database interactions. However, cue application context, g. 
def get_db():
  if 'db' not in g:
    # store db connection in app context; using application context (g) so it return the connection from the g object instead of creating a new Session instance each time.
    g.db = Session()

  return g.db   

# The pop() method attempts to find and remove db from the g object. If db exists (that is, db doesn't equal None), then db.close() will end the connection.
def close_db(e=None):
  db = g.pop('db', None)

  if db is not None:
    db.close()




# The engine variable manages the overall connection to the database.
# The Session variable generates temporary connections for performing create, read, update, and delete (CRUD) operations.
# The Base class variable helps us map the models to real MySQL tables.
# pool_recycle=3600: This recycles the connections every hour (3600 seconds). It helps to avoid issues where the database server might drop idle connections after a certain period.
# pool_pre_ping=True: This pre-pings the connection to ensure it is still valid before using it. If the connection is invalid, it will be replaced with a new one.