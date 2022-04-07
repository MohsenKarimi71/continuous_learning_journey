from django.core.exceptions import ValidationError
from django.test import TestCase

from posts.models import Category


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
    
    def test_can_not_save_category_with_empty_title(self):
        category = Category(title='')
        with self.assertRaises(ValidationError):
            category.save()
            category.full_clean()
    
    def test_can_not_save_multiple_categoris_with_same_name(self):
        Category.objects.create(title="some title")
        with self.assertRaises(ValidationError):
            second_category = Category(title= "some title")
            second_category.full_clean()
