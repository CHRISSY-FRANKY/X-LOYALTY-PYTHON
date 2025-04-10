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
    
    def stop(self): # stop the playwright and browser instance
        if self._browser:
            self._browser.close()
            print("Browser closed")
        if self._playwright:
            self._playwright.stop()
            print("Playwright stopped")

    def load_page(self, url, page=None): # loads page by recreating playwright instance 
        self._playwright = sync_playwright().start()
        try:
            self._browser = self._playwright.firefox.launch(headless=True) # launch new browser instance
            if not page: # create a new page
                page = self._browser.new_page()
            page.goto(url) # navigate to new url
            return page
        except Exception as e:
            print(f"Error loading page: {e}")
            return None
        