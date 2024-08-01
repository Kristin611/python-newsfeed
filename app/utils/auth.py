from flask import session, redirect
from functools import wraps

# Defines a decorator function named login_required that takes a function func as an argument.
def login_required(func):
  # This decorator applies the wraps function to wrapped_function. This ensures that wrapped_function retains the metadata of func.
  @wraps(func)
  # Defines an inner function wrapped_function that takes any number of positional (*args) and keyword (**kwargs) arguments. This allows the wrapped function to accept any arguments that the original function accepts.
  def wrapped_function(*args, **kwargs):
    # checks if the key loggedIn in the session object is set to True. 
    # If the user is logged in (i.e., session.get('loggedIn') == True), the original function (func) is called with its original arguments (*args, **kwargs).
    if session.get('loggedIn') == True:
      return func(*args, **kwargs)
    # If the user is not logged in, the function redirects the user to the /login URL.
    return redirect('/login')
  # The login_required decorator returns the wrapped_function. This effectively replaces the original function (func) with wrapped_function, adding the login check functionality.
  return wrapped_function

# the wraps decorator from the functools module is used to preserve the original function's metadata (such as its name and docstring) when it is wrapped by another function.