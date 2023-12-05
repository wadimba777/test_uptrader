from django.test import TestCase, RequestFactory
from django.template import Context, Template
from django.urls import reverse

from .models import MenuItem


class DrawMenuTestCase(TestCase):
    # Указание фикстур для тестов
    fixtures = [
        'menu-fixture.json',
        'menuitem-fixture.json',
    ]

    def setUp(self):
        # Создаём RequestFactory для генерации request в context по странице main-page
        self.request_factory = RequestFactory()
        self.request = self.request_factory.get(reverse('main-page'))

    def test_get_menu(self):
        name = "main_menu"
        context = Context({'request': self.request})
        template = Template("{% load menu_tags %}{% draw_menu 'main_menu' %}")

        rendered = template.render(context)

        # Проверяем что все необходимые пункты меню отрисованы
        for i_item in MenuItem.objects.filter(menu__name=name):
            self.assertIn(i_item.title, rendered)

    def test_one_query(self):
        # Тест на количество запросов к БД
        with self.assertNumQueries(1):
            context = Context({'request': self.request})
            template = Template("{% load menu_tags %}{% draw_menu 'main_menu' %}")
            template.render(context)
