from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

 
from users.forms import LoginUserForm, RegisterUserForm, AccountUserForm
 

# Create your views here.


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Войти в аккаунт'}
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('index'))
        else:
            return super().get(self, request, *args, **kwargs)


def users_cart(request):
    return render(request, 'users/user_cart.html')

# def login_user(request):
#     if request.method == 'POST':
#         form_login = LoginUserForm(request.POST)
#         if form_login.is_valid():
#             cd = form_login.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             print(cd)
#             if user and user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('blog:list_post'))
#     else:
#         form_login = LoginUserForm()
#     data = {
#         'form_login': form_login,
#     }
#
#     return render(request, 'users/login.html', context=data)

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))


# def account_user(request):
#     return render(request, 'users/user_account.html')

# def register_user(request):
#     if request.method == 'POST':
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password1'])
#             user.save()
#             return HttpResponseRedirect(reverse('users:login'))
#     else:
#         form = RegisterUserForm()
#     return render(request, 'users/register_user.html', context={'form': form})

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register_user.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('blog:list_post'))
        else:
            return super().get(self, request, *args, **kwargs)


class AccountUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = AccountUserForm
    template_name = 'users/user_account.html'
    extra_context = {'title': 'Данные аккаунта'}
    success_url = reverse_lazy('users:account')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change.html"

class UserPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = "users/password_done_change.html"