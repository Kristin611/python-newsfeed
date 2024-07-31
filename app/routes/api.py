from flask import Blueprint, request, jsonify, session
from app.models import User
# establish a connection to the db
from app.db import get_db
from sqlalchemy.exc import SQLAlchemyError
import sys

bp = Blueprint('api', __name__, url_prefix=('/api'))

@bp.route('/users', methods=['POST'])
def signup():
    data = request.get_json()
    print('Received data:', data)
    
    db = get_db()
    print('DB session:', db)

    try:
    # create a new user
        newUser = User(
        username = data['username'],
        email = data['email'],
        password = data['password']
        )
        print('New user created', newUser)

        # save in db; preps the INSERT statement
        db.add(newUser)
        print('User added to session')
        # officially update the db with commit()
        db.commit()
        print('Database committed')

    except:
        print(sys.exe_info()[0])
        # insert failed, so rollback and send error to front end
        db.rollback()
       # insert failed, so send error to front end
        return jsonify(message = 'Signup failed'), 500     

    # clear any existing session data
    session.clear()
    # create new session by user_id to aid future database queries
    session['user_id'] = newUser.id
    # Boolean property that the templates will use to conditionally render elements.
    session['loggedIn'] = True
    return jsonify(id = newUser.id)

@bp.route('/users/logout', methods=['POST'])
def logout():
    # remove session variables
    session.clear()
    return '', 204

@bp.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()
    db = get_db()

    # check if the user's posted email address exists in the db. since sqlalchemy will throw an error if the user doesnt exist, wrap the query in a try/except statement
    try:
        user = db.query(User).filter(User.email == data['email']).one()
    except:
        print(sys.exc_info()[0])
        return jsonify(message = 'Incorrect credentials'), 400
    
    # verify_password() method comes from user model
    if user.verify_password(data['password']) == False:
        return jsonify(message = 'Incorrect credentials'), 400
    
    # create the session and send back a valid response
    session.clear()
    session['user_id'] = user.id
    session['loggedIn'] = True

    return jsonify(id = user.id)
        
        

# @bp.route('/users', methods=['POST'])
# def create_user():
#     data = request.get_json()
#     print(f"Received data: {data}")

#     db = get_db()


#     try:
#         newUser = User(
#             username=data['username'],
#             email=data['email'],
#             password=data['password']
#         )
#         print(f"New user created {newUser}")

        
#         db.add(newUser)
#         print('User added to session:', newUser)
#         db.commit()
#         print('Database committed')
#     except SQLAlchemyError as e:
#         db.rollback()
#         print(f'Error occurred: {e}')   
#         return jsonify({'message': 'An error occurred while creating the user.'}), 500 
    
#     return jsonify({'message': 'User created successfully'}), 200




# blueprint is a Flask concept that allows you to organize routes and other code in your application into distinct/modular components, making it easier to manage large applications. When you create a Blueprint, you're essentially defining a set of routes and views that can be registered on an application later. 
    # api is the name of the blueprint, used to identify the blueprint w/i your app
    # __name__ is a special variable in Python that represents the name of the current module. It's used by Flask to locate the blueprint's resources.
    # url_prefix=('/api'): This specifies a URL prefix for all routes defined in this blueprint. In this case, it means that all routes in this blueprint will be prefixed with /api.

# the request object imported from flask contains info about the request itself     

# <class 'AssertionError'> : An AssertionError is thrown when our custom validations fail
# <class 'sqlalchemy.exc.IntegrityError'> : IntegrityError is thrown when something specific to MySQL (like a UNIQUE constraint) fails
    # try:
    #     db.add(newUser)
    #     db.commit()
    #     print('success!')
    # except AssertionError:
    #     print('validation error')
    # except sqlalchemy.exc.IntegrityError:
    #     print('mysql error')

# Keep in mind that if db.commit() fails, the connection will remain in a pending state. This doesn't seem to have any negative effects during local testing. You can try to sign up again on the front end, and the next attempt will go through just fine. In a production environment, however, those pending database connections can result in app crashes. To resolve this issue, you can roll back the last commit: db.rollback(). you won't see the benefits of calling db.rollback() in your local environment, but doing so ensures that the database won't lock up when deployed to Heroku. 