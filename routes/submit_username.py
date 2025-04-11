from main_routes import main_routes # import the route manager 
from flask import request # request fields
from flask import render_template
from playwright_utils.Delegate import Playwright_Delegate
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__) # setup logging

def verify_username(username) -> bool:
    page = Playwright_Delegate.get_instance().load_page(f"https://x.com/{username}") # load the username
    if page is None:
        return None
    try:
        page.wait_for_selector('text="This account doesn\'t exist"', timeout=6900) 
        return False  # username doesn't exist
    except Exception as e:
        try:
            page.wait_for_selector('text="Sign in to X"', timeout=6900) 
            return True  # username exists
        except Exception as e:
            print(f"An error occured: {e}")
            return None  # connection is slow or something else

@main_routes.route("/submit_username", methods=["POST"]) # create the submit_username route 
def submit_username():
    """
    Handle the submission of a username for verification.
    
    Returns:
        str: The rendered template based on the verification result
    """
    username = request.form["username"] # get username from form
    logger.info(f"Verifying username: {username}")
    
    username_exists = verify_username(username)
    
    if username_exists is True: # username exists
        logger.info(f"Username exists: {username}")
        return render_template("username_existant.html")
    elif username_exists is False: # username doesn't exist
        logger.info(f"Username does not exist: {username}")
        return render_template("username_inexistant.html")
    else: # connection error or unknown issue
        logger.warning(f"Connection error or unknown issue for username: {username}")
        return render_template("connection_error.html")
   