from .home import bp as home
from .dashboard import bp as dashboard
from .api import bp as api

# the .home syntax directs the program to find the module named home in the current directory. Next, we want to import the bp object, but we rename it home as part of the import process