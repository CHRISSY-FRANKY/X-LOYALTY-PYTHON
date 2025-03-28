from routes import main_routes # import the route manager

@main_routes.route('/') # create the index route
def index(): 
    return "Welcome to XLoyalty!" # render the intro page