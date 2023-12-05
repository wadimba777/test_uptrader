Python 3.10.2

Установка

Для настройки приложения выполните клонирование репозитория с помощью команды: git clone https://github.com/wadimba777/test_uptrader.git


Установите необходимые зависимости: pip install -r requirements.txt


Примените миграции с помощью: python manage.py migrate

Использование

!!! Модульные тесты для функции draw_menu доступны по команде
python manage.py test menu_app.tests
Он включает два теста - проверку отображения пунктов меню и уверенность в том, что количество запросов к базе данных не превышает 1.

Создание меню

Меню можно создавать через стандартный интерфейс администратора Django. Для этого перейдите на страницу http://localhost:8000/admin/menu_app/menu/, где http://localhost:8000 - адрес вашего приложения. На этой странице вы можете создать новое меню, указав его название и пункты меню. Пункты меню можно создавать в административном интерфейсе или привязывать к уже существующим моделям и их URL.

Отображение меню

Чтобы показать меню на странице, загрузите шаблонный тег:

{% load menu_tags %}

И затем в нужном месте вызовите

{% draw_menu 'main_menu' %}

где main_menu - название меню.
Тег draw_menu будет отрисовывать древовидное меню на основе элементов, созданных в административном интерфейсе.


Все, что выше выделенного пункта, развернуто. Первый уровень вложенности под выделенным пунктом также развернут.

Активный пункт меню определяется на основе URL текущей страницы.

На одной странице может быть несколько меню. Они отличаются по названию.

При клике на пункт меню происходит переход по указанному в нем URL. URL может быть задан явно или через именованный URL.

Для отрисовки каждого меню требуется ровно 1 запрос к базе данных.


