import re
from django import forms
from django.contrib.auth import get_user_model

class CreateOrderForm(forms.Form):

    first_name = forms.CharField(label='Имя',
                                 widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    
    last_name = forms.CharField(label='Фамилия',
                                widget=forms.TextInput(attrs={'placeholder': 'Фамилия'}))
    middle_name = forms.CharField(label='Отчество',
                                  required=False,
                                widget=forms.TextInput(attrs={'placeholder': 'Отчество'}))
    
    email = forms.EmailField(label='E-mail',
                            required=False,
                            widget=forms.EmailInput(attrs={'placeholder': 'E-mail'}))
    
    phone_number = forms.CharField(label='Номер телефона',
                            widget=forms.TextInput(attrs={'placeholder': 'Номер телефона'}))
    
    username = forms.CharField(label='Логин',
                               required=False,
                                widget=forms.TextInput(attrs={'placeholder': 'Логин',
                                                          'class': 'form-control'}))
    
    password1 = forms.CharField(label='Пароль',
                                required=False,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='Повтор пароля',
                                required=False,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Повтор пароля'}))
    subs_news = forms.BooleanField(label='Подписка на рассылку', required=False, widget=forms.CheckboxInput(), initial=True)
    agree = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    requires_delivery = forms.BooleanField(label='Требуется доставка',
                                           widget=forms.CheckboxInput(),
                                           required=False)
    
    address_delivery = forms.CharField(label="Адрес",
                                       required=False,
                                       widget=forms.Textarea(attrs={
                                           'placeholder': 'г. Красноярск, ул., д., подъезд, кв.'
                                           }))

    postcode = forms.CharField(label='Почтовый индекс (если вы находитесь не в Красноярске) ',
                               max_length=15, required=False)
    
    notes = forms.CharField(label='Примечание к заказу', required=False, widget=forms.Textarea(attrs={'cols': "30", 'rows': "10"}))

    payment_on_get = forms.BooleanField(
        widget=forms.CheckboxInput(),
        required=False,
    )

    def clean_phone_number(self):
        pattern = re.compile(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$')
        if not pattern.match(self.cleaned_data['phone_number']):
            raise forms.ValidationError('Введите корректный номер телефона. Пример: +7(999)-99-99')
        return self.cleaned_data['phone_number']


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if self.cleaned_data.get('is_create') and password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2
    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if get_user_model().objects.filter(email=email).exists():
    #         raise forms.ValidationError('Пользователь с таким Email уже существует')
    #     return email

    def clean_agree(self):
        agree = self.cleaned_data.get('agree')
        if not agree and self.cleaned_data.get('is_create'):
            raise forms.ValidationError('Подтвердите, что вы ознакомились с правилами')
        return agree
