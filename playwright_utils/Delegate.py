from playwright.sync_api import sync_playwright

class Playwright_Delegate:

    _instance = None # singleton
    playwright = None

    @classmethod
    def get_instance(cls): # returns an instance of the caller that is saved in the caller
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        self._playwright = sync_playwright().start()
    
    def stop(self):
        self._playwright.stop()
        