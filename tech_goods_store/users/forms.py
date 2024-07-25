from datetime import date

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Логин',
                                                             'class': 'form-control'}),
                               label='Логин')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль',
                                                                 'class': 'form-control'}),
                               label='Пароль')

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(label='Имя',
                                 widget=forms.TextInput(attrs={'placeholder': 'Имя',
                                                             'class': 'form-control'}))
    last_name = forms.CharField(label='Фамилия',
                                widget=forms.TextInput(attrs={'placeholder': 'Фамилия',
                                                             'class': 'form-control'}))

    email = forms.EmailField(label='E-mail',
                            widget=forms.EmailInput(attrs={'placeholder': 'E-mail',
                                                           'class': 'form-control'}))
    username = forms.CharField(label='Логин',
                                widget=forms.TextInput(attrs={'placeholder': 'Логин',
                                                          'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Пароль',
                                                                 'class': 'form-control'}))
    password2 = forms.CharField(label='Повтор пароля',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Повтор пароля',
                                                                  'class': 'form-control'}))
    subs_news = forms.BooleanField(label='Подписка на рассылку', required=False, widget=forms.CheckboxInput(), initial=True)
    agree = forms.BooleanField(widget=forms.CheckboxInput(), required=False)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'subs_news', 'agree']


    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким Email уже существует')
        return email

    def clean_agree(self):
        agree = self.cleaned_data['agree']
        if not agree:
            raise forms.ValidationError('Подтвердите, что вы ознакомились с правилами')
        return agree


class AccountUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин',
                                widget=forms.TextInput(attrs={'placeholder': 'Логин',
                                                          'class': 'form-control'}))
    this_year = date.today().year
    date_birth = forms.DateField(widget=forms.SelectDateWidget(years=tuple(range(this_year - 100, this_year-5))))
    class Meta:
        model = get_user_model()
        fields = ['photo', 'gender', 'first_name', 'last_name', 'username', 'date_birth', 'subs_news']

