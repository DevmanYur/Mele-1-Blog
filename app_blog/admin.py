from django.contrib import admin
from .models import Post, Comment

# Декоратор
# @admin.register() выполняет ту же функцию, что и функция admin.site.register()
# которую вы заменили, регистрируя декорируемый им класс ModelAdmin.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    # Атрибут list_display позволяет задавать поля модели, которые вы хотите
    # показывать на странице списка объектов администрирования.
    list_display = ['title', 'slug', 'author', 'publish', 'status']

    # Теперь страница
    # списка содержит правую боковую панель, которая позволяет фильтровать
    # результаты по полям, включенным в атрибут list_filter.
    list_filter = ['status', 'created', 'publish', 'author']

    # На странице появилась строка поиска. Это вызвано тем, что мы опреде-
    # лили список полей, по которым можно выполнять поиск, используя атрибут
    # search_fields.
    search_fields = ['title', 'body']

    # Далее кликните по ссылке ADD POST (Добавить пост). Здесь вы тоже заме-
    # тите некоторые изменения. При вводе заголовка нового поста поле slug запол-
    # няется автоматически. Вы сообщили Django, что нужно предзаполнять поле
    # slug данными, вводимыми в поле title, используя атрибут prepopulated_fields
    prepopulated_fields = {'slug': ('title',)}

    # Кроме того, теперь поле author отображается поисковым виджетом, который
    #  будет более приемлемым, чем выбор из выпадающего списка, когда у вас
    # тысячи пользователей. Это достигается с помощью атрибута raw_id_fields
    raw_id_fields = ['author']

    # Чуть ниже строки поиска находятся навигационные ссылки
    # для навигации по иерархии дат; это определено атрибутом date_hierarchy.
    date_hierarchy = 'publish'

    # Вы также видите, что по умолчанию посты упорядочены по столбцам STATUS (Статус)
    #  и PUBLISH (Опубликован). С помощью атрибута ordering были
    # заданы критерии сортировки, которые будут использоваться по умолчанию.
    ordering = ['status', 'publish']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']


'''


 


:

# и выглядит следующим образом:
'''
