from flask import Blueprint, request, jsonify, session
from app.models import User, Post, Comment, Vote 
# establish a connection to the db
from app.db import get_db
from sqlalchemy.exc import SQLAlchemyError
import sys
from app.utils.auth import login_required

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

# create a comment route
@bp.route('/comments', methods=['POST'])
@login_required
def comment():
    # capture posted data with get_json()
    data = request.get_json()
    # connecting to the db
    db = get_db()

    # bc the creation of comment can fail, we want to wrap it in a try..except statement
    try:
        # create new comment
        newComment = Comment(
            comment_text = data['comment_text'],
            post_id = data['post_id'],
            user_id = session.get('user_id')
        )

        db.add(newComment)
        # db.commit() performs INSERT statement
        db.commit()
    except:
        print(sys.exc_info()[0])

        # discards the pending commit if it fails
        db.rollback()
        return jsonify(message = 'Comment failed'), 500
    
    # return newly created ID if the comment creation succeeded. 
    return jsonify(id = newComment.id) 

# update a post with a vote route
@bp.route('/posts/upvote', methods=['PUT'])
@login_required
def upvote():
    data = request.get_json()
    db = get_db()

    try:
        # create a new vote with incoming id and session id
        newVote = Vote(
            post_id = data['post_id'],
            user_id = session.get('user_id')
        )

        db.add(newVote)
        db.commit()
    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Upvote failed'), 500
    
    return '', 204

# creat a post route
@bp.route('/posts', methods=['POST'])
@login_required
def create():
    data = request.get_json()
    db = get_db()

    try:
        # create a new post
        newPost = Post(
            title = data['title'],
            post_url = data['post_url'],
            user_id = session.get('user_id')
        )

        db.add(newPost)
        db.commit()
    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Post failed'), 500
    
    return jsonify(id = newPost.id)

# update a post
@bp.route('/posts/<id>', methods=['PUT'])
@login_required
def update(id):
    data = request.get_json()
    db = get_db()

    try:
        # query the db for a post with a specific id 
        post = db.query(Post).filter(Post.id == id).one()
        # Update the title of the post with the new title from the data dictionary; see (3) below for explanation of the dictionary vs. object instance in python/flask
        post.title = data['title']
        db.commit()
    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Post not found'), 500
    
    return '', 204

# delete posts route
@bp.route('/posts/<id>', methods=['DELETE'])
@login_required
def delete(id):
    db = get_db()

    try:
        # delete post from db
        db.delete(db.query(Post).filter(Post.id == id).one())
        db.commit()
    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Post not found'), 404
    
    return '', 204
        
        


        
        
    




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

# (3) The data variable is a dictionary--it contains new data you want to update in the Post object, for example, data['title']accesses the value associated with the key 'title' in the dictionary. On the other hand, 'post' is an object instance of the 'Post' class, representing a row in the Post table. We use dot notation (post.title) to access and update the title attribute of the post object. Understanding this distinction is important for correctly manipulating data within your application. When working with dictionaries, you need to use bracket notation to access or modify values. When working with objects, you use dot notation to access or modify attributes.