from playwright.sync_api import sync_playwright

class Playwright_Delegate:

    _instance = None # singleton
    playwright = None

    @classmethod
    def get_instance(cls): # returns an instance of the caller that is saved in the caller
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self): # initialises the playwright instance
        self._playwright = sync_playwright().start()
    
    def stop(self): # stop the playwright instance
        self._playwright.stop()

    def load_page(self, url, page=None): # loads a page by creating one and/or navigating to a url 
        try:
            browser = self._playwright.firefox.launch(headless=False)
            page = browser.new_page()
            page.goto(url)
            return page
        except Exception as e:
            return None
        