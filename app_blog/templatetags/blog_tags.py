
# Django предоставляет следующие вспомогательные функции, которые по-
# зволяют легко создавать шаблонные теги:
# •• simple_tag: обрабатывает предоставленные данные и возвращает стро-
# ковый литерал;
# •• inclusion_tag: обрабатывает предоставленные данные и возвращает
# прорисованный шаблон.

# Мы создали простой шаблонный тег, который возвращает число опубликованных в блоге постов.
# Для того чтобы быть допустимой библиотекой тегов, в каждом содержащем
# шаблонные теги модуле должна быть определена переменная с именем register.
# Эта переменная является экземпляром класса template.Library, и она
# используется для регистрации шаблонных тегов и фильтров приложения.
# В приведенном выше исходном коде тег total_posts был определен с помощью
# простой функции Python. В функцию был добавлен декоратор @register.
# simple_tag, чтобы зарегистрировать ее как простой тег. Django будет
# использовать имя функции в качестве имени тега. Если есть потребность за-
# регистрировать ее под другим именем, то это можно сделать, указав атрибут
# name, например @register.simple_tag(name='my_tag').


from django import template
from ..models import Post
from django.db.models import Count

register = template.Library()

@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


# В приведенном выше шаблонном теге с помощью
# функции annotate() формируется набор запросов QuerySet, чтобы агрегировать общее число ком-
# ментариев к каждому посту. Функция агрегирования Count используется для
# сохранения количества комментариев в вычисляемом поле total_comments по
# каждому объекту Post. Набор запросов QuerySet упорядочивается по вычисляемому
# полю в убывающем порядке. Также предоставляется опциональная
# переменная count, чтобы ограничивать общее число возвращаемых объектов.
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')
                                   ).order_by('-total_comments')[:count]