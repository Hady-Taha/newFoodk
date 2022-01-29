from allauth.account.signals import user_logged_in, user_signed_up
from django.dispatch import receiver
from .models import Customer
from store.models import Cart
from django.contrib import messages


@receiver(user_logged_in)
def user_login(request,*arrgs, **kwargs):
    device = request.COOKIES.get('device')
    customer=Customer.objects.get(device=device)
    cart=Cart.objects.filter(customer=customer)
    for item in cart:
        if item.order == False:
            item.customer = request.user.customer
            item.save()
    customer.delete()



# @receiver(user_signed_up)
# def user_signedup(request, *arrgs, **kwargs):
#     messages.success(request, 'تهانينا لقد تمت عملية التسجيل بنجاح. يمكنك الان متابعة الشراء')

