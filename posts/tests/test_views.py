from django.test import TestCase
from django.utils.html import escape

from posts.models import Category


class HomePageTest(TestCase):
    
    def test_view_uses_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, "posts/home.html")


class AddNewCategoryPageTest(TestCase):

    def test_view_uses_correct_html(self):
        response = self.client.get('/categories/new/')
        self.assertTemplateUsed(response, "posts/add_new_category.html")

    def test_view_can_save_a_POST_request(self):
        self.client.post("/categories/new/", data={
            'new_category_title': 'Programming'
        })
        self.assertEqual(Category.objects.count(), 1)
        saved_object = Category.objects.first()
        self.assertEqual(saved_object.title, 'Programming')
    
    def test_redirects_after_POST(self):
        response = self.client.post("/categories/new/", data={
            'new_category_title': 'some category'
        })
        self.assertRedirects(response, "/categories/")
    
    def test_empty_title_validation_error_is_send_back_to_add_new_category_template(self):
        response = self.client.post('/categories/new/', data={
            'new_category_title': ''
        })
        self.assertEqual(response.status_code, 200)
        expected_error_message = escape('This field cannot be blank')
        self.assertContains(response, expected_error_message)
    
    def test_category_with_empty_title_is_not_saved(self):
        self.client.post('/categories/new/', data={
            'new_category_title': ''
        })
        self.assertEqual(Category.objects.all().count(), 0)
    
    def test_white_space_only_title_validation_error_is_send_back_to_add_new_category_template(self):
        response = self.client.post('/categories/new/', data={
            'new_category_title': ' '
        })
        self.assertEqual(response.status_code, 200)
        expected_error_message = escape('This field cannot be blank')
        self.assertContains(response, expected_error_message)
    
    def test_category_with_only_white_speces_in_title_is_ont_saved(self):
        self.client.post('/categories/new/', data={
            'new_category_title': ' '
        })
        self.assertEqual(Category.objects.all().count(), 0)

    def test_unique_title_validation_error_is_send_back_to_add_new_category_template(self):
        title = "some title"
        self.client.post("/categories/new/", data={
            "new_category_title": title
        })

        response = self.client.post("/categories/new/", data={
            "new_category_title": title
        })

        self.assertEqual(response.status_code, 200)
        expected_error_message = "Category with this Title already exists"
        self.assertContains(response, expected_error_message)

    def test_category_with_unique_title_validation_error_is_not_saved(self):
        title = "some title"
        response = self.client.post("/categories/new/", data={
            "new_category_title": title
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Category.objects.all().count(), 1)

        response = self.client.post("/categories/new/", data={
            "new_category_title": title
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Category.objects.all().count(), 1)


class CategoryListPageTest(TestCase):

    def test_view_uses_correct_html(self):
        response = self.client.get("/categories/")
        self.assertTemplateUsed(response, "posts/category_list.html")
    
    def test_view_displays_categoris(self):
        Category.objects.create(title="Programming")
        Category.objects.create(title="English")

        response = self.client.get("/categories/")

        self.assertContains(response, "Programming")
        self.assertContains(response, "English")
