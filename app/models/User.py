from app.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates 
import bcrypt

salt = bcrypt.gensalt()

# user class inherits from the Base class; the properties in the user class will be used by the parent Base class to create the table

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)

    # @validates is a function decorator; see below for more info; make sure the function decorators are indented within the User class for them to work 
    # self refers to the instance of the class in which the validate_email method is defined, in this case the  class is the User class.
    # key refers to the name of the attribute being validated, which in this case is 'email'. In this context, key will always be 'password' because the decorator is specified as @validates('password').
    @validates('email')
    def validate_email(self, key, email):
        # use assert keyword to make sure email address contains @ character. The assert keyword automatically throws an error if the condition is false, thus preventing the return statement from happening.
        assert '@' in email

        return email

    @validates('password')
    def validate_password(self, key, password):
        assert len(password) > 4

        # encrypt pw
        return bcrypt.hashpw(password.encode('utf-8'), salt) 



# Function Decorators:
# A decorator is a function that takes another function and extends its behavior without explicitly modifying it. Decorators are commonly used for logging, enforcing access control and permissions, instrumentation, caching, and more.