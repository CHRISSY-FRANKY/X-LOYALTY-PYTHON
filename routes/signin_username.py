from main_routes import main_routes # import the route manager 
from flask import request
from flask import render_template
from playwright_utils.Delegate import Playwright_Delegate
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__) # setup logging

def extract_counts(text):
    """
    Extract followers and following counts from the text.
    
    Args:
        text (str): The text containing followers and following counts.
        
    Returns:
        dict: A dictionary with 'following' and 'followers' counts.
    """
    parts = text.split("Following") # split the text by "Following"
    
    following = int(parts[0].strip()) # get the following count
    
    followers = int(parts[1].split("Followers")[0].strip()) # get the followers count
    
    return {
        'following': following,
        'followers': followers
    }

def build_statistics_summary(counts):
    """
    Create a summary about loyal or unloyal users based on follower and following counts.
    
    Args:
        counts (dict): A dictionary with 'following' and 'followers' counts.
        
    Returns:
        str: A message about the follower and following statistics of the user.
    """
    followers = counts['followers'] # get the counts
    following = counts['following']
    
    diff = abs(followers - following) # get the difference
    
    loyalty_type = "loyal" if followers > following else "unloyal" # determine if the users are loyal or unloyal
    
    message = ( # build the message
        f"You have {followers} followers and you are following {following}.<br>"
        f"You potentially have {diff} {loyalty_type} users."
    )
    
    return message

@main_routes.route("/signin_username", methods=["POST"])
def signin_username():
    """
    This route is used to sign in to a username and get the followers and following counts
    """
    username = request.form["username"]
    delegate = Playwright_Delegate.get_instance()

    page = delegate.load_page(f"https://x.com/{username}", headless=False) # load profile page
    logger.info(f"LOADED https://x.com/{username}")

    page.wait_for_url(f"https://x.com/i/flow/login?redirect_after_login=%2F{username}") # wait for login page
    logger.info(f"LOADED https://x.com/i/flow/login?redirect_after_login=%2F{username}")
    
    page.wait_for_url(f"https://x.com/{username}") # wait for profile page
    logger.info(f"LOADED https://x.com/{username}")
    page.wait_for_load_state("domcontentloaded") # wait for page to load
    
    element = page.query_selector(".css-175oi2r.r-13awgt0.r-18u37iz.r-1w6e6rj") # find element
    
    try:   
        if element: # get followers and following counts
            text = element.text_content().strip()
            logger.info(f"Found element with text: {text}")
            
            counts = extract_counts(text) # extract the counts from the text
            logger.info(f"Extracted counts: {counts}")
            
            return build_statistics_summary(counts)
        else: # if element not found
            logger.warning("Element not found with the specified class")
            return render_template("connection_error.html") 
    except Exception as e: # handle errors
        logger.error(f"Error: {e}")
        return render_template("connection_error.html")
    finally: # clean up resources
        try:
            delegate.stop()
        except Exception as e:
            logger.error(f"Error stopping delegate: {e}")
   
    
