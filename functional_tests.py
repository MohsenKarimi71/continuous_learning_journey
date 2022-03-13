import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

from django.contrib.staticfiles.testing import StaticLiveServerTestCase


MAX_WAIT = 10
##############################################################################
class NewVisitorTest(StaticLiveServerTestCase):
    
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
    
    def test_can_add_a_new_category(self):
        #################### User Story 1: Adding new category ###############
        # Ali just heared about a cool site that it's users can add and
        # organize whatever they have learned in any field.
        # He goes to check that so, he opens the home page of the site:
        self.browser.get(self.live_server_url)

        # He sees that home page title & header contain:
        #   "Record what you have learned"
        self.assertEqual(self.browser.title, "Record what you have learned")
        main_header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertEqual(main_header_text, "Record what you have learned")

        # In the home page he sees a button with a text that says:
        #   "add new category"
        add_new_category_link = self.browser.find_element(By.ID, "add-new-category-link")
        self.assertEqual(add_new_category_link.text, "add new category")

        # He clicks on that button and the site goes to a new page:
        #   "adding new category" page
        add_new_category_link.click()

        # In the new page, he notices that the page title and header contain:
        #   "New Category"
        self.wait_for(lambda: self.assertEqual(
            self.browser.title, "New Category"
        ))
        
        main_header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertEqual(main_header_text, "New Category")

        # In that page he can see an input box with a palaceholder text: 
        #   "Enter a new category"
        input_box = self.browser.find_element(By.ID, "new-category-input")
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            "Enter a new category"
        )

        # He enters "programming stuffs" in the input box and hits Enter key.
        input_box.send_keys("programming stuffs")
        input_box.send_keys(Keys.ENTER)

        # The site goes to a new page:
        #   "list of added categories" page
        # Ali notices that title and header of the new page contain:
        #   "list of your categories"
        self.wait_for(lambda: self.assertEqual(
            self.browser.title, "list of your categories"
        ))
        main_header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertEqual(main_header_text, "list of your categories")

        # He can see that the page has listed his new added category:
        # '1: programming stuffs'
        categories_table = self.browser.find_element(By.ID, "categories-table")
        rows = categories_table.find_elements(By.TAG_NAME, "tr")
        self.assertIn("1: programming stuffs", [row.text for row in rows])

        # He is happy now and goes home for next user story
    ######################################################################
    def test_layout_and_styling(self):
        win_height = 768
        win_width = 1024
        # Ali goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(win_width, win_height)

        # He notices that the header text and link to add new category are
        # nicely centered
        main_header = self.browser.find_element(By.TAG_NAME, 'h1')
        self.assertAlmostEqual(
            win_width / 2,
            main_header.location['x'] + main_header.size['width'] / 2,
            delta=10
        )

        add_new_category_link = self.browser.find_element(By.ID, 'add-new-category-link')
        self.assertAlmostEqual(
            win_width / 2,
            add_new_category_link.location['x'] + add_new_category_link.size['width'] / 2,
            delta=10
        )

