from customer.models import Customer


def customer_or_device(request):
    try:
        customer = request.user.customer
    except:
        device = request.COOKIES.get('device')
        if Customer.objects.filter(user=None, device=device).exists():
            customer=Customer.objects.get(user=None,device=device)
        else:
            customer = Customer.objects.create(user=None,device=device)
    return customer
