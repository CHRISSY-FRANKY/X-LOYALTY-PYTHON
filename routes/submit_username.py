from main_routes import main_routes # import the route manager 
from flask import request # request fields
from flask import render_template
from playwright_utils.Delegate import Playwright_Delegate
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__) # setup logging

def verify_username(username) -> bool:
    """
    Verify if a Twitter/X username exists by checking the profile page.
    
    Args:
        username (str): The username to verify
        
    Returns:
        bool: True if the username exists, False if it doesn't, None if there was an error
    """
    delegate = Playwright_Delegate.get_instance()
    page = None
    
    try:
        page = delegate.load_page(f"https://x.com/{username}") # load the username page
        if page is None:
            logger.error(f"Failed to load page for username: {username}")
            return None
            
        try: # check if the account doesn't exist
            page.wait_for_selector('text="This account doesn’t exist"', timeout=6900)
            logger.info(f"Username does not exist: {username}")
            return False  # username doesn't exist
        except Exception:
            try: # check if the account exists (by looking for the sign-in prompt)
                page.wait_for_selector('text="Sign in to X"', timeout=6900)
                logger.info(f"Username exists: {username}")
                return True  # username exists
            except Exception as e:
                logger.error(f"Error checking for username existence: {e}")
                return None  # connection is slow or something else
                
    except Exception as e:
        logger.error(f"Error verifying username: {e}")
        return None
    finally:
        try: # stop the delegate to clean up resources
            delegate.stop()
        except Exception as e:
            logger.error(f"Error stopping delegate: {e}")

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
        return render_template("username_existant.html", username=username)
    elif username_exists is False: # username doesn't exist
        logger.info(f"Username does not exist: {username}")
        return render_template("username_inexistant.html", username=username)
    else: # connection error or unknown issue
        logger.warning(f"Connection error or unknown issue for username: {username}")
        return render_template("connection_error.html", username=username)
   