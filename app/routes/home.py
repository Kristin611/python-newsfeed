# home.py is a standalone file that is a module within routes package, i.e., it is a module that belongs to the routes package

from flask import Blueprint, render_template, session, redirect 
from app.models import Post
from app.db import get_db

bp = Blueprint('home', __name__, url_prefix='/')
# Blueprint() consolidates routes into a single bp object that the parent app can register later. this corresponds to using the router middleware of express.js
# see (2) below for more info

# @bp is a decorator that turns functions into routes, like the index() & login() functions
# whatever the function returns becomes the response. we are using the render_template() functio to respond with a html template
# see (3) below for more info
@bp.route('/')
def index():
    # get all posts
    db = get_db()
    posts = db.query(Post).order_by(Post.created_at.desc()).all()
    return render_template('homepage.html', posts=posts, loggedIn=session.get('loggedIn'))

@bp.route('/login')
def login():
    # not logged in yet
    if session.get('loggedIn') is None:
        return render_template('login.html')
    
    return redirect('/dashboard')

# id is the parameter in this route
@bp.route('/post/<id>')
def single(id):
    # get single post by id
    db = get_db()
    post = db.query(Post).filter(Post.id == id).one()
    return render_template('single-post.html', post=post, loggedIn=session.get('loggedIn'))

# Blueprint: This is a Flask feature that allows you to organize your application into modular components. Blueprints are a way to structure your Flask application into smaller and more manageable parts.
# render_template: This function is used to render HTML templates with the given context. It looks for HTML files in the templates folder by default.

# (2) Creating a Blueprint:
    # 'home': This is the name of the blueprint. It is used to identify the blueprint.
    # __name__: This is the name of the module or package where the blueprint is located. Flask uses this to locate the blueprint.
    # url_prefix='/': This sets a URL prefix for all routes in this blueprint. In this case, the prefix is '/', meaning the routes defined in this blueprint will be accessible from the root URL.

# (3) Defining Routes:
    # Homepage Route
        # @bp.route('/'): This decorator defines a route for the blueprint. The '/' URL means this route will be accessible from the root URL (e.g., http://localhost/).
        # index(): This is the view function that will be called when the root URL is accessed. It renders the homepage.html template.
    # Login Page Route
        # @bp.route('/login'): This decorator defines a route for the login page. The '/login' URL means this route will be accessible from http://localhost/login.
        # login(): This is the view function that will be called when the login URL is accessed. It renders the login.html template.
    # Single Post Page Route  
        # @bp.route('/post/<id>'): This decorator defines a route for a single post page. The '/post/<id>' URL means this route will be accessible from http://localhost/post/<id>, where <id> is a dynamic segment that will be passed to the single function.  
        # single(id): This is the view function that will be called when a URL like http://localhost/post/123 is accessed. The id parameter captures the value from the URL, which can be used within the function. It renders the single-post.html template.

# Summary:
#   Blueprint: Organizes routes and handlers into modular components.
#   @bp.route(): Defines a route within the blueprint.
#   render_template(): Renders HTML templates.    

# Example Use Case:
#  Homepage: Accessible at http://localhost/, renders homepage.html.
# Login Page: Accessible at http://localhost/login, renders login.html.
# Single Post Page: Accessible at http://localhost/post/<id>, renders single-post.html, where <id> is a dynamic part of the URL.

# Interestingly, you can import any variables or functions defined by Python modules into other modules. Thus, the bp object and the three route functions are all available for importing. We only care about bp, though, because the other functions are already attached to it—thanks to the @bp.route() decorator.