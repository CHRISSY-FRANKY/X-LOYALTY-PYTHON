from main_routes import main_routes # import the route manager 
from flask import request # request fields

@main_routes.route("/submit_username", methods=["POST"]) # create the submit_username route 
def submit_username():
    username = request.form["username"]
    print(username) # print the username
    return "<div>^-^</div>"