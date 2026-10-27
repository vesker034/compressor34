from django.db import models
from django.utils.text import slugify

class NewsCategory(models.Model):
    name = models.CharField(max_length=50, verbose_name="Рубрика")

    def __str__(self):
        return self.name

class News(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL (slug)", blank=True)
    preview_image = models.ImageField(upload_to='news/previews/', verbose_name="Превью-картинка")
    short_description = models.TextField(verbose_name="Краткое описание")
    category = models.ForeignKey(NewsCategory, on_delete=models.SET_NULL, null=True, verbose_name="Рубрика")
    content = models.TextField(verbose_name="Текст новости")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class NewsImage(models.Model):
    news = models.ForeignKey(News, related_name="images", on_delete=models.CASCADE, verbose_name="Новость")
    image = models.ImageField(upload_to='news/images/', verbose_name="Изображение")

    def __str__(self):
        return f"Картинка для {self.news.title}"
