## Project

```shell
python -m django --version
```

```shell
django-admin startproject project_mysite
```

## App
```shell
cd project_mysite
```
```shell
python manage.py migrate
```
```shell
python manage.py runserver
```
```shell
python manage.py startapp app_blog
```

## CRUD
```sh
python manage.py shell
```

```sh
from django.contrib.auth.models import User
from app_blog.models import Post

user = User.objects.get(username='devmanyur')
```

### создать и сохранить save()

```sh
post = Post(title='Another post',
	slug='another-post',
	body='Post body.',
	author=user)
post.save()
```

### создать и сохранить create()
Создавать объект и сохранять его в базе данных также можно одной операцией, 
используя метод `create()`

```sh
Post.objects.create(title='One more post',
	slug='one-more-post',
	body='Post body.', 
	author=user)
```

### Извлечение объектов
Одиночный объект извлекается из базы данных методом `get()`

Каждая модель Django 
имеет по меньшей мере один модельный менеджер, а менеджер, который 
применяется по умолчанию, называется `objects`. Набор запросов QuerySet 
можно получать с помощью модельного менеджера.

Для того чтобы извлечь все объекты из таблицы, используется метод `all()`
```sh
all_posts = Post.objects.all()
```

Наборы запросов QuerySet в Django являются ленивыми, то есть они 
вычисляются только тогда, когда это приходится делать. 
Подобное поведение придает 
наборам запросов QuerySet большую эффективность. Если не назначать набор 
запросов QuerySet переменной, а вместо этого писать его непосредственно 
в оболочке Python, то инструкция SQL набора запросов будет исполняться
```sh
Post.objects.all()
```

### Применение метода `filter()`
Запросы с операциями поиска в полях формируются с использованием двух 
знаков подчеркивания, например cpublish__year`, но те же обозначения также 
используются для обращения к полям ассоциированных моделей, например 
`author__username`.
```sh
Post.objects.filter(publish__year=2024)
Post.objects.filter(publish__year=2024, author__username='devmanyur')
```
### Применение метода `exclude()`
```sh
Post.objects.filter(publish__year=2024).exclude(title__startswith='One')
```

### Применение метода `order_by()`
```shell
Post.objects.order_by('title')
Post.objects.order_by('-title')
```

### Удаление объектов
```shell
post = Post.objects.get(id=1) 
post.delete()
```

### Когда вычисляются наборы запросов QuerySet
- при первом их прокручивании в цикле
- при их нарезке, например Post.objects.all()[:3]; 
- при их консервации в поток байтов или кешировании; 
- при вызове на них функций repr() или len(); 
- при вызове на них функции list() в явной форме; 
- при их проверке в операциях bool(), or, and или if.

## Создание модельных менеджеров
По умолчанию в каждой модели используется менеджер 'objects'. Этот менеджер
извлекает все объекты из базы данных. Однако имеется возможность 
определять конкретно-прикладные модельные менеджеры.

Создадим конкретно-прикладной менеджер, чтобы извлекать все 
посты, имеющие статус 'PUBLISHED'

Есть два способа добавлять или адаптировать модельные менеджеры под 
конкретно-прикладную задачу:
- `Post.objects.my_manager()` можно добавлять дополнительные методы 
менеджера в существующий менеджер 
- `Post.my_manager.all()` создавать новый менеджер, видоизменив изначальный набор запросов QuerySet, возвращаемый менедже- 
ром. 

```shell
from app_blog.models import Post
Post.published.filter(title__startswith="Let's")
```
