from django import forms
from .models import MenuItem


class MenuItemForm(forms.ModelForm):
    """
    Форма позволяет выбирать поле parent только исходя из выбранного menu.
    """

    class Meta:
        model = MenuItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs:

            if kwargs['instance'] is not None:
                # Получает выбранное menu_id
                menu_id = kwargs['instance'].menu_id
            else:
                menu_id = None

            if menu_id:
                # Если меню выбрано, предоставляет выбор из объектов related к этому меню
                self.fields['parent'].queryset = MenuItem.objects.filter(menu_id=menu_id)
            else:
                # Если меню не выбрано вставляет в chosefield пустой queryset.
                self.fields['parent'].queryset = MenuItem.objects.none()
