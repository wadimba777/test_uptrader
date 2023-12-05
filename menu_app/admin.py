from django.contrib import admin

from .forms import MenuItemForm
from .models import Menu, MenuItem


class ItemInline(admin.StackedInline):
    # Inline представление для отображения связанных MenuItems
    model = MenuItem
    extra = 0
    fields = ['menu', 'title', 'parent', 'href', 'named_url']


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    # Регистрация модели Menu в админ панели
    inlines = ItemInline,


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    # Регистрация модели MenuItem в админ панели

    # Форма для выбора parent исходя из выбранного menu.
    # Предварительно необходимо сохранить новый объект с необходимым меню в селекторе.
    form = MenuItemForm
    list_display = ('menu', 'title', 'parent', 'href', 'named_url')
    fields = ['menu', 'title', 'parent', 'href', 'named_url']
    inlines = ItemInline,
