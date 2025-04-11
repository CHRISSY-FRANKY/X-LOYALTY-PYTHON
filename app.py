from flask import Flask # import libraries
import main_routes
from routes.index import index as index
from routes.submit_username import submit_username as submit_username
from routes.signin_username import signin_username as signin_username

app = Flask(__name__) # create flask application instance

if "__main__" == __name__:
    app.register_blueprint(main_routes.main_routes) # add the routes
    app.run() # run flask instance