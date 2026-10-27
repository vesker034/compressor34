from django.db import models
from django.utils.text import slugify

class Service(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название услуги")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL (slug)", blank=True)
    description = models.TextField(verbose_name="Описание услуги")
    image = models.ImageField(upload_to="services/", verbose_name="Картинка", blank=True, null=True)
    details = models.TextField(verbose_name="Полный перечень", blank=True)
    
    price_from = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена от",
        blank=True,
        null=True
    )
    

    avito_url = models.URLField(
        verbose_name="Ссылка на Авито",
        blank=True,
        null=True,
        help_text="Ссылка на объявление услуги на Авито"
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title