
from django.contrib import messages
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import redirect, render

from carts.utils import get_user_carts
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem
from users.models import User

# Create your views here.

def create_order(request):
    user = request.user if request.user.is_authenticated else None
    carts = get_user_carts(request)

    if request.method == 'POST':
        form = CreateOrderForm(data=request.POST)
        if form.is_valid():

            # first_name = request.POST.get('first_name')
            # last_name = request.POST.get('last_name')
            # middle_name = request.POST.get('middle_name')
            # email = request.POST.get('email')
            # phone_number = request.POST.get('phone_number')
            # username = request.POST.get('username')
            # password = request.POST.get('password1')
            # subs_news = request.POST.get('subs_news')
            # requires_delivery = request.POST.get('requires_delivery')
            # address_delivery = request.POST.get('address_delivery')
            # postcode = request.POST.get('postcode')
            # notes = request.POST.get('notes')
            # payment_on_get = request.POST.get('payment_on_get')

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
                print(str(e))
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