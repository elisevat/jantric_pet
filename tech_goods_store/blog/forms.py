from django import forms
from .models import Comment, Posts


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Ваша электронная почта'}))
    to = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Электронная почта получателя'}))
    comments = forms.CharField(required=False,
                               widget=forms.Textarea(attrs={'placeholder': 'Комментарий'}))


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder':"Ваше имя"}),
            'email': forms.EmailInput(attrs={'placeholder': "E-mail"}),
            'body': forms.Textarea(attrs={'placeholder': "Текст"})
        }


class SearchForm(forms.Form):
    query = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
                                                                'class': 'email',
                                                                'placeholder': 'Поиск статьи',
                                                                'type': 'text',
                                                                }))


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'image', 'content', 'is_published', 'cats', 'tags']


