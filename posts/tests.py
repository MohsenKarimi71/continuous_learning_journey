from unicodedata import category
from django.test import TestCase
from posts.models import Category

class HomePageTest(TestCase):
    
    def test_view_uses_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, "posts/home.html")


class AddNewCategoryPageTest(TestCase):

    def test_view_uses_correct_html(self):
        response = self.client.get('/categories/new/')
        self.assertTemplateUsed(response, "posts/add_new_category.html")
    
    def test_redirects_after_POST(self):
        response = self.client.post("/categories/new/", data={})
        self.assertRedirects(response, "/categories/")


class CategoryListPageTest(TestCase):

    def test_view_uses_correct_html(self):
        response = self.client.get("/categories/")
        self.assertTemplateUsed(response, "posts/category_list.html")


class CategoryModelTest(TestCase):
    
    def test_saving_and_retrieving_category_objects(self):
        first_category = Category()
        first_category.title = "Programming"
        first_category.save()

        second_category = Category()
        second_category.title = "English"
        second_category.save()

        saved_categories = Category.objects.all()
        self.assertEqual(saved_categories.count(), 2)
        self.assertEqual(saved_categories[0].title, "Programming")
        self.assertEqual(saved_categories[1].title, "English")
