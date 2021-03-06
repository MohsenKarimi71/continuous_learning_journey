from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest


class NewVisitorTest(FunctionalTest):
    
    def test_can_add_a_new_category(self):
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
        self.assertEqual(add_new_category_link.text, "Add new category")

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
