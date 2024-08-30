from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.http import Http404
from django.views.generic import ListView

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail

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
# Функция сокращенного доступа render() учитывает контекст запроса, по-
# этому любая переменная, установленная процессорами контекста шаблона,
# доступна данному шаблону. Процессоры контекста шаблона – это просто вы-
# зываемые объекты (функции, методы и классы), которые назначают контекст
# переменным
def post_list(request):
    # posts = Post.published.all()
    post_list = Post.published.all()

    # Постраничная разбивка с 3 постами на страницу
    # 1. Мы создаем экземпляр класса Paginator с числом объектов, возвращаемых
    # в расчете на страницу. Мы будем отображать по три поста на страницу.
    # 2. Мы извлекаем HTTP GET-параметр page и сохраняем его в переменной
    # page_number. Этот параметр содержит запрошенный номер страницы.
    # Если параметра page нет в GET-параметрах запроса, то мы используем
    # стандартное значение 1, чтобы загрузить первую страницу результатов.
    # 3. Мы получаем объекты для желаемой страницы, вызывая метод page()
    # класса Paginator. Этот метод возвращает объект Page, который хранится
    # в переменной posts.
    # 4. Мы передаем номер страницы и объект posts в шаблон.
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # Если page_number не целое число, то
        # выдать первую страницу
        # Мы добавили новый блок except, чтобы при извлечении страницы управ-
        # лять исключением PageNotAnInteger. Если запрошенная страница не является
        # целым числом, то мы возвращаем первую страницу результатов.
        posts = paginator.page(1)
    except EmptyPage:
        # Если page_number находится вне диапазона, то
        # выдать последнюю страницу
        # Мы добавили блок try и except, чтобы при извлечении страницы управлять
        # исключением EmptyPage. Если запрошенная страница находится вне диапа-
        # зона, то мы возвращаем последнюю страницу результатов. Мы получаем
        # общее число страниц посредством paginator.num_pages. Общее число страниц
        # совпадает с номером последней страницы.
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})


# Указанное представление принимает аргумент id поста. Здесь мы пытаемся извлечь объект Post
# с заданным id, вызвав метод get() стандартного менеджера objects. Мы
# создаем исключение Http404, чтобы вернуть ошибку HTTP с кодом состояния,
# равным 404, если возникает исключение DoesNotExist, то есть модель не
# существует, поскольку результат не найден.
# Наконец, мы используем функцию сокращенного доступа render(), чтобы
# прорисовать извлеченный пост с использованием шаблона.
# def post_detail(request, id):

    # try:
    #     post = Post.published.get(id=id)
    # except Post.DoesNotExist:
    #     raise Http404("No Post found.")

    # Django предоставляет функцию сокращенного доступа для вызова метода
    # get() в заданном модельном менеджере и вызова исключения Http404 вместо
    # исключения DoesNotExist, когда объект не найден
    # post = get_object_or_404(Post,
    #                          id=id,
    #                          status=Post.Status.PUBLISHED)
    #
    # return render(request,'blog/post/detail.html',{'post': post})

# Мы видоизменили представление post_detail, чтобы использовать аргу-
# менты year, month, day и post и извлекать опубликованный пост с заданным
# слагом и датой публикации. Ранее, добавив в поле slug значение параметра
# unique_for_date='publish' модели Post, мы обеспечили, чтобы был только один
# пост со слагом на заданную дату. Таким образом, используя дату и слаг, мож-
# но извлекать одиночные посты.
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})


