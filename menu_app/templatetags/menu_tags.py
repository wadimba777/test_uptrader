from django import template
from django.urls import reverse_lazy, NoReverseMatch

from menu_app.models import MenuItem


register = template.Library()


@register.inclusion_tag(filename='menu_app/dropdown_menu.html', takes_context=True)
def draw_menu(context, menu_name: str) -> dict:
    """
    Шаблонный тег draw_menu используется для отрисовки выпадающего меню,
    который принимает два аргумента: context и menu_name. Он также использует тег menu_item для рекурсивной отрисовки
    меню без заданной максимальной вложенности.

    :param context: context from view render
    :param menu_name: str name
    :return: dict() for template writing
    """

    # Первым делом, мы получаем текущий URL-адрес запроса и
    # загружаем все элементы меню с заданным именем из базы данных.
    request_url = context['request'].build_absolute_uri()
    raw_menu_items = MenuItem.objects.filter(menu__name=menu_name)

    items_dict = dict()
    root_items = list()
    current_items = list()

    # Далее, мы создаем словарь items_dict, который содержит информацию обо всех элементах меню.
    # Этот словарь используется для построения древовидной структуры.

    for i_item in raw_menu_items:
        try:
            item_url = i_item.href or (context['request'].build_absolute_uri(reverse_lazy(i_item.named_url))
                                       if reverse_lazy(i_item.named_url) else None)
        except NoReverseMatch:
            item_url = None

        items_dict[i_item.id] = {
            'menu_name': menu_name,
            'item_id': i_item.id,
            'title': i_item.title,
            'parent_id': i_item.parent_id,
            'href': item_url,
            'expand': False,
            'children': list()
        }

        # Добавляем активные элементы в список активных элеметов,
        # чтобы сократить цикл для определения активных элементов.
        if request_url.endswith(str(item_url)):
            current_items.append(i_item.id)

    # Создаем древовидную структуру на базе parent-child отношений.
    for item_id, item_value in items_dict.items():
        item_parent = items_dict[item_id]['parent_id']
        if item_parent is not None:
            items_dict[item_parent]['children'].append(item_value)
        else:
            root_items.append(item_value)

    # Находим все активные элементы и раскрываем списки в которые они вложены, и те списки которые находятся под ними.
    for current_item_id in current_items:
        item = items_dict[current_item_id]

        item['expand'] = True

        parent = item['parent_id']

        while parent is not None:
            items_dict[parent]['expand'] = True
            parent = items_dict[parent]['parent_id']

    return {'menu_items': root_items, 'menu_name': menu_name}


@register.inclusion_tag(filename='menu_app/item-list.html')
def menu_item(items: list) -> dict:
    # Используется для рекурсивной отрисовки всех вложенных списков.
    return {'item_list': items}
