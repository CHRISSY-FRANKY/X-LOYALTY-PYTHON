from routes import main_routes # import the route manager
from flask import render_template # render your html files

@main_routes.route('/') # create the index route
def index(): 
    return render_template("index.html") # render the intro page