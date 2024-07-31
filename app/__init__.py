from app.routes import home, dashboard, api 
from app.db import init_db
from flask import Flask
from app.utils import filters
from os import getenv

def create_app(test_config=None):
  # set up app config
  app = Flask(__name__, static_url_path='/')
  app.url_map.strict_slashes = False
  app.config.from_mapping(
    SECRET_KEY='super_secret_key',
    SQLALCHEMY_DATABASE_URI= getenv('DB_URL')
  )

  @app.route('/hello')
  def hello():
    return 'hello world'
  
  init_db(app)
  
  #register routes
  app.register_blueprint(home)
  app.register_blueprint(dashboard)
  # registering the blueprint: Now any routes that we define in the api.py module will automatically become part of the Flask app and have a prefix of /api.
  app.register_blueprint(api)  

  app.jinja_env.filters['format_url'] = filters.format_url
  app.jinja_env.filters['format_date'] = filters.format_date
  app.jinja_env.filters['format_plural'] = filters.format_plural


  
   

  return app