from store.models import Category, Cart
from customer.utils import customer_or_device


def categories(request):
    categories = Category.objects.select_related()
    return {'categories': categories, }


def cart(request):
    total_cart = 0
    cart = Cart.objects.filter(
        customer=customer_or_device(request), order=False)
    for i in cart:
        total_cart += i.get_total_summery
    return {'cart': cart, "total_cart": total_cart, }



def customer(request):
    
    return {'customer':customer_or_device(request)}