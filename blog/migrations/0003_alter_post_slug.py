# Generated by Django 4.2.3 on 2023-07-18 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_remove_post_blog_post_publish_c4286e_idx_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(allow_unicode=True, max_length=250, unique_for_date='publish'),
        ),
    ]
