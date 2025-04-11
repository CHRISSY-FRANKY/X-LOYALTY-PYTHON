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
        try:
            if self._playwright and not self._playwright.is_running(): # exists but not running
                self._playwright.stop()
                self._playwright = None
        except Exception as e:
            print(f"Error checking if playwright is running: {e}")
            try: # assume playwright is not running
                self._playwright.stop()
            except:
                pass
            self._playwright = None
        if not self._playwright:
            self._playwright = sync_playwright().start() # just start it
            print("Playwright started")
    
    def start_browser(self): # check if browser exists and is still working
        if self._browser: # if browser exists
            try:
                self._browser.contexts() # see if browser is still working
            except Exception: # restart browser if not working
                print("Browser is not working, restarting...")
                self._browser.close()
                self._browser = None
        if not self._browser: # just start it
            self._browser = self._playwright.firefox.launch(headless=True) # just start it
            print("Browser started")

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
            if not page:  # create a new page if none is provided
                page = self._browser.new_page()
            page.goto(url) # navigate to new url
            return page
        except Exception as e:
            print(f"Error loading page: {e}")
            return None
        