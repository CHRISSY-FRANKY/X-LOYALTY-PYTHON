from flask import Flask # import libraries
import routes
import index

app = Flask(__name__) # create flask application instance

if "__main__" == __name__:
    app.register_blueprint(routes.main_routes) # add the routes
    app.run() # run flask instance