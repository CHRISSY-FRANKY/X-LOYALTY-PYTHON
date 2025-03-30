from flask import Flask # import libraries
import main_routes
from routes.index import index as index

app = Flask(__name__) # create flask application instance

if "__main__" == __name__:
    app.register_blueprint(main_routes.main_routes) # add the routes
    app.run() # run flask instance