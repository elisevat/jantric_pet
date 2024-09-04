from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path, reverse_lazy
from . import views


app_name = 'users'

urlpatterns = [
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('account/', views.AccountUser.as_view(), name='account'),
    path('cart/', views.UserCartView.as_view(), name='cart'),
    path('register/', views.RegisterUser.as_view(), name='register'),

    path('password_change/', views.UserPasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.UserPasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password-reset/',
         PasswordResetView.as_view(template_name='users/password_reset.html',
                                   email_template_name='users/password_reset_email.html',
                                   success_url=reverse_lazy('users:password_reset_done')),
         name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
                template_name='users/password_reset_confirm.html',
             success_url=reverse_lazy('users:password_reset_complete'),
         ), name='password_reset_confirm'),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]