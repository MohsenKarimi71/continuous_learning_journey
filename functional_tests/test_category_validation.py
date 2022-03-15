from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest

MAX_WAIT = 10


class CategoryValidationTest(FunctionalTest):

    def test_can_not_add_category_with_empty_title(self):
        # Ali goes to add a new category page
        self.browser.get(self.live_server_url)
        add_new_category_link = self.browser.find_element(By.ID, "add-new-category-link")
        add_new_category_link.click()

        # He tries to add a new category that with empty title
        # So he hits ENTER key without typing any thing in the input field
        input_box = self.browser.find_element(By.ID, "new-category-input")
        input_box.send_keys(Keys.ENTER)

        # He faces a message that says a category title can not be empty
        self.wait_for(lambda: self.assertIn(
            "This field cannot be blank.",
            self.browser.find_element(By.CSS_SELECTOR, ".invalid-feedback").text
            )
        )

    def test_can_not_add_category_with_white_spaces_only_title(self):
        # Ali goes to add a new category page
        self.browser.get(self.live_server_url)
        add_new_category_link = self.browser.find_element(By.ID, "add-new-category-link")
        add_new_category_link.click()

        # He tries to add a new category with a non empty title
        # that contains only a space
        input_box = self.browser.find_element(By.ID, "new-category-input")
        input_box.send_keys(" ")
        input_box.send_keys(Keys.ENTER)

        # He faces a message that says a category title can not be empty
        self.wait_for(lambda: self.assertIn(
            "This field cannot be blank.",
            self.browser.find_element(By.CSS_SELECTOR, ".invalid-feedback").text
            )
        )

    def test_can_not_add_multiple_categories_with_same_title(self):
        # Ali goes to add a new category page
        self.browser.get(self.live_server_url)
        add_new_category_link = self.browser.find_element(By.ID, "add-new-category-link")
        add_new_category_link.click()

        # He tries to add a new category
        input_box = self.browser.find_element(By.ID, "new-category-input")
        input_box.send_keys("new category")
        input_box.send_keys(Keys.ENTER)

        categories_table = self.wait_for(lambda: 
            self.browser.find_element(By.ID, "categories-table")
        )
        rows = categories_table.find_elements(By.TAG_NAME, "tr")
        self.assertIn("1: new category", [row.text for row in rows])

        # He goes back to the previous page
        self.browser.back()
        
        # Now he tries to add a new category with the same title as previous category's
        input_box = self.wait_for(lambda: 
            self.browser.find_element(By.ID, "new-category-input")
        )
        input_box.clear()
        input_box.send_keys("new category")
        input_box.send_keys(Keys.ENTER)

        # He faces a message that says a category with this title is already created
        self.wait_for(lambda: 
            self.assertIn(
                "Category with this Title already exists.",
                self.browser.find_element(By.CSS_SELECTOR, ".invalid-feedback").text
            )
        )
