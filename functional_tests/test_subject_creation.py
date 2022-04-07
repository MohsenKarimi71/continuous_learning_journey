from unicodedata import category
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest


class NewVisitorTest(FunctionalTest):

    def test_can_add_a_new_subject(self):
        # Ali wants to add a new subject under a category. He goes to the site home page
        self.browser.get(self.live_server_url)

        # He clicks on the add new category link
        self.wait_for(lambda:
            self.browser.find_element(By.ID, "add-new-category-link")
        ).click()

        # He types "Programming" as the title of the category and hits the ENTER key
        input_box = self.wait_for(lambda:
            self.browser.find_element(By.ID, "new-category-input")
        )
        input_box.send_keys("Programming")
        input_box.send_keys(Keys.ENTER)

        # Site goes to the list of categories page and he sees that his
        # new added category is listed there
        categories_table = self.wait_for(lambda:
            self.browser.find_element(By.ID, "categories-table")
        )
        rows = categories_table.find_elements(By.TAG_NAME, "tr")
        self.assertIn("1: Programming", [row.text for row in rows])

        # He clicks on the "Programming" category and site goes to a new page
        rows[0].find_element(By.TAG_NAME, 'a').click()
        # In the new page he notices that the page title and header is the 
        # same as category name
        self.wait_for(lambda:
            self.assertEqual(self.browser.title, "Programming")
        )
        self.assertEqual(
            self.browser.find_element(By.TAG_NAME, "h1").text,
            "Programming"
        )

        # Ali sees a button with text: "Add New subject" and clicks on it
        add_new_subject_link = self.browser.find_element(By.ID, "add-new-subject")
        self.assertEqual(add_new_subject_link.text, "Add New subject")
        add_new_subject_link.click()

        # The site goes to a new page and In the new page, he notices that the page title
        # and header contain: "New subject for Programming Category"
        self.wait_for(lambda:
            self.assertEqual(
                self.browser.title,
                "New subject for Programming Category"
        ))
        
        self.assertEqual(
            self.browser.find_element(By.TAG_NAME, 'h1').text,
            "New subject for Programming Category"
        )

        # In that page he can see a form with several inputs
        # There is a input for title with placeholder: "Enter subject Title"
        title_input = self.browser.find_element(By.ID, "subject-title")
        self.assertEqual(title_input.get_attribute("placeholder"), "Enter subject Title")

        # He enters "Python" in the input box
        title_input.send_keys("Python")

        # There is a text-area input for description with placeholder: "Enter subject description Here..."
        description_input = self.browser.find_element(By.ID, "subject-description")
        self.assertEqual(
            description_input.get_attribute("placeholder"),
            "Enter subject description Here..."
        )

        # He types some text in the text-area
        description_input.send_keys(
            """
            This subject is about Python programming language.
            Any post under this subject will be added here
            """
        )
        
        # There is a button for submitting the form with text: "Create subject"
        submit_button = self.browser.find_element(By.ID, "submit-form")
        self.assertEqual(submit_button.text, "Create subject")
        # Ali clicks submit button
        submit_button.click()

        # Site redirects to the "Programming" category page and Ali notices
        # that the title of his new added subject is listed there
        list_of_subjects = self.wait_for(lambda:
            self.browser.find_element(By.ID, "list-of-subjects")
        )
        items = list_of_subjects.find_elements(By.TAG_NAME, 'li')
        self.assertIn("1: Python", [item.text for item in items])



        

