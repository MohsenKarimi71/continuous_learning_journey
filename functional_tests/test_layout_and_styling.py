from selenium.webdriver.common.by import By

from functional_tests.base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
    
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
