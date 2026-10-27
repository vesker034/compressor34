from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import (
    News, NewsCategory, NewsImage,
    Service, Product, ProductImage, ProductFeature,
    Brand, CompanyDocument, DocumentCategory
)

# ----- Инлайны -----
class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 1
    verbose_name = "Изображение"
    verbose_name_plural = "Изображения"

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    verbose_name = "Картинка"
    verbose_name_plural = "Картинки"

class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature
    extra = 2
    verbose_name = "Характеристика"
    verbose_name_plural = "Характеристики"

# ----- Новости -----
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "created_at")
    list_filter = ("category",)
    search_fields = ("title", "short_description")
    inlines = [NewsImageInline]
    prepopulated_fields = {"slug": ("title",)}
    verbose_name = "Новость"
    verbose_name_plural = "Новости"

@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    verbose_name = "Рубрика новости"
    verbose_name_plural = "Рубрики новостей"

# ----- Услуги -----
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "price_from", "avito_url") 
    list_editable = ("price_from",)  
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'image')
        }),
        ('Детали', {
            'fields': ('details', 'price_from', 'avito_url'), 
            'classes': ('collapse',)
        }),
    )
    verbose_name = "Услуга"
    verbose_name_plural = "Услуги"


# ----- Товары -----

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    class Media:
        js = ("js/hide_type_field.js",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ("title", "brand", "category", "type", "price", "is_new")
    list_filter = ("brand", "category", "type", "is_new")
    search_fields = ("title", "description")
    inlines = [ProductImageInline, ProductFeatureInline]
    prepopulated_fields = {"slug": ("title",)}
    verbose_name = "Товар"
    verbose_name_plural = "Товары"


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "logo_preview")  # ← показываем превью
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("logo_preview",)      # ← превью только для чтения
    fields = ("name", "slug", "logo", "logo_preview")

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:60px; border-radius:6px;" />', obj.logo.url)
        return "—"
    logo_preview.short_description = "Превью"

# ----- Документы -----
@admin.register(CompanyDocument)
class CompanyDocumentAdmin(admin.ModelAdmin):
    list_display = ("get_filename", "category", "uploaded_at")
    list_filter = ("category",)
    search_fields = ("file",)
    
    def get_filename(self, obj):
        return obj.get_filename()
    get_filename.short_description = "Название файла"

@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    verbose_name = "Категория документа"
    verbose_name_plural = "Категории документов"
