from main_routes import main_routes
from flask import request
from flask import render_template
from playwright_utils.Delegate import Playwright_Delegate
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__) # setup logging

def extract_following_count(username, followingCount):
    delegate = Playwright_Delegate.get_instance()
    page = delegate.load_page(f"https://x.com/{username}/following", headless=False)
    logger.info(f"LOADING https://x.com/{username}/following")

    page.wait_for_url(f"https://x.com/i/flow/login?redirect_after_login=%2F{username}") # wait for login page
    logger.info(f"LOADED https://x.com/i/flow/login?redirect_after_login=%2F{username}")

    page.wait_for_url(f"https://x.com/{username}") # wait for profile page
    logger.info(f"LOADED https://x.com/{username}")

    page.goto(f"https://x.com/{username}/following")
    logger.info(f"REDIRECTED TO https://x.com/{username}/following")
    
    page.wait_for_url(f"https://x.com/{username}/following")
    logger.info(f"LOADED https://x.com/{username}/following")
    
    page.wait_for_load_state("domcontentloaded")

@main_routes.route("/get_advanced_statistics", methods=["POST"])
def get_advanced_statistics():
    """
    This route is used to get the advanced statistics of the user
    """
    username = request.form["username"]
    followersCount = request.form["followers"]
    followingCount = request.form["following"]
    extract_following_count(username, followingCount)
    
    
    return "^-^"
