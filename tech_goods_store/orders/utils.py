from django.db.models import Prefetch
from .models import Order, OrderItem


def get_orders(request, *args, **kwargs):
    orders = (
        Order.objects.filter(user=request.user).prefetch_related(
            Prefetch(
                'orderitem_set',
                queryset=OrderItem.objects.all()
            )
        )
        .order_by('-id')
        )
    return orders