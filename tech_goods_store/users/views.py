from typing import Any
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.db.models import F, Prefetch
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

 
from carts.models import Cart
from orders.utils import get_orders
from users.forms import LoginUserForm, RegisterUserForm, AccountUserForm
 

# Create your views here.


class LoginUserView(LoginView):

    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Войти в аккаунт'}

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.get_user()
        if user:
            login(self.request, user)
            carts_session = Cart.objects.filter(session_key=session_key)
            carts_user = Cart.objects.filter(user=user)
            for cart in carts_session:
                if carts_user.filter(product=cart.product).exists():
                    cart_user = carts_user.get(product=cart.product)
                    cart.quantity = F("quantity") + cart.quantity
                    cart_user.delete()
                cart.user = user
                cart.save()


        return HttpResponseRedirect(self.get_success_url())
    

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('index'))
        else:
            return super().get(self, request, *args, **kwargs)
        

class UserCartView(TemplateView):
    template_name = 'users/user_cart.html'
    def get_context_data(self, **kwargs: reverse_lazy) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Корзина'


# def users_cart(request):
#     return render(request, 'users/user_cart.html')

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
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Аккаунт'
        context['orders'] = get_orders(self.request)
        return context


class UserPasswordChange(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change.html"

class UserPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = "users/password_done_change.html"