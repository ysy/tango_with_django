from django.test import TestCase
from django.core.urlresolvers import reverse
from rango.models import Category


class CategoryMethodTests(TestCase):
    def test_ensure_category_views_are_postive(self):
        """
            views of Category should be >= 0
        :return:
        """
        cat = Category(name='test', views=-1, likes=0)
        cat.save()
        self.assertEqual((cat.views >= 0), True)

    def test_ensure_category_likes_are_postive(self):
        cat = Category(name='test', views=0, likes=-1)
        cat.save()
        self.assertEqual((cat.likes >= 0), True)

    def test_slug_createor(self):
        cat = Category(name='Some Random Name')
        cat.save()
        self.assertEqual(cat.slug, 'some-random-name')


def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c


class IndexViewTests(TestCase):

    def test_index_view_with_no_categories(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['categories'], [])

    def test_index_view_with_categories(self):
        add_cat("test", 1, 1)
        add_cat("test1", 1, 1)
        add_cat("test2", 1, 1)
        add_cat("test3", 1, 1)
        add_cat("test4", 1, 1)

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        num_cats = len(response.context['categories'])
        self.assertEqual(num_cats, 5)
