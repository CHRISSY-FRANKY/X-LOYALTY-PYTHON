from main_routes import main_routes
from flask import request
from flask import render_template
from playwright_utils.Delegate import Playwright_Delegate
import logging
import time
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__) # setup logging

def extract_following_usernames(username, following_count):
    delegate = Playwright_Delegate.get_instance() # load username following page
    page = delegate.load_page(f"https://x.com/{username}/following", headless=False)
    logger.info(f"LOADING https://x.com/{username}/following")

    page.wait_for_url(f"https://x.com/i/flow/login?redirect_after_login=%2F{username}") # wait for login page
    logger.info(f"LOADED https://x.com/i/flow/login?redirect_after_login=%2F{username}")

    page.wait_for_url(f"https://x.com/{username}") # wait for profile page
    logger.info(f"LOADED https://x.com/{username}")

    page.goto(f"https://x.com/{username}/following") # redirect to following page
    logger.info(f"REDIRECTED TO https://x.com/{username}/following")
    
    page.wait_for_url(f"https://x.com/{username}/following")
    logger.info(f"LOADED https://x.com/{username}/following")
    
    page.wait_for_load_state("domcontentloaded")

    total_count = 0 # initialize total count
    following_usernames = set() # initialize found usernames set
    while total_count < following_count: # loop until total count is equal to following count
        while True: # loop until element is removed
            element = page.query_selector('.css-175oi2r.r-vacyoi.r-ttdzmv') # locate element
            if element:
                element.evaluate("element => element.remove()") # remove element
            else:
                break
        elements = page.locator(".css-1jxf684.r-bcqeeo.r-1ttztb7.r-qvutc0.r-poiln3") # located elements
        element_count = elements.count() # get count of matching elements on the current page
        for i in range(element_count): # iterate over the elements
            element = elements.nth(i)
            text_color = page.evaluate( "(element) => window.getComputedStyle(element).color", element.element_handle()) # get text color
            if text_color == "rgb(29, 155, 240)": # skip elements with the text color rgb(29, 155, 240)
                logger.debug(f"Skipping element with text color {text_color}")
                continue
            text = element.text_content().strip()  # clean text
            if text and text[0] == '@' and username not in text:  # only add non-empty text
                following_usernames.add(text)
        total_count = len(following_usernames) # update total count with the number of unique usernames found
        logger.info(f"Currently found {total_count} unique usernames")
        if total_count >= following_count: # if we've found enough usernames, break the loop
            break
        page.evaluate("window.scrollBy(0, window.innerHeight)") # scroll down to load more elements
        time.sleep(1) # wait for new content to load
    logger.info(f"Found {total_count} elements (unique usernames)")
    return following_usernames

@main_routes.route("/get_advanced_statistics", methods=["POST"])
def get_advanced_statistics():
    """
    This route is used to get the advanced statistics of the user
    """
    username = request.form["username"]
    followersCount = request.form["followers"]
    followingCount = request.form["following"]
    following_usernames = extract_following_usernames(username, int(followingCount))
    return following_usernames
