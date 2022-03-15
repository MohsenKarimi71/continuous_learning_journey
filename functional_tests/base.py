import time

from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from django.contrib.staticfiles.testing import StaticLiveServerTestCase


MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
    
    def tearDown(self):
        self.browser.quit()
    
    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (WebDriverException, AssertionError) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
