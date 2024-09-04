from typing import Any
from urllib import request
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from django.forms import ValidationError
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.template import context
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView

from carts.utils import get_user_carts
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem
from orders.utils import get_orders
from users.models import User

# Create your views here.
class ShowOrderView(LoginRequiredMixin, DetailView):
    template_name = 'orders/show_order.html'
    model = Order
    pk_url_kwarg = 'pk'
    context_object_name = 'order'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            return HttpResponseForbidden()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["order_items"] = OrderItem.objects.filter(order=context['order']).select_related('order', 'product')
        return context
    


@login_required
def show_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.user != request.user:
        return HttpResponseForbidden()
    order_items = OrderItem.objects.filter(order=order).select_related('order', 'product')
    context = {
        'order': order,
        'order_items': order_items
    }
    return render(request, 'orders/show_order.html', context=context)


class CreateOrderView(LoginRequiredMixin, FormView):
    template_name = 'orders/create_orders.html'
    form_class = CreateOrderForm
    success_url = reverse_lazy('users:account')

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = 'Оформление заказа' 
        context['carts'] = get_user_carts(self.request)
        return context
    
    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial.update({
                    'first_name': self.request.user.first_name,
                    'last_name': self.request.user.last_name,
                    'middle_name': self.request.user.middle_name,
                    'email': self.request.user.email,
                    'phone_number': self.request.user.phone_number,
                    'address_delivery': self.request.user.address_delivery,
                })
        return initial
    
    def form_invalid(self, form: Any) -> HttpResponse:
        messages.success(request, 'Заполните все обязательные поля')
        return redirect('orders:create_order')

    def form_valid(self, form: Any) -> HttpResponse:
        
        try:
            with transaction.atomic():
                user = self.request.user if self.request.user.is_authenticated else None
                carts = get_user_carts(self.request)
                if carts.exists():

                    #создание (регистрация) нового пользователя при желании
                    if form.cleaned_data.get('is_create'):
                        user = User.objects.create(
                            username=form.cleaned_data['username'],
                            first_name=form.cleaned_data['first_name'],
                            last_name=form.cleaned_data['last_name'],
                            middle_name=form.cleaned_data['middle_name'],
                            email=form.cleaned_data['email'],
                            phone_number=form.cleaned_data['phone_number'],
                            subs_news=bool(form.cleaned_data['subs_news']),
                            address_delivery=form.cleaned_data['address_delivery']
                            )
                        user.set_password(form.cleaned_data['password1'])
                        user.save()

                    #создание заказа
                    order = Order.objects.create(
                        user=user,
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'],
                        middle_name=form.cleaned_data['middle_name'],
                        email=form.cleaned_data['email'],
                        phone_number=form.cleaned_data['phone_number'],
                        requires_delivery=form.cleaned_data['requires_delivery'],
                        address_delivery=form.cleaned_data['address_delivery'],
                        notes=form.cleaned_data['notes'],
                    )
                    
                    #создание подзаказов (отдельных товаров)
                    for cart in carts:
                        product = cart.product
                        name = cart.product.name
                        price = cart.product.price_with_discount()
                        quantity = cart.quantity

                        if product.quantity < quantity:
                            raise ValidationError(f'''Недостаточно товара {name}.
                                                    В наличии - {product.quantity}''')

                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            name=name,
                            price=price,
                            quantity=quantity,
                        )

                        product.quantity -= quantity
                        product.save()
                    
                    carts.delete()

                    messages.success(self.request, 'Заказ оформлен')

                    return redirect('users:account')
                
        except ValidationError as e:
            messages.success(self.request, str(e))
            return redirect('orders:create_order')

def create_order(request):
    user = request.user if request.user.is_authenticated else None
    carts = get_user_carts(request)

    if request.method == 'POST':
        form = CreateOrderForm(data=request.POST)
        if form.is_valid():

            try:
                with transaction.atomic():
                    if carts.exists():

                        #создание (регистрация) нового пользователя при желании
                        if form.cleaned_data.get('is_create'):
                            user = User.objects.create(
                                username=form.cleaned_data['username'],
                                first_name=form.cleaned_data['first_name'],
                                last_name=form.cleaned_data['last_name'],
                                middle_name=form.cleaned_data['middle_name'],
                                email=form.cleaned_data['email'],
                                phone_number=form.cleaned_data['phone_number'],
                                subs_news=bool(form.cleaned_data['subs_news']),
                                address_delivery=form.cleaned_data['address_delivery']
                                )
                            user.set_password(form.cleaned_data['password1'])
                            user.save()

                        #создание заказа
                        order = Order.objects.create(
                            user=user,
                            first_name=form.cleaned_data['first_name'],
                            last_name=form.cleaned_data['last_name'],
                            middle_name=form.cleaned_data['middle_name'],
                            email=form.cleaned_data['email'],
                            phone_number=form.cleaned_data['phone_number'],
                            requires_delivery=form.cleaned_data['requires_delivery'],
                            address_delivery=form.cleaned_data['address_delivery'],
                            notes=form.cleaned_data['notes'],
                        )
                        
                        #создание подзаказов (отдельных товаров)
                        for cart in carts:
                            product = cart.product
                            name = cart.product.name
                            price = cart.product.price_with_discount()
                            quantity = cart.quantity

                            if product.quantity < quantity:
                                raise ValidationError(f'''Недостаточно товара {name}.
                                                      В наличии - {product.quantity}''')

                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                name=name,
                                price=price,
                                quantity=quantity,
                            )

                            product.quantity -= quantity
                            product.save()
                        
                        carts.delete()

                        messages.success(request, 'Заказ оформлен')

                        return redirect('users:account')
                    
            except ValidationError as e:
                messages.success(request, str(e))
                return redirect('orders:create_order')

        
    else:
        initial = {}
        
        if request.user.is_authenticated:
            initial = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'middle_name': request.user.middle_name,
                'email': request.user.email,
                'phone_number': request.user.phone_number,
                'address_delivery': request.user.address_delivery,
            }
        
        

        form = CreateOrderForm(initial=initial)

    

    context = {
        'title': 'Оформление заказа',
        'form': form,
        'carts': carts
    }
    
    return render(request, 'orders/create_orders.html', context=context)