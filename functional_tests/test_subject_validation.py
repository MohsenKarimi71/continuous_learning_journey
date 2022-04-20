from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest

    
class SubjectValidationTest(FunctionalTest):

    def create_category_and_navigate_to_subject_creation_form(self, title):
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.ID, "add-new-category-link").click()

        input_box = self.browser.find_element(By.ID, "new-category-input")
        input_box.send_keys(title)
        input_box.send_keys(Keys.ENTER)

        # The site redirects to the list of categories page
        # He clicks on the link of his new added category
        categories_table = self.wait_for(lambda:
            self.browser.find_element(By.ID, "categories-table")
        )
        rows = categories_table.find_elements(By.TAG_NAME, "tr")
        category_link = rows[0].find_element(By.TAG_NAME, "a")
        category_link.click()

        # Site goes to the page of new added category and
        # Ali clicks on the add new subject button
        self.wait_for(lambda:
            self.browser.find_element(By.ID, "add-new-subject")
        ).click()

    def test_can_not_add_subject_with_empty_title(self):
        # Ali goes to add a new subject under a category
        # He adds a new category
        self.create_category_and_navigate_to_subject_creation_form("Programming")

        # The site goes to the subject creation form page
        # Ali leaves the title input empty and fill description input
        # with some text
        self.wait_for(lambda:
            self.browser.find_element(By.ID, "subject-description")
        ).send_keys("some description for this subject with empty title!")

        
        # Finally he clicks on the "Create subject" button and submits the form
        self.browser.find_element(By.ID, "submit-form").click()
        
        # He faces a message that says a subject title can not be empty
        self.wait_for(lambda: self.assertIn(
            "This field cannot be blank.",
            self.browser.find_element(By.CSS_SELECTOR, ".invalid-feedback").text
            )
        )

    def test_can_not_add_subject_with_white_spaces_only_title(self):
        # Ali goes to add a new subject under a category
        # He adds a new category
        self.create_category_and_navigate_to_subject_creation_form("Programming")

        # The site goes to the subject creation form page
        # Ali enters "   " in the title input and fill description input
        # with some text
        self.wait_for(lambda:
            self.browser.find_element(By.ID, "subject-title")
        ).send_keys("   ")

        self.browser.find_element(By.ID, "subject-description").send_keys(
            "This is some description...!"
        )

        # Finally he clicks on the "Create subject" button and submits the form
        self.browser.find_element(By.ID, "submit-form").click()
        
        # He faces a message that says a subject title can not be empty
        self.wait_for(lambda: self.assertIn(
            "This field cannot be blank.",
            self.browser.find_element(By.CSS_SELECTOR, ".invalid-feedback").text
            )
        ) 

    def test_can_not_add_multiple_subject_with_same_title_under_a_category(self):
        # Ali goes to add a new subject under a category
        # He adds a new category
        self.create_category_and_navigate_to_subject_creation_form("Programming")

        # The site goes to the subject creation form page
        # Ali fills in the title input and description input
        # with some text
        self.wait_for(lambda:
            self.browser.find_element(By.ID, "subject-title")
        ).send_keys("Python")

        self.browser.find_element(By.ID, "subject-description").send_keys(
            "This is some description...!"
        )

        # He clicks on the "Create subject" button and submits the form
        self.browser.find_element(By.ID, "submit-form").click()
        
        # Site redirects to the category detail page and ali sees the new added subject
        # Ali clicks on the add new subject button again to add another subject
        self.wait_for(lambda: 
            self.browser.find_element(By.ID, "add-new-subject")
        ).click()

        # The site goes to the subject creation form page
        # Ali fills in the title input same as previous subject's title and description input
        # with some text
        self.wait_for(lambda:
            self.browser.find_element(By.ID, "subject-title")
        ).send_keys("Python")

        self.browser.find_element(By.ID, "subject-description").send_keys(
            "Some different description...!"
        )

        # He clicks on the "Create subject" button and submits the form
        self.browser.find_element(By.ID, "submit-form").click()

        # The page shows an error message that title of subjects of a category can not be equal
        self.wait_for(lambda: self.assertIn(
            "Subject with this Title and Category already exists.",
            self.browser.find_element(By.CSS_SELECTOR, ".invalid-feedback").text
            )
        )
