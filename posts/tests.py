from urllib import response
from django.test import TestCase

class HomePageTest(TestCase):
    
    def test_view_uses_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, "posts/home.html")


class AddNewCategoryPageTest(TestCase):

    def test_view_uses_correct_html(self):
        response = self.client.get('/categories/new/')
        self.assertTemplateUsed(response, "posts/add_new_category.html")
    