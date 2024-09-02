from django.contrib.sitemaps import Sitemap
from .models import Post


# Мы определили конкретно-прикладную карту сайта, унаследовав класс
# Sitemap модуля sitemaps. Атрибуты changefreq и priority указывают частоту
# изменения страниц постов и их релевантность на веб-сайте (максимальное значение равно 1).
# Метод items() возвращает набор запросов QuerySet объектов, подлежащих включению в эту карту сайта.
#
# По умолчанию Django вызывает метод get_absolute_
# url() по каждому объекту, чтобы получить его URL-адрес.
# Если нужно указать URL-адрес каждого объекта, то в класс sitemap можно добавить метод location.


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    def items(self):
        return Post.published.all()

    # Метод lastmod получает каждый возвращаемый методом items() объект
    # и возвращает время последнего изменения объекта.
    # Атрибуты changefreq и priority могут быть либо методами, либо атрибутами.
    def lastmod(self, obj):
        return obj.updated