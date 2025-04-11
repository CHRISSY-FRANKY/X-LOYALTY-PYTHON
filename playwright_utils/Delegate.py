from playwright.sync_api import sync_playwright
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__) # setup logging

class Playwright_Delegate:

    _instance = None # singleton
    _playwright = None
    _browser = None

    @classmethod
    def get_instance(cls): # returns an instance of the caller that is saved in the caller
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def start_playwright(self): # start playwright if it exists but not running or not started
        try:
            if self._playwright and not self._playwright.is_running(): # exists but not running
                logger.info("Playwright exists but is not running, restarting...")
                self._playwright.stop()
                self._playwright = None
        except Exception as e:
            logger.error(f"Error checking if playwright is running: {e}")
            try: # assume playwright is not running
                self._playwright.stop()
            except:
                pass
            self._playwright = None
            
        if not self._playwright:
            self._playwright = sync_playwright().start() # just start it
            logger.info("Playwright started")
    
    def start_browser(self, headless=True): # check if browser exists and is still working
        if self._browser: # if browser exists
            try:
                self._browser.contexts() # see if browser is still working
            except Exception: # restart browser if not working
                logger.info("Browser is not working, restarting...")
                self._browser.close()
                self._browser = None
        if not self._browser: # just start it
            self._browser = self._playwright.firefox.launch(headless=headless) # just start it
            logger.info("Browser started")

    def stop(self): # stop the playwright and browser instance
        if self._browser:
            self._browser.close()
            logger.info("Browser closed")
            self._browser = None
        if self._playwright:
            self._playwright.stop()
            logger.info("Playwright stopped")
            self._playwright = None

    def load_page(self, url, page=None, headless=True): # loads page by recreating playwright instance 
        self.start_playwright()
        self.start_browser(headless=headless)
        try:
            if not page:  # create a new page if none is provided
                page = self._browser.new_page()
                logger.info(f"Created new page for URL: {url}")
            page.goto(url) # navigate to new url
            logger.info(f"Navigated to URL: {url}")
            return page
        except Exception as e:
            logger.error(f"Error loading page: {e}")
            return None
        