class PostListView(ListView):
    """
    Альтернативное представление списка постов
    •• атрибут queryset используется для того, чтобы иметь конкретно-при-
    кладной набор запросов QuerySet, не извлекая все объекты. Вместо
    определения атрибута queryset мы могли бы указать model=Post, и Django
    сформировал бы для нас типовой набор запросов Post.objects.all();
    •• контекстная переменная posts используется для результатов запроса.
    Если не указано имя контекстного объекта context_object_name, то по
    умолчанию используется переменная object_list;
    •• в атрибуте paginate_by задается постраничная разбивка результатов
    с возвратом трех объектов на страницу;
    •• конкретно-прикладной шаблон используется для прорисовки страницы
    шаблоном template_name. Если шаблон не задан, то по умолчанию List-
    View будет использовать blog/post_list.html.
    """

    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_share(request, post_id):

    # Извлечь пост по идентификатору id
    # Когда страница загружается в первый раз, представление получает запрос GET.
    # В этом случае создается новый экземпляр класса EmailPostForm,
    # который сохраняется в переменной form. Указанный экземпляр формы
    # будет использоваться для отображения пустой формы в шаблоне:
    # form = EmailPostForm()

    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)

    # мы объявили переменную sent с изна-
    # чальным значением False. Мы задаем этой переменной значение True после от-
    # правки электронного письма.
    sent = False

    # Когда пользователь заполняет форму и передает ее методом POST на
    # обработку, создается экземпляр формы с использованием переданных
    # данных, содержащихся в request.POST
    if request.method == 'POST':

        # Форма была передана на обработку
        form = EmailPostForm(request.POST)

        # После этого переданные данные валидируются методом is_valid() формы.
        # ных и возвращает значение True, если все поля содержат валидные данные.
        # Если какое-либо поле содержит невалидные данные, то is_valid()
        # возвращает значение False. Список ошибок валидации можно получить
        # посредством form.errors.
        # Если форма невалидна, то форма снова прорисовывается в шаблоне,
        # включая переданные данные. Ошибки валидации будут отображены в шаблоне.
        if form.is_valid():
            # Поля формы успешно прошли валидацию
            # Если форма валидна, то валидированные данные извлекаются посред-
            # ством form.cleaned_data. Указанный атрибут представляет собой словарь полей формы и их значений.
            # Если данные формы не проходят валидацию, то cleaned_data будет содержать
            # только валидные поля.
            cd = form.cleaned_data
            # ... отправить электронное письмо
           # Позже мы будем использовать переменную sent
            # в шаблоне отображения сообщения об успехе при успешной передаче формы.
            # Поскольку ссылка на пост должна вставляться в электронное письмо, мы
            # получаем абсолютный путь к посту, используя его метод get_absolute_url().
            # Мы используем этот путь на входе в метод request.build_absolute_uri(), чтобы
            # сформировать полный URL-адрес, включая HTTP-схему и хост-имя (hostname)1.
            # Мы создаем тему и текст сообщения электронного письма, используя очи-
            # щенные данные валидированной формы. Наконец, мы отправляем электрон-
            # ное письмо на адрес электронной почты, указанный в поле to (Кому) формы
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'kolodinyv@gmail.com',[cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,'form': form, 'sent': sent})


from django.views.decorators.http import require_POST
@require_POST
def post_comment(request, post_id):

    # По id поста извлекается опубликованный пост, используя функцию сокращенного доступа get_object_or_404().
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)

    # Определяется переменная comment с изначальным значением None. Указанная
    # переменная будет использоваться для хранения комментарного объекта при его создании.
    comment = None

    # Комментарий был отправлен
    # Создается экземпляр формы, используя переданные на обработку POST-
    # данные, и проводится их валидация методом is_valid(). Если форма
    # невалидна, то шаблон прорисовывается с ошибками валидации.
    form = CommentForm(data=request.POST)
    if form.is_valid():

        # Создать объект класса Comment, не сохраняя его в базе данных
        # Если форма валидна, то создается новый объект Comment, вызывая метод save()
        # формы, и назначается переменной new_comment
        # Метод save() создает экземпляр модели, к которой форма привязана,
        # и сохраняет его в базе данных. Если вызывать его, используя commit=False,
        # то экземпляр модели создается, но не сохраняется в базе данных. Такой
        # подход позволяет видоизменять объект перед его окончательным сохранением.
        # Метод save() доступен для ModelForm, но не для экземпляров класса
        # Form, поскольку они не привязаны ни к одной модели.

        comment = form.save(commit=False)
        # Назначить пост комментарию

        comment.post = post


        # Сохранить комментарий в базе данных

        comment.save()

    # Прорисовывается шаблон blog/post/comment.html, передавая объекты
    # post, form и comment в контекст шаблона
    return render(request, 'blog/post/comment.html',
                  {'post': post,
                   'form': form,
                   'comment': comment})