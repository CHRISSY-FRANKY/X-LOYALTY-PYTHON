from flask import Flask # import libraries
import routes

app = Flask(__name__) # create flask application instance

if "__main__" == __name__:
    app.run() # run flask instance