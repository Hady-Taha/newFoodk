from django.db import models
from .utils import slugify
from customer.models import Customer
# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='Category-icon',blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)
    updated = models.DateTimeField(unique=True,auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_all_product(self):
        return self.product_set.filter(stock=True)


class Product(models.Model, models.Manager):
    title = models.CharField(max_length=50, verbose_name="اسم المنتج")
    description = models.TextField(blank=True, null=True, verbose_name="وصف المنتج")
    type_Product = models.CharField(max_length=20, default='الكمية', verbose_name="نوع المنتج ",help_text="هل المنتج با الكيلو ام با القطعه ام ب العلبة")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="الصنف")
    price = models.FloatField(verbose_name="السعر")
    discount = models.FloatField(blank=True, null=True, verbose_name="تخفيض")
    start = models.FloatField(default=1, verbose_name="الحجم")
    stock = models.BooleanField(default=True, verbose_name="هل المنتج متواجد ")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, allow_unicode=True, blank=True, null=True)

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.FloatField(default=1)
    order = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f'{self.customer}-{self.product.title}')

    @property
    def get_total_summery(self):
        if self.product.discount:
            return round(float(self.quantity * self.product.discount), 2)
        else:
            return round(float(self.quantity * self.product.price), 2)

    @property
    def get_total_price(self):
        items = Cart.objects.filter(customer=self.customer, order=False)
        total_cart = 0
        for i in items:
            total_cart += i.get_total_summery
        return round(total_cart, 2)

    def save(self, *args, **kwargs):
        super(Cart, self).save(*args, **kwargs)


class Order(models.Model):
    STATUS_CHOICES = [('تم الطلب',1 ), ('تم التوصيل',2 )]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    price = models.FloatField(blank=True, null=True)
    cart = models.ManyToManyField(Cart, related_name="items")
    discount = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default=1)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f'{self.customer.user}{" "}{self.id}')

    @property
    def get_cart(self):
        return self.cart.all()

    @property
    def get_price(self):
        price = float(0)
        for i in self.cart.all():
            price += i.get_total_summery
        return round(price, 2)


class PromoCode(models.Model):
    code = models.CharField(max_length=50)
    decrease = models.FloatField()
    counter = models.IntegerField()
    # customer    = models.ManyToManyField(Customer)

    def __str__(self):
        return str(self.code)