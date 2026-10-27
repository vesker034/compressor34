from django.urls import path
from django.contrib.sitemaps.views import sitemap
from .sitemaps import (
    ProductSitemap, NewsSitemap, ServiceSitemap,
    CompanyDocumentSitemap, StaticPagesSitemap, ProductCategoryListSitemap,
)
from .views import (
    news_list, news_detail, service_list, service_detail, product_list, product_detail,
    product_search, product_autocomplete, home, avito_redirect,
    about, how_to_get, delivery, robots_txt   
)

sitemaps = {
    "products": ProductSitemap,
    "news": NewsSitemap,
    "services": ServiceSitemap,
    "docs": CompanyDocumentSitemap,
    "static": StaticPagesSitemap,
    "product_categories": ProductCategoryListSitemap,
}

urlpatterns = [
    path("", home, name="home"),

    path("news/", news_list, name="news_list"),
    path("news/<slug:slug>/", news_detail, name="news_detail"),

    path("services/", service_list, name="service_list"),
    path("services/<slug:slug>/", service_detail, name="service_detail"),

    path("products/search/", product_search, name="product_search"),
    path("products/autocomplete/", product_autocomplete, name="product_autocomplete"),
    path("products/", product_list, name="product_list"),
    path("products/<slug:slug>/", product_detail, name="product_detail"),

   


    path("products/buy/<slug:slug>/", avito_redirect, name="avito_redirect"),

    path("about/", about, name="about"),
    path("delivery/", delivery, name="delivery"),
    path("how-to-get/", how_to_get, name="how_to_get"),

    # sitemap.xml и robots.txt
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt", robots_txt, name="robots_txt"),
]
