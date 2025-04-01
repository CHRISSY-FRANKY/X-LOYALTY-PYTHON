from main_routes import main_routes # import the route manager 
from flask import request # request fields
from flask import render_template
from playwright_utils.Delegate import Playwright_Delegate

def verify_username(username) -> bool:
   pass

@main_routes.route("/submit_username", methods=["POST"]) # create the submit_username route 
def submit_username():
    username = request.form["username"]
    print(username) # print the username
    print(verify_username(username))
    page = Playwright_Delegate.get_instance().load_page(f"https://x.com/{username}")
    if page is None:
        return render_template("username_existant.html")
    else:
        return render_template("username_error.html")