from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone

from .models import Product, News, Service, CompanyDocument

# --- Товары ---
class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.80

    def items(self):
        return Product.objects.all()

    def location(self, obj: Product):
        return reverse("product_detail", kwargs={"slug": obj.slug})

    def lastmod(self, obj: Product):
        # если есть updated_at в модели — используем его; иначе можно вернуть created_at
        return getattr(obj, "updated_at", None) or getattr(obj, "created_at", None)


# --- Новости (блог) ---
class NewsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.70

    def items(self):
        return News.objects.all()

    def location(self, obj: News):
        return reverse("news_detail", kwargs={"slug": obj.slug})

    def lastmod(self, obj: News):
        return getattr(obj, "created_at", None)


# --- Услуги ---
class ServiceSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.65

    def items(self):
        return Service.objects.all()

    def location(self, obj: Service):
        return reverse("service_detail", kwargs={"slug": obj.slug})

    def lastmod(self, obj: Service):
        # если у услуги нет поля updated_at — можно вернуть timezone.now() или опустить
        return timezone.now()


# --- Документы и сертификаты ---
class CompanyDocumentSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.50

    def items(self):
        return CompanyDocument.objects.all()

    def location(self, obj: CompanyDocument):
        # определяем, какой маршрут использовать
        if hasattr(obj, "category") and obj.category:
            name = obj.category.name.lower()
            if "сертифик" in name:   # "Сертификаты"
                return reverse("certificate_detail", kwargs={"slug": obj.slug})
        # иначе считаем, что это обычный документ
        return reverse("document_detail", kwargs={"slug": obj.slug})

    def lastmod(self, obj: CompanyDocument):
        return getattr(obj, "uploaded_at", None)


# --- Статичные страницы ---
class StaticPagesSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.60

    def items(self):
        # имена urlpattern’ов, у которых нет параметров
        return [
            "home",
            "about",
            "delivery",
            "how_to_get",
            "service_list",
            "news_list",
            "certificates_list",
            "documents_list",
        ]

    def location(self, name):
        return reverse(name)


# --- Категории товаров (у вас они реализованы через query-параметр) ---
# Добавим спец-класс, который вернёт два URL с ?category=...
class ProductCategoryListSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.90

    # два значения — slug категории из вашего интерфейса
    def items(self):
        return ["kompressory", "zapchasti"]

    def location(self, item):
        # /products/?category=kompressory  и  /products/?category=zapchasti
        base = reverse("product_list")
        return f"{base}?category={item}"
