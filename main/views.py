from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string



from .models import (
    News, Service, Product, DocumentCategory, CompanyDocument,
    Brand
)

# --- Главная страница ---
def home(request):
    popular_products = Product.objects.order_by('-avito_clicks')[:5]
    new_products = Product.objects.filter(is_new=True)[:5]

    latest_news = News.objects.order_by('-created_at')[:4]
    brands = Brand.objects.filter(logo__isnull=False).exclude(logo="").order_by('name')
    return render(request, 'home.html', {
        'popular_products': popular_products,
        'new_products': new_products,
        'latest_news': latest_news,
        'brands': brands,
    })

# --- Новости ---
def news_list(request):
    qs = News.objects.select_related('category').order_by('-created_at', '-id')
    paginator = Paginator(qs, 16)
    page_number = request.GET.get('page') or 1
    page_obj = paginator.get_page(page_number)

    return render(request, 'news/news_list.html', {
        'page_obj': page_obj,
        'total_count': paginator.count,
    })

def news_detail(request, slug):
    news = get_object_or_404(News, slug=slug)
    return render(request, 'news/news_detail.html', {'news': news})

# --- Услуги ---

def service_list(request):
    services = Service.objects.all()  # убрал фильтрацию по is_active
    return render(request, 'services/service_list.html', {'services': services})

def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)

  
    raw = service.details or ""
    details_lines = [line.strip() for line in str(raw).splitlines() if line.strip()]

    return render(
        request,
        "services/service_detail.html",
        {
            "service": service,
            "details_lines": details_lines,  # список для чек-листа
        },
    )


# --- Товары: фильтрация по категориям, брендам, типам, пагинация ---


def _is_mobile(request) -> bool:
    ua = (request.META.get('HTTP_USER_AGENT') or '').lower()
    # простой детектор, без библиотек
    needles = ('iphone', 'android', 'mobile', 'ipod', 'windows phone')
    tablets  = ('ipad', 'tablet')
    return any(n in ua for n in needles) and not any(t in ua for t in tablets)

def product_list(request):
    category_slug = request.GET.get('category')
    brand_slugs = request.GET.getlist('brand')
    type_values = request.GET.getlist('type')

    # Изменено: сортировка в обратном порядке по ID
    products_qs = Product.objects.all().order_by('-id')
    category_selected = None

    CATEGORY_DICT = dict(Product.CATEGORY_CHOICES)
    if category_slug in CATEGORY_DICT:
        category_selected = {"slug": category_slug, "name": CATEGORY_DICT[category_slug]}
        products_qs = products_qs.filter(category=category_slug)

    if brand_slugs:
        products_qs = products_qs.filter(brand__slug__in=brand_slugs)

    if type_values:
        products_qs = products_qs.filter(type__in=type_values)

    brands = Brand.objects.all()
    product_types = Product.PRODUCT_TYPE_CHOICES

    per_page = int(request.GET.get('per') or (6 if _is_mobile(request) else 15))

    paginator = Paginator(products_qs, per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'brands': brands,
        'category_selected': category_selected,
        'selected_brands': brand_slugs,
        'product_types': product_types,
        'selected_types': type_values,
        'has_next': page_obj.has_next(),
        'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
        'per_page': per_page,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'products/product_detail.html', {'product': product})






# --- Поиск товаров (страница) ---
def product_search(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.all()
    if query:
        products = products.filter(title__icontains=query)

 
    popular_products = (
        Product.objects.order_by('-avito_clicks')
        .prefetch_related('images')[:5]
    )

    return render(
        request,
        'products/product_search.html',
        {
            'products': products,
            'query': query,
            'popular_products': popular_products,  
        },
    )
# --- Автокомплит (поиск по товарам, категориям, брендам) ---
def product_autocomplete(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        # Товары
        for p in Product.objects.filter(title__icontains=query)[:7]:
            results.append({
                'type': 'product',
                'title': p.title,
                'slug': p.slug,
                'url': f'/products/{p.slug}/',
            })
        # Категории (по name из choices)
        for key, value in Product.CATEGORY_CHOICES:
            if query.lower() in value.lower():
                results.append({
                    'type': 'category',
                    'title': f'Категория: {value}',
                    'slug': key,
                    'url': f'/products/?category={key}',
                })
        # Бренды
        for b in Brand.objects.filter(name__icontains=query)[:3]:
            results.append({
                'type': 'brand',
                'title': f'Бренд: {b.name}',
                'slug': b.slug,
                'url': f'/products/?brand={b.slug}',
            })
    return JsonResponse({'results': results})

# --- Клик по Авито-кнопке (увеличение счётчика) ---
def avito_redirect(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product.avito_clicks = (product.avito_clicks or 0) + 1
    product.save(update_fields=["avito_clicks"])
    return redirect(product.avito_url)


def about(request):
    doc_categories = (
        DocumentCategory.objects
        .prefetch_related('documents')
        .all()
        .order_by('name')
    )
    return render(request, 'static_page/about_company.html', {
        'doc_categories': doc_categories
    })

def delivery(request):
    return render(request, 'static_page/delivery.html')

def how_to_get(request):
    return render(request, 'static_page/map.html')

def robots_txt(request):
    content = """
User-agent: *
Disallow: /admin/
Disallow: /accounts/
Disallow: /cart/
Disallow: /search/
Disallow: /products/autocomplete/
Disallow: /products/search/

Allow: /products/
Allow: /services/
Allow: /news/
Allow: /documents/
Allow: /certificates/
Allow: /about/
Allow: /delivery/
Allow: /how-to-get/

Sitemap: https://compressor34.ru/sitemap.xml
Host: https://compressor34.ru
"""
    return HttpResponse(content, content_type="text/plain")