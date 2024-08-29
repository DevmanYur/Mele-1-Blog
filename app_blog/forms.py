'''
Django поставляется с двумя базовыми классами для разработки форм:
•• Form: позволяет компоновать стандартные формы путем определения
полей и валидаций;
•• ModelForm: позволяет компоновать формы, привязанные к экземплярам
модели. Он предоставляет все функциональности базового класса Form,
но поля формы можно объявлять явным образом или автоматически
генерировать из полей модели. Форму можно использовать для созда-
ния либо редактирования экземпляров модели.

Формы могут находиться в любом месте проекта Django. По традиции их по-
мещают внутри файла forms.py в каждом приложении.
'''

from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    # •• name: экземпляр класса CharField с максимальной длиной 25 символов,
    # который будет использоваться для имени человека, отправляющего пост
    name = forms.CharField(max_length=25)

    # •• email: экземпляр класса EmailField. Здесь используется адрес электронной
    # почты человека, отправившего рекомендуемый пост
    email = forms.EmailField()

    # •• to: экземпляр класса EmailField. Здесь используется адрес электронной
    # почты получателя, который будет получать электронное письмо с рекомендуемым постом;
    to = forms.EmailField()

    # •• comments: экземпляр класса CharField. Он используется для комментариев,
    # которые будут вставляться в электронное письмо с рекомендуемым постом.
    # Это поле сделано опциональным путем установки required
    # равным значению False, при этом был задан конкретно-прикладной
    # виджет прорисовки поля.
    comments = forms.CharField(required=False,widget=forms.Textarea)


# есть два базовых класса,
# которые можно использовать для создания форм: Form и ModelForm. Мы использовали класс Form,
# чтобы предоставлять пользователям возможность
# делиться постами по электронной почте. Теперь мы будем использовать
# ModelForm, чтобы воспользоваться преимуществами существующей модели
# Comment и компоновать для нее форму динамически.
# Для того чтобы создать форму из модели, надо в Meta-классе формы просто
# указать модель, для которой следует компоновать форму. Django проведет
# интроспекцию модели и динамически скомпонует соответствующую форму.
# Каждому типу поля модели соответствует заранее заданный тип поля фор-
# мы. Атрибуты полей модели учитываются при валидации формы. По умолчанию
# Django создает поле формы для каждого содержащегося в модели поля.
# Однако, используя атрибут fields, можно сообщать поля, которые следует
# включать в форму, либо, используя атрибут exclude, сообщать поля, которые
# следует исключать, задавая поля в явном виде. В форме CommentForm мы включили
# поля name, email и body в явном виде. Это единственные поля, которые
# будут включены в форму.
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']

'''



'''