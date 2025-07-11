from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категория")
    slug = models.SlugField(max_length=100, unique=True)
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название бренда")
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, verbose_name="Описание бренда")
    logo = models.ImageField(upload_to="brands/", blank=True, null=True)
    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"
    def __str__(self):
        return self.name

class Product(models.Model):
    FRAME_TYPE_CHOICES = [
        ('full', 'Полная оправа'),
        ('half', 'Полуоправа'),
        ('rimless', 'Без оправы'),
    ]
    LENS_TYPE_CHOICES = [
        ('single', 'Однофокальные'),
        ('progressive', 'Прогрессивные'),
        ('bifocal', 'Бифокальные'),
    ]
    name = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True)
    main_image = models.ImageField(upload_to='products/main/', verbose_name="Основное изображение")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name="Бренд")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Цена")
    discount = models.PositiveIntegerField(default=0, verbose_name="Скидка (%)")
    frame_type = models.CharField(max_length=20, choices=FRAME_TYPE_CHOICES, verbose_name="Тип оправы")
    lens_type = models.CharField(max_length=20, choices=LENS_TYPE_CHOICES, verbose_name="Тип линз")
    frame_material = models.CharField(max_length=100, verbose_name="Материал оправы")
    lens_material = models.CharField(max_length=100, verbose_name="Материал линз")
    color = models.CharField(max_length=50, verbose_name="Цвет")
    gender = models.CharField(max_length=20, choices=[('men', 'Мужские'), ('women', 'Женские'), ('unisex', 'Унисекс')])
    is_available = models.BooleanField(default=True, verbose_name="Доступен")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-created_at']
    def __str__(self):
        return self.name
    @property
    def current_price(self):
        return self.price * (100 - self.discount) / 100

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/extra/")
    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товаров"
    def __str__(self):
        return f"Изображение для {self.product.name}"