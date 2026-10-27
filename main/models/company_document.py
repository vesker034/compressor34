from django.db import models
from django.utils.text import slugify
import os

class DocumentCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категория/тип документа")
    slug = models.SlugField(max_length=120, unique=True, verbose_name="URL (slug)", blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Категория документа"
        verbose_name_plural = "Категории документов"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CompanyDocument(models.Model):
    category = models.ForeignKey(
        DocumentCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="documents",
        verbose_name="Категория",
    )
    file = models.FileField(upload_to="company_docs/", verbose_name="Файл документа")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")

    class Meta:
        ordering = ["-uploaded_at", "id"]
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    def get_filename(self):
        return os.path.basename(self.file.name) if self.file else ""

    def __str__(self):
        return self.get_filename()