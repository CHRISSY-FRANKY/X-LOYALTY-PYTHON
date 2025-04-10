from playwright.sync_api import sync_playwright

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
        if self._playwright and not self._playwright.is_running(): # exists but not running
            self._playwright.stop()
        if not self._playwright:
            self._playwright = sync_playwright().start() # just start it
    
    def start_browser(self): # start browser if it exists but not running or not started
        if self._browser and not self._browser.is_running(): # exists but not running
            self._browser.stop()
        if not self._browser:
            self._browser = self._playwright.firefox.launch(headless=True) # just start it

    def stop(self): # stop the playwright and browser instance
        if self._browser:
            self._browser.close()
            print("Browser closed")
        if self._playwright:
            self._playwright.stop()
            print("Playwright stopped")

    def load_page(self, url, page=None): # loads page by recreating playwright instance 
        self.start_playwright()
        self.start_browser()
        try:
            page.goto(url) # navigate to new url
            return page
        except Exception as e:
            print(f"Error loading page: {e}")
            return None
        