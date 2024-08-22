from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)



class Post(models.Model):
    objects = models.Manager()  # менеджер, применяемый по умолчанию
    published = PublishedManager()


    # Мы определили перечисляемый класс Status путем подклассирования
    # класса models.TextChoices. Доступными вариантами статуса поста являются
    # DRAFT и PUBLISHED. Их соответствующими значениями выступают DF и PB, а их
    # метками или читаемыми именами являются Draft и Published.
    # Для того чтобы получать имеющиеся варианты, можно обращаться к вари-
    # антам статуса (Post.Status.choices), для того чтобы получать удобочитаемые
    # имена – к меткам статуса (Post.Status.labels), и для того чтобы получать
    # фактические значения вариантов– к значениям статуса (Post.Status.values).
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    # title: поле заголовка поста. Это поле с типом CharField, которое транс-
    # лируется в столбец VARCHAR в базе данных SQL;
    title = models.CharField(max_length=250)

    # slug: поле SlugField, которое транслируется в столбец VARCHAR в базе дан-
    # ных SQL. Слаг – это короткая метка, содержащая только буквы, цифры,
    # знаки подчеркивания или дефисы. Пост с заголовком «Django Reinhardt:
    # A legend of Jazz» мог бы содержать такой заголовок: «django-reinhardt-
    # legend-jazz». В главе 2 «Усовершенствование блога за счет продвинутых
    # функциональностей» мы будем использовать поле slug для формиро-
    # вания красивых и  дружественных для поисковой оптимизации URL-
    # адресов постов блога;
    # slug = models.SlugField(max_length=250)

    # Теперь при использовании параметра unique_for_date поле slug должно
    # быть уникальным для даты, сохраненной в поле publish. Обратите внимание,
    # что поле publish является экземпляром класса DateTimeField, но проверка на
    # уникальность значений будет выполняться только по дате (не по времени).
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')

    # Мы импортировали модель User из модуля django.contrib.auth.models и о-
    # бавили в модель Post поле author. Это поле определяет взаимосвязь многие-
    # к-одному, означающую, что каждый пост написан пользователем и пользо-
    # ватель может написать любое число постов. Для этого поля Django создаст
    # внешний ключ в базе данных, используя первичный ключ соответствующей
    # модели.
    # Параметр on_delete определяет поведение, которое следует применять
    # при удалении объекта, на который есть ссылка. Это поведение не относит-
    # ся конкретно к Django; оно является стандартным для SQL. Использование
    # ключевого слова CASCADE указывает на то, что при удалении пользователя, на
    # которого есть ссылка, база данных также удалит все связанные с ним пос-
    # ты в блоге
    # Мы используем related_name, чтобы указывать имя обратной связи, от User
    # к Post. Такой подход позволит легко обращаться к связанным объектам из
    # объекта User, используя обозначение user.blog_posts. Подробнее об этом мы
    # узнаем позже.
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')

    # body: поле для хранения тела поста. Это поле с типом TextField, которое
    # транслируется в столбец Text в базе данных SQL.
    body = models.TextField()

    # publish: поле с типом DateTimeField, которое транслируется в столбец
    # DATETIME в базе данных SQL. Оно будет использоваться для хранения
    # даты и времени публикации поста. По умолчанию значения поля за-
    # даются методом Django timezone.now. Обратите внимание, что для того,
    # чтобы использовать этот метод, был импортирован модуль timezone.
    # Метод timezone.now возвращает текущую дату/время в формате, завися-
    # щем от часового пояса. Его можно трактовать как версию стандартного
    # метода Python datetime.now с учетом часового пояса;
    publish = models.DateTimeField(default=timezone.now)

    # created: поле с типом DateTimeField. Оно будет использоваться для хра-
    # нения даты и времени создания поста. При применении параметра
    # auto_now_add дата будет сохраняться автоматически во время создания
    # объекта;
    created = models.DateTimeField(auto_now_add=True)

    # updated: поле с типом DateTimeField. Оно будет использоваться для хра-
    # нения последней даты и времени обновления поста. При применении
    # параметра auto_now дата будет обновляться автоматически во время
    # сохранения объекта.
    updated = models.DateTimeField(auto_now=True)

    # В модель также было добавлено новое поле status, являющееся экземп-
    # ляром типа CharField. Оно содержит параметр choices, чтобы ограничивать
    # значение поля вариантами из Status.choices. Кроме того, применяя параметр
    # default, задано значение поля, которое будет использоваться по умолчанию.
    # В этом поле статус DRAFT используется в качестве предустановленного вари-
    # анта, если не указан иной.
    # На практике неплохая идея – определять варианты внутри модельного класса
    # и использовать перечисляемые типы. Такой подход будет позволять легко ссы-
    # латься на метки вариантов, значения или имена из любого места исходного
    # кода. При этом можно импортировать модель Post и использовать Post.Status.
    # DRAFT в качестве ссылки на статус Draft в любом месте своего исходного кода.
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)



    # Внутрь модели был добавлен Meta-класс. Этот класс определяет метадан-
    # ные модели. Мы используем атрибут ordering, сообщающий Django, что он
    # должен сортировать результаты по полю publish. Указанный порядок будет
    # применяться по умолчанию для запросов к базе данных, когда в запросе не
    # указан конкретный порядок. Убывающий порядок задается с помощью де-
    # фиса перед именем поля: -publish. По умолчанию посты будут возвращаться
    # в обратном хронологическом порядке.
    class Meta:
        ordering = ['-publish']

        # В Meta-класс модели была добавлена опция indexes. Указанная опция по-
        # зволяет определять в модели индексы базы данных, которые могут содержать
        # одно или несколько полей в возрастающем либо убывающем порядке, или
        # функциональные выражения и функции базы данных. Был добавлен индекс
        # по полю publish, а перед именем поля применен дефис, чтобы определить
        # индекс в убывающем порядке. Создание этого индекса будет вставляться
        # в миграции базы данных, которую мы сгенерируем позже для моделей блога.
        # Индексное упорядочивание в MySQL не поддерживается. Если в качестве
        # базы данных вы используете MySQL, то убывающий индекс будет создаваться
        # как обычный индекс.
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title

    # Функция reverse() будет формировать URL-адрес динамически, применяя
    # имя URL-адреса, определенное в шаблонах URL-адресов. Мы использовали
    # именное пространство blog, за которым следуют двоеточие и URL-адрес
    # post_detail. Напомним, что именное пространство blog определяется в главном
    # файле urls.py проекта при вставке шаблонов URL-адресов из blog.urls.
    # URL-адрес post_detail определен в файле urls.py приложения blog.
    # Результирующий строковый литерал, blog:post_detail, можно использовать глобально
    # в проекте, чтобы ссылаться на URL-адрес детальной информации о посте.
    # Этот URL-адрес имеет обязательный параметр – id извлекаемого поста бло-
    # га. Идентификатор id объекта Post был включен в качестве позиционного
    # аргумента, используя параметр args=[self.id].
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       # args=[[self.id])
                       args=[self.publish.year,
                       self.publish.month,
                       self.publish.day,
                       self.slug])


'''
# 


# '''
