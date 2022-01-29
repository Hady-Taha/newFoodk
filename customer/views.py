from django.shortcuts import render
from store.models import Order
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def orders(request):
    orders = Order.objects.filter(
        customer=request.user.customer).order_by("-created")
    # orders = Order.objects.raw(f"SELECT * FROM store_order WHERE customer_id={request.user.customer.id} ORDER BY status='تم التوصيل'")
    context = {
        'title': 'orders',
        "orders": orders,
    }
    return render(request, 'customer/orders.html', context)
