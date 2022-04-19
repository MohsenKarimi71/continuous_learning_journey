from django.test import TestCase
from django.utils.html import escape

from posts.models import Category, Subject


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


class CategoryDetailPageTest(TestCase):
    
    def test_view_uses_correct_html(self):
       category = Category.objects.create(title="Programming")
       response = self.client.get(f"/categories/{category.id}/")
       
       self.assertTemplateUsed(response, "posts/category_detail.html")
    
    def test_view_sends_and_uses_correct_category(self):
        first_category = Category.objects.create(title="Programming")
        second_category = Category.objects.create(title="Python Programming")

        response = self.client.get(f"/categories/{first_category.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['category'].id, first_category.id)
        self.assertContains(response, first_category.title)

        response = self.client.get(f"/categories/{second_category.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['category'].id, second_category.id)
        self.assertContains(response, second_category.title)
    
    def test_view_sends_and_uses_correct_subjects_for_category(self):
        first_category = Category.objects.create(title="Programming")
        first_category_first_subject = Subject.objects.create(
            title="Python",
            description="This subject is about python programming language.",
            category=first_category
        )
        first_category_second_subject = Subject.objects.create(
            title="Jave",
            description="This subject is about Jave programming language.",
            category=first_category
        )

        second_category = Category.objects.create(title="English")
        second_category_first_subject = Subject.objects.create(
            title="Grammer",
            description="This subject is about grammer in English language.",
            category=second_category
        )
        second_category_second_subject = Subject.objects.create(
            title="Reading",
            description="This subject is about reading in English language.",
            category=second_category
        )

        response = self.client.get(f"/categories/{first_category.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, first_category_first_subject.title)
        self.assertContains(response, first_category_second_subject.title)

        self.assertNotContains(response, second_category_first_subject.title)
        self.assertNotContains(response, second_category_second_subject.title)


class AddNewSubjectPageTest(TestCase):

    def test_view_uses_correct_html(self):
        category = Category.objects.create(title="Programming")
        response = self.client.get(f"/categories/{category.id}/new/")

        self.assertTemplateUsed(response, "posts/add_new_subject.html")
    
    def test_view_sends_and_uses_correct_category(self):
        first_category = Category.objects.create(title="Pragramming")
        second_category = Category.objects.create(title="Network")

        response = self.client.get(f"/categories/{first_category.id}/new/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['category'].id, first_category.id)
        self.assertContains(response, first_category.title)

        response = self.client.get(f"/categories/{second_category.id}/new/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['category'].id, second_category.id)
        self.assertContains(response, second_category.title)
    
    def test_view_can_save_a_POST_request(self):
        category = Category.objects.create(title="Programming")
        self.client.post(
            f"/categories/{category.id}/new/",
            data={
                "new_subject_title": "Python",
                "new_subject_description": "This subject is about Python."
            }
        )

        self.assertEqual(category.subject_set.count(), 1)
        saved_subject = category.subject_set.first()
        self.assertEqual(saved_subject.title, "Python")
        self.assertEqual(saved_subject.description, "This subject is about Python.")

    def test_redirects_after_POST(self):
        category = Category.objects.create(title="Programming")
        response = self.client.post(
            f"/categories/{category.id}/new/",
            data={
                "new_subject_title": "Python",
                "new_subject_description": "This subject is about Python."
            }
        )

        self.assertRedirects(response, f"/categories/{category.id}/")

    def test_empty_title_validation_error_is_send_back_to_add_new_subject_template(self):
        category = Category.objects.create(title="Programming")
        response = self.client.post(
            f"/categories/{category.id}/new/",
            data={
                "new_subject_title": "",
                "new_subject_description": "This is some descriotion."
            }
        )
        self.assertEqual(response.status_code, 200)
        expected_error_message = escape('This field cannot be blank')
        self.assertContains(response, expected_error_message)

    def test_subject_with_empty_title_is_not_saved(self):
        category = Category.objects.create(title="Programming")
        response = self.client.post(
            f"/categories/{category.id}/new/",
            data={
                "new_subject_title": "",
                "new_subject_description": "This is some description."
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Subject.objects.count(), 0)

    def test_white_space_only_title_validation_error_is_send_back_to_add_new_subject_template(self):
        category = Category.objects.create(title="Programming")
        response = self.client.post(
            f"/categories/{category.id}/new/",
            data={
                "new_subject_title": "   ",
                "new_subject_description": "This is some descriotion."
            }
        )
        self.assertEqual(response.status_code, 200)
        expected_error_message = escape('This field cannot be blank')
        self.assertContains(response, expected_error_message)

    def test_subject_with_only_white_speces_in_title_is_ont_saved(self):
        category = Category.objects.create(title="Programming")
        response = self.client.post(
            f"/categories/{category.id}/new/",
            data={
                "new_subject_title": "   ",
                "new_subject_description": "This is some description."
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Subject.objects.count(), 0)

    def test_unique_title_validation_error_for_subjects_of_a_category_is_send_back_to_template(self):
        category = Category.objects.create(title="Programming")

        title = "some title"
        # create first subject
        response = self.client.post(f"/categories/{category.id}/new/", data={
            "new_subject_title": title,
            "new_subject_description": "This is some description."
        })
        self.assertEqual(response.status_code, 302)

        # creating second subject with same title
        response = self.client.post(f"/categories/{category.id}/new/", data={
            "new_subject_title": title,
            "new_subject_description": "Some new description."
        })
        expected_error_message = "Subject with this Title and Category already exists."
        self.assertContains(response, expected_error_message)
