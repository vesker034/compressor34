from django.db import migrations, models
from django.utils.text import slugify

def set_slugs(apps, schema_editor):
    for ModelName, attr in [
        ("Brand", "name"),
        ("Category", "name"),
        ("CompanyDocument", "title"),
        ("DocumentCategory", "name"),
        ("News", "title"),
        ("Product", "title"),
        ("Service", "title"),
    ]:
        Model = apps.get_model("main", ModelName)
        for obj in Model.objects.all():
            if not obj.slug:
                obj.slug = slugify(getattr(obj, attr))
                obj.save()

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_documentcategory_companydocument'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='slug',
            field=models.SlugField(blank=True, max_length=120, unique=True, verbose_name='URL (slug)'),
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=120, unique=True, verbose_name='URL (slug)'),
        ),
        migrations.AddField(
            model_name='companydocument',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True, verbose_name='URL (slug)'),
        ),
        migrations.AddField(
            model_name='documentcategory',
            name='slug',
            field=models.SlugField(blank=True, max_length=120, unique=True, verbose_name='URL (slug)'),
        ),
        migrations.AddField(
            model_name='news',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True, verbose_name='URL (slug)'),
        ),
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True, verbose_name='URL (slug)'),
        ),
        migrations.AddField(
            model_name='service',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True, verbose_name='URL (slug)'),
        ),
        migrations.RunPython(set_slugs, reverse_code=migrations.RunPython.noop),
    ]
