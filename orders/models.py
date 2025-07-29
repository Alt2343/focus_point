from django.db import models
from django.conf import settings
from shop.models import Product
from django.core.validators import EmailValidator, RegexValidator
# Create your models here.

class Order(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    first_name = models.CharField(max_length=50, verbose_name = "Фамилия")
    last_name = models.CharField(max_length=50, verbose_name = "Имя")
    email = models.EmailField(verbose_name = "Почта")
    phone = models.CharField(max_length=20,validators=[RegexValidator(regex=r'^\+?[0-9\s\-\(\)]+$')],help_text='Формат: +7 (XXX) XXX-XX-XX')
    address = models.CharField(max_length=100, verbose_name = "Адрес")
    postal_code = models.CharField(max_length=20, verbose_name = "Почтовый индекс")
    city = models.CharField(max_length=100, verbose_name = "Город")
    street = models.CharField(verbose_name = 'Улица',max_length=255)
    house = models.CharField(verbose_name = 'Дом',max_length=20)
    apartment = models.CharField(verbose_name = 'Квартира',max_length=20,blank=True,null=True)
    entrance = models.CharField(verbose_name = 'Подъезд',max_length=20,blank=True,null=True)
    comment = models.TextField(verbose_name = 'Комментарий к доставке',blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name = "Создан")
    updated = models.DateTimeField(auto_now=True, verbose_name = "Обновлен")
    paid = models.BooleanField(default=False , verbose_name = "Статус")
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created']
        indexes = [models.Index(fields=['-created'])]
    def __str__(self):
        return f'Order {self.id}'
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
        

class OrderItem(models. Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name = "Заказ")
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name = "Товар")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name = "Цена")
    quantity = models.PositiveIntegerField(default=1, verbose_name = "Количество")
    def __str__(self):
        return str(self.id)
    def get_cost(self):
        return self.price * self.quantity