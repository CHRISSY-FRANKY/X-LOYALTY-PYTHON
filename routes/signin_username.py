from main_routes import main_routes # import the route manager 
from flask import redirect
from playwright_utils.Delegate import Playwright_Delegate
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__) # setup logging
