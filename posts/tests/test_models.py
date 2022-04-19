from django.core.exceptions import ValidationError
from django.test import TestCase

from posts.models import Category, Subject


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


class SubjectModelTest(TestCase):
    
    def test_saving_and_retrieving_subject_objects(self):
        first_category = Category()
        first_category.title = "Programming"
        first_category.save()

        first_category_first_subject = Subject(
            title = "Python",
            description = "about python programming language",
            category = first_category
        )
        first_category_first_subject.save()

        first_category_second_subject = Subject(
            title = "Java",
            description = "about Java programming language",
            category = first_category
        )
        first_category_second_subject.save()

        second_category = Category()
        second_category.title = "English"
        second_category.save()

        second_category_first_subject = Subject(
            title = "Vocabulary",
            description = "about vocabulries of English language",
            category = second_category
        )
        second_category_first_subject.save()

        second_category_second_subject = Subject(
            title = "Grammar",
            description = "about grammar of English language",
            category = second_category
        )
        second_category_second_subject.save()

        saved_subjects = Subject.objects.all()
        first_category_subjects = saved_subjects.filter(category=first_category)
        second_category_subjects = saved_subjects.filter(category=second_category)

        self.assertEqual(saved_subjects.count(), 4)
        self.assertEqual(first_category_subjects.count(), 2)
        self.assertEqual(second_category_subjects.count(), 2)
        
        self.assertEqual(first_category_subjects[0].title, "Python")
        self.assertEqual(first_category_subjects[1].title, "Java")

        self.assertEqual(second_category_subjects[0].title, "Vocabulary")
        self.assertEqual(second_category_subjects[1].title, "Grammar")
    
    def test_can_not_save_subject_with_empty_title(self):
        category = Category(title="Programming")
        category.save()

        subject = Subject(
            title="",
            description="subject with empty title!",
            category=category
        )
        with self.assertRaises(ValidationError):
            subject.full_clean()
            subject.save()
        self.assertEqual(Subject.objects.count(), 0)

    def test_can_not_save_multiple_subjects_for_a_category_with_same_title(self):
        category = Category(title="Programming")
        category.save()

        first_subject = Subject(
            title="Python",
            description="about python!",
            category=category
        )
        first_subject.full_clean()
        first_subject.save()

        second_subject = Subject(
            title="Python",
            description="another subject about python!",
            category=category
        )
        with self.assertRaises(ValidationError):
            second_subject.full_clean()
            second_subject.save()
        self.assertEqual(Subject.objects.count(), 1)
    
    def test_can_save_multiple_subject_with_same_title_for_different_categories(self):
        first_category = Category.objects.create(title="Java")
        second_category = Category.objects.create(title="Python")

        first_category_subject = Subject(
            title="OOP",
            description="about OOP in Java",
            category=first_category
        )

        first_category_subject.full_clean()
        first_category_subject.save()

        second_category_subject = Subject(
            title="OOP",
            description="about OOP in Python",
            category=second_category
        )

        second_category_subject.full_clean()
        second_category_subject.save()

        self.assertEqual(Subject.objects.count(), 2)
