from django.shortcuts import render
from .models import Post

# Представление post_list
# принимает объект request в качестве единственного параметра. Указанный
# параметр необходим для всех функций-представлений.
#
# В данном представлении извлекаются все посты со статусом PUBLISHED, используя
# менеджер published, который мы создали ранее.
#
# Наконец, мы используем функцию сокращенного доступа render(),
# предоставляемую Django, чтобы прорисовать список постов заданным шаблоном.
#
# Указанная функция принимает
# объект request,
# путь к шаблону и
# контекстные переменные, чтобы прорисовать данный шаблон.
#
# Она возвращает объект
# HttpResponse с прорисованным текстом (обычно исходным кодом HTML).
def post_list(request):
    posts = Post.published.all()
    return render(request,'blog/post/list.html', {'posts': posts})

'''

'''