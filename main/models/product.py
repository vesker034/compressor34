from django.db import models
from django.utils.text import slugify

class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name="Бренд")
    slug = models.SlugField(max_length=120, unique=True, verbose_name="URL (slug)", blank=True)
    logo = models.ImageField(upload_to="brands/", verbose_name="Логотип", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('kompressory', 'Компрессоры'),
        ('zapchasti', 'Запасные части'),
    ]
    PRODUCT_TYPE_CHOICES = [
        ('', 'Не указано'),
        ('porshnevye-bloki', 'Поршневые блоки'),
        ('bloki-dlya-elektrodvigatelej', 'Блоки для электродвигателей')
    ]

    title = models.CharField(max_length=255, verbose_name="Название товара")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL (slug)", blank=True)
    category = models.CharField(
        max_length=32,
        choices=CATEGORY_CHOICES,
        verbose_name="Категория",
        default='kompressory'
    )
    type = models.CharField(
        max_length=32, choices=PRODUCT_TYPE_CHOICES, default='', blank=True,
        verbose_name="Тип запчасти"
    )
    is_new = models.BooleanField(default=True, verbose_name="Новое")
    avito_url = models.URLField(verbose_name="Ссылка на Авито", blank=True, null=True)
    description = models.TextField(verbose_name="Описание")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Бренд")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Цена", blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    avito_clicks = models.PositiveIntegerField(default=0, verbose_name="Клики на Авито", editable=False)

    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE, verbose_name="Товар")
    image = models.ImageField(upload_to="products/", verbose_name="Картинка")

    def __str__(self):
        return f"Картинка для {self.product.title}"

class ProductFeature(models.Model):
    product = models.ForeignKey(Product, related_name="features", on_delete=models.CASCADE, verbose_name="Товар")
    name = models.CharField(max_length=100, verbose_name="Название характеристики")
    value = models.CharField(max_length=255, verbose_name="Значение")

    def __str__(self):
        return f"{self.name}: {self.value} ({self.product.title})"
