from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from random import sample
import string


class CodeGenerate(models.Model):
    code = models.CharField(max_length=255, blank=True, unique=True)

    @staticmethod
    def generate_code():
        return ''.join(sample(string.ascii_letters, 15))

    def save(self, *args, **kwargs):
        if not self.id:
            while True:
                code = self.generate_code()
                if not self.__class__.objects.filter(code=code).count():
                    self.code = code
                    break
        super(CodeGenerate, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatar/', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.IntegerField(blank=True, null=True)

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"


class Banner(CodeGenerate):
    img = models.ImageField(upload_to='banner')


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    @property
    def sub_category(self):
        return SubCategory.objects.filter(category__name=self.name)


class SubCategory(CodeGenerate):
    name = models.CharField(max_length=255, )
    image = models.ImageField(upload_to='subcategory', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(CodeGenerate):
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    des = models.TextField()
    des2 = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discountPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantity = models.IntegerField(null=True, blank=True)

    # delivery = models.BooleanField(default=False)  # +

    @property
    def images(self):
        return ProductImage.objects.filter(product__code=self.code)

    @property
    def stock_status(self):
        return bool(self.quantity)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='img/')


# class EnterProduct(CodeGenerate):
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
#     quantity = models.IntegerField()
#     date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.product.name

#     @property
#     def enterprice(self):
#         price = 0
#         if self.product.discountPrice:
#             price = self.product.discountPrice * self.quantity

#         else:
#             price = self.product.price * self.quantity
#         return price

#     def save(self, *args, **kwargs):
#         if self.pk:
#             obj = EnterProduct.objects.get(pk=self.pk)
#             self.product.quantity = self.product.quantity - obj.quantity

#         self.product.quantity = self.product.quantity + self.quantity
#         self.product.save()

#         super(EnterProduct, self).save(*args, **kwargs)


# class ProductVideo(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     video = models.FileField(upload_to='video')
#     link = models.URLField(null=True, blank=True)


class Cart(CodeGenerate):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(
        choices=(
            (1, 'No Faol'),
            (2, "Yo'lda"),
            (3, 'Qaytarilgan'),
            (4, 'Qabul qilingan')
        ),
        default=1
    )
    date = models.DateField(null=True, blank=True, auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.status == 2 and Cart.objects.get(id=self.id).status == 1:
            self.order_date = datetime.now()
        super(Cart, self).save(*args, **kwargs)

    @property
    def total(self):
        count = 0
        queryset = CartProduct.objects.filter(cart=self)
        for item in queryset:
            count += item.count
        return count

    @property
    def price(self):
        queryset = CartProduct.objects.filter(cart=self)
        total = 0
        for item in queryset:
            if item.product.discountPrice:
                total += item.count * item.product.discountPrice
            else:
                total += item.count * item.product.price
        return total

    @property
    def total_price(self):
        queryset = CartProduct.objects.filter(cart=self)
        total = 0
        for item in queryset:
            total += item.count * item.product.price
        return total


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    count = models.IntegerField()

    @property
    def price(self):
        if self.product.discountPrice:
            return self.count * self.product.discountPrice
        else:
            return self.count * self.product.price


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        obj = WishList.objects.filter(user=self.user, product=self.product)
        if obj.count():
            obj.delete()
        else:
            super(WishList, self).save(*args, **kwargs)


    def __str__(self):
        return self.product.name + " | " + self.user.